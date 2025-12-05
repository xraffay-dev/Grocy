import { useParams, Link } from "react-router-dom";
import { ShoppingCart, Star, Minus, Plus } from "lucide-react";
import { useState } from "react";
import { getProductById, products } from "../data/mockProducts";
import { useCart } from "../contexts/CartContext";
import ProductCard from "../components/ProductCard";
import PriceComparison from "../components/PriceComparison";

const ProductDetail = () => {
  const { id } = useParams<{ id: string }>();
  const product = id ? getProductById(id) : undefined;
  const [quantity, setQuantity] = useState(1);
  const { addToCart } = useCart();

  if (!product) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h1 className="text-3xl font-bold mb-4">Product Not Found</h1>
        <Link to="/products" className="text-primary-600 hover:underline">
          Continue Shopping
        </Link>
      </div>
    );
  }

  // Show random related products instead of by category
  const relatedProducts = products
    .filter((p) => p.id !== product.id)
    .sort(() => Math.random() - 0.5)
    .slice(0, 4);

  const handleAddToCart = () => {
    // Use the lowest price from storePrices if available, otherwise use default price
    const priceToUse =
      product.storePrices && product.storePrices.length > 0
        ? Math.min(...product.storePrices.map((sp) => sp.price))
        : product.price;

    for (let i = 0; i < quantity; i++) {
      addToCart({
        id: product.id,
        name: product.name,
        price: priceToUse,
        image: product.image,
      });
    }
  };

  // Calculate savings if store prices are available
  const getSavingsInfo = () => {
    if (!product.storePrices || product.storePrices.length === 0) return null;

    const prices = product.storePrices.map((sp) => sp.price);
    const lowestPrice = Math.min(...prices);
    const highestPrice = Math.max(...prices);

    if (lowestPrice === highestPrice) return null;

    const savings = highestPrice - lowestPrice;
    const percentage = Math.round((savings / highestPrice) * 100);

    return { amount: savings, percentage, lowestPrice, highestPrice };
  };

  const savingsInfo = getSavingsInfo();

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-4">
        <Link to="/products" className="text-primary-600 hover:underline">
          ← Back to Products
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">
        {/* Product Image */}
        <div className="relative aspect-square overflow-hidden rounded-lg bg-gray-100">
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-full object-cover"
          />
          {savingsInfo && (
            <div className="absolute top-4 left-4 flex flex-col gap-2">
              <div className="bg-green-600 text-white px-4 py-2 rounded-full font-semibold text-sm shadow-lg">
                Save Rs. {savingsInfo.amount.toFixed(0)}
              </div>
              <div className="bg-purple-600 text-white px-4 py-2 rounded-full font-semibold text-sm shadow-lg">
                {savingsInfo.percentage}% Cheaper
              </div>
            </div>
          )}
        </div>

        {/* Product Info */}
        <div>
          <h1 className="text-4xl font-bold mb-4">{product.name}</h1>

          {product.rating && (
            <div className="flex items-center gap-2 mb-4">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    size={20}
                    className={
                      i < Math.floor(product.rating!)
                        ? "fill-yellow-400 text-yellow-400"
                        : "text-gray-300"
                    }
                  />
                ))}
              </div>
              <span className="text-gray-600">
                {product.rating} ({product.totalReviews || product.reviews}{" "}
                reviews from {product.storePrices?.length || 1}{" "}
                {product.storePrices?.length === 1 ? "store" : "stores"})
              </span>
            </div>
          )}

          <div className="mb-6">
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-bold text-primary-600">
                Rs.
                {(product.storePrices && product.storePrices.length > 0
                  ? Math.min(...product.storePrices.map((sp) => sp.price))
                  : product.price
                ).toFixed(0)}
              </span>
              {savingsInfo && (
                <span className="text-lg text-gray-500 line-through">
                  Rs. {savingsInfo.highestPrice.toFixed(0)}
                </span>
              )}
            </div>
            {savingsInfo && (
              <p className="text-green-600 font-medium mt-1">
                Best price available - Save up to Rs.
                {savingsInfo.amount.toFixed(0)}
              </p>
            )}
          </div>

          <p className="text-gray-700 mb-8 text-lg leading-relaxed">
            {product.description}
          </p>

          <div className="mb-8">
            <div className="flex items-center gap-4 mb-6">
              <span className="font-semibold">Quantity:</span>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2 border border-gray-300 rounded-lg hover:bg-gray-100"
                >
                  <Minus size={20} />
                </button>
                <span className="text-xl font-semibold w-12 text-center">
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="p-2 border border-gray-300 rounded-lg hover:bg-gray-100"
                >
                  <Plus size={20} />
                </button>
              </div>
            </div>

            <button
              onClick={handleAddToCart}
              className="w-full btn-primary flex items-center justify-center gap-2 py-4 text-lg"
            >
              <ShoppingCart size={24} />
              Add to Cart
            </button>
          </div>

          <div className="border-t pt-6">
            <h3 className="font-semibold mb-2">Product Details</h3>
            <ul className="space-y-2 text-gray-600">
              <li>
                Category:{" "}
                {product.category
                  .split("-")
                  .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
                  .join(" & ")}
              </li>
              <li>Status: {product.inStock ? "In Stock" : "Out of Stock"}</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Price Comparison Section */}
      {product.storePrices && product.storePrices.length > 0 && (
        <div className="mb-16">
          <PriceComparison
            storePrices={product.storePrices}
            productName={product.name}
            defaultPrice={product.price}
          />
        </div>
      )}

      {/* Customer Reviews Section */}
      {product.rating && product.totalReviews && (
        <div className="card p-6 mb-16">
          <h2 className="text-2xl font-semibold mb-6">What people say</h2>
          <div className="flex items-center gap-4 mb-6">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  size={24}
                  className={
                    i < Math.floor(product.rating!)
                      ? "fill-yellow-400 text-yellow-400"
                      : "text-gray-300"
                  }
                />
              ))}
            </div>
            <span className="text-lg font-semibold">
              {product.totalReviews} reviews from{" "}
              {product.storePrices?.length || 1}{" "}
              {product.storePrices?.length === 1 ? "shop" : "shops"}
            </span>
          </div>
          <div className="bg-gray-50 p-6 rounded-lg border-l-4 border-primary-600">
            <p className="text-gray-700 italic">
              "Great quality product! I've been buying this regularly and it
              never disappoints. The price comparison feature helped me find the
              best deal. Highly recommend!"
            </p>
            <p className="text-sm text-gray-500 mt-3">- Verified Customer</p>
          </div>
        </div>
      )}

      {/* Related Products */}
      {relatedProducts.length > 0 && (
        <section className="mt-16">
          <h2 className="text-3xl font-bold mb-8">You May Also Like</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {relatedProducts.map((relatedProduct) => (
              <ProductCard key={relatedProduct.id} product={relatedProduct} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
};

export default ProductDetail;
