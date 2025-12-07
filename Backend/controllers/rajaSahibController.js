const mongoose = require("mongoose");
const { getProductModel, productSchema } = require("../models/productModel");

async function storeRajaSahibData(items) {
  try {
    const productModel = getProductModel("Raja Sahib");
    let processedCount = 0;
    let skippedCount = 0;
    let createdCount = 0;
    let updatedCount = 0;

    for (let i = 1; i < items.length; i++) {
      if (!items[i] || !items[i][0] || items[i][0].trim() === "") {
        skippedCount++;
        continue;
      }

      const productName = items[i][0]?.trim() || "";
      const priceStr = items[i][2]?.trim() || "";
      const cleanedPrice = priceStr
        .replace(/Rs\.?\s*/i, "")
        .replace(/,/g, "")
        .trim();
      const originalPrice = parseFloat(cleanedPrice) || 0;

      if (originalPrice === 0) {
        skippedCount++;
        continue;
      }

      const discountedPrice = originalPrice;
      let productURL = items[i][6]?.trim() || "";
      const productImage = items[i][5]?.trim() || "";

      let filter;
      if (productURL) {
        filter = {
          productURL: productURL,
          productName: productName,
          availableAt: "Raja Sahib",
        };
      } else if (productImage) {
        filter = {
          productName: productName,
          productImage: productImage,
          originalPrice: originalPrice,
          availableAt: "Raja Sahib",
        };
      } else {
        filter = {
          productName: productName,
          originalPrice: originalPrice,
          availableAt: "Raja Sahib",
        };
      }

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
          discount: 0,
          availableAt: "Raja Sahib",
        },
        { upsert: true, new: true }
      );

      if (isNew) {
        createdCount++;
      } else {
        updatedCount++;
      }
      processedCount++;
    }

    console.log(
      `Raja Sahib: ${processedCount} processed (${createdCount} created, ${updatedCount} updated), ${skippedCount} skipped`
    );
  } catch (error) {
    console.error("Error storing products:", error);
    throw error;
  }
}

const displayProducts = async () => {
  const productModel = mongoose.model(
    "Raja Sahib",
    productSchema,
    "Raja Sahib"
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
      "Raja Sahib",
      productSchema,
      "Raja Sahib"
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

module.exports = { storeRajaSahibData, displayProducts, displayProduct };
