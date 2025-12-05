const mongoose = require("mongoose");
const { getProductModel, productSchema } = require("../models/productModel");

async function storeRahimStoreData(items) {
  try {
    const productModel = getProductModel("Rahim Store");
    let processedCount = 0;
    let skippedCount = 0;
    let createdCount = 0;
    let updatedCount = 0;
    const skippedProducts = [];
    const updatedProducts = [];

    for (let i = 1; i < items.length; i++) {
      if (!items[i] || !items[i][0] || items[i][0].trim() === "") {
        skippedCount++;
        skippedProducts.push({
          row: i + 1,
          reason: "Empty product name",
          data: items[i],
        });
        continue;
      }

      const productName = items[i][0]?.trim() || "";
      // Remove commas from price strings before parsing (e.g., "1,098" -> "1098")
      const originalPriceStr = (items[i][2] || "").toString().replace(/,/g, "");
      const originalPrice = parseFloat(originalPriceStr) || 0;
      const discountedPriceStr = (items[i][1] || "")
        .toString()
        .replace(/,/g, "");
      const discountedPrice = parseFloat(discountedPriceStr) || originalPrice;
      let productURL = items[i][3]?.trim() || "";
      const productImage = items[i][4]?.trim() || "";

      // Skip if price is 0 or invalid
      if (originalPrice === 0) {
        skippedCount++;
        skippedProducts.push({
          row: i + 1,
          reason: "Invalid or missing price",
          productName: productName,
          priceString: items[i][2]?.trim() || "",
        });
        continue;
      }

      // Calculate discount percentage from price difference
      let discount = 0;
      if (originalPrice > 0 && discountedPrice < originalPrice) {
        discount = ((originalPrice - discountedPrice) / originalPrice) * 100;
      }

      // Use combination of fields as unique identifier
      // This prevents products with same URL but different names from overwriting each other
      // If URL is empty, use combination of productName + productImage + originalPrice to ensure uniqueness
      // If image is also empty, use productName + originalPrice + availableAt
      let filter;
      if (productURL) {
        // Combine URL with productName to ensure uniqueness
        filter = {
          productURL: productURL,
          productName: productName,
          availableAt: "Rahim Store",
        };
      } else if (productImage) {
        filter = {
          productName: productName,
          productImage: productImage,
          originalPrice: originalPrice,
          availableAt: "Rahim Store",
        };
      } else {
        filter = {
          productName: productName,
          originalPrice: originalPrice,
          availableAt: "Rahim Store",
        };
      }

      // Check if document exists before update to track creates vs updates
      const existingDoc = await productModel.findOne(filter);
      const isNew = !existingDoc;

      await productModel.findOneAndUpdate(
        filter,
        {
          productName: productName,
          productImage: productImage,
          productURL: productURL,
          originalPrice: originalPrice,
          discountedPrice: discountedPrice,
          discount: discount,
          availableAt: "Rahim Store",
        },
        { upsert: true, new: true }
      );

      if (isNew) {
        createdCount++;
      } else {
        updatedCount++;
        updatedProducts.push({
          row: i + 1,
          productName: productName,
          originalPrice: originalPrice,
          productImage: productImage,
          productURL: productURL,
          existingPrice: existingDoc?.originalPrice,
          existingName: existingDoc?.productName,
        });
      }
      processedCount++;
    }
    console.log(
      `Products stored successfully in Rahim Store collection: ${processedCount} processed (${createdCount} created, ${updatedCount} updated), ${skippedCount} skipped`
    );

    if (skippedProducts.length > 0) {
      console.log("\n=== SKIPPED PRODUCTS ===");
      skippedProducts.forEach((skipped) => {
        console.log(`\nRow ${skipped.row}: ${skipped.reason}`);
        if (skipped.productName) {
          console.log(`  Product: ${skipped.productName}`);
        }
        if (skipped.priceString) {
          console.log(`  Price: "${skipped.priceString}"`);
        }
        if (skipped.data) {
          console.log(`  Data: ${JSON.stringify(skipped.data)}`);
        }
      });
    }

    if (updatedProducts.length > 0) {
      console.log(
        "\n=== UPDATED/OVERWRITTEN PRODUCTS (" +
          updatedProducts.length +
          ") ==="
      );
      const duplicateGroups = {};
      updatedProducts.forEach((updated) => {
        const key = updated.productName;
        if (!duplicateGroups[key]) {
          duplicateGroups[key] = [];
        }
        duplicateGroups[key].push(updated);
      });

      Object.entries(duplicateGroups).forEach(([name, products]) => {
        if (products.length > 0) {
          console.log(`\nProduct: ${name}`);
          products.forEach((p) => {
            const imageStatus = p.productImage ? "Yes" : "No";
            const urlStatus = p.productURL ? "Yes" : "No";
            console.log(
              "  Row " +
                p.row +
                ": Price Rs. " +
                p.originalPrice +
                ", Image: " +
                imageStatus +
                ", URL: " +
                urlStatus
            );
            if (p.existingName && p.existingName !== p.productName) {
              console.log(
                "    Overwrote: " +
                  p.existingName +
                  " (Price: Rs. " +
                  p.existingPrice +
                  ")"
              );
            } else if (p.existingPrice && p.existingPrice !== p.originalPrice) {
              console.log(
                "    Overwrote existing price: Rs. " +
                  p.existingPrice +
                  " -> Rs. " +
                  p.originalPrice
              );
            }
          });
        }
      });
    }
  } catch (error) {
    console.error("Error storing products:", error);
    throw error;
  }
}

const displayProducts = async () => {
  const productModel = mongoose.model(
    "Rahim Store",
    productSchema,
    "Rahim Store"
  );
  const products = await productModel.find();

  return {
    success: true,
    status: 200,
    count: products.length,
    data: products,
  };
};

const displayProduct = async (productID = "nil") => {
  try {
    const productModel = mongoose.model(
      "Rahim Store",
      productSchema,
      "Rahim Store"
    );

    if (productID === "nil") {
      return { success: false, status: 404, message: "Product not found" };
    }

    const product = await productModel.findOne({ productID });

    if (!product) {
      return { success: false, status: 404, message: "Product not found" };
    }

    return {
      success: true,
      status: 200,
      data: {
        productID: product.productID,
        productName: product.productName,
        productURL: product.productURL,
        productImage: product.productImage,
        originalPrice: product.originalPrice,
        discount: product.discount,
        discountedPrice: product.discountedPrice,
        availableAt: product.availableAt,
      },
    };
  } catch (error) {
    console.error("Error fetching product:", error);

    return {
      success: false,
      status: 500,
      message: error.message,
    };
  }
};

module.exports = { storeRahimStoreData, displayProducts, displayProduct };
