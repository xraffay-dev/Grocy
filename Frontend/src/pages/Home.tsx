import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import ProductCard from "../components/ProductCard";
import { products, stores } from "../data/mockProducts";

const Home = () => {
  const featuredProducts = products.slice(0, 8);

  return (
    <div>
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-600 via-primary-500 to-primary-700 text-white overflow-hidden">
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }}
        ></div>
        <div className="container mx-auto px-4 py-24 md:py-32 relative z-10">
          <div className="max-w-3xl animate-slide-up">
            <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight">
              Fresh Groceries
              <br />
              <span className="bg-gradient-to-r from-white to-primary-100 bg-clip-text text-transparent">
                Delivered to Your Door
              </span>
            </h1>
            <p className="text-xl md:text-2xl mb-10 text-primary-50 leading-relaxed">
              Shop the freshest produce, premium meats, and everyday essentials.
              Fast delivery, great prices, and quality you can trust.
            </p>
            <Link
              to="/products"
              className="inline-flex items-center gap-3 bg-white text-primary-600 px-10 py-5 rounded-2xl font-bold text-lg shadow-2xl hover:shadow-3xl hover:scale-105 active:scale-100 transition-all duration-300 group"
            >
              Shop Now
              <ArrowRight
                size={22}
                className="group-hover:translate-x-1 transition-transform"
              />
            </Link>
          </div>
        </div>
      </section>

      {/* Stores Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4">
            Shop by <span className="gradient-text">Store</span>
          </h2>
          <p className="text-gray-600 text-lg">
            Compare prices across your favorite stores
          </p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
          {stores.map((store, index) => (
            <Link
              key={store.path}
              to={store.path}
              className="card-hover overflow-hidden group animate-fade-in flex flex-col items-center justify-center p-8 hover:shadow-xl transition-all duration-300"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              <div className="w-24 h-24 mb-4 flex items-center justify-center">
                <img
                  src={store.logo}
                  alt={store.name}
                  className="max-w-full max-h-full object-contain group-hover:scale-110 transition-transform duration-500"
                />
              </div>
              <h3 className="text-lg font-bold text-center group-hover:text-primary-600 transition-colors">
                {store.name}
              </h3>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Products */}
      <section className="bg-gradient-to-b from-gray-50 to-white py-20">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between mb-16">
            <div>
              <h2 className="text-4xl md:text-5xl font-extrabold mb-2">
                Featured <span className="gradient-text">Products</span>
              </h2>
              <p className="text-gray-600 text-lg">
                Handpicked favorites just for you
              </p>
            </div>
            <Link
              to="/products"
              className="hidden md:flex items-center gap-2 text-primary-600 font-bold hover:text-primary-700 hover:gap-3 transition-all duration-300"
            >
              View All
              <ArrowRight
                size={20}
                className="group-hover:translate-x-1 transition-transform"
              />
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featuredProducts.map((product, index) => (
              <div
                key={product.id}
                style={{ animationDelay: `${index * 100}ms` }}
                className="animate-fade-in"
              >
                <ProductCard product={product} />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center mb-16 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4">
            Why Choose <span className="gradient-text">Grocy?</span>
          </h2>
          <p className="text-gray-600 text-lg">Experience the difference</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="card p-8 text-center hover:scale-105 transition-transform duration-300 animate-fade-in">
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg shadow-primary-500/30">
              <span className="text-4xl">🚚</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Fast Delivery</h3>
            <p className="text-gray-600 leading-relaxed">
              Get your groceries delivered within hours, not days.
            </p>
          </div>
          <div
            className="card p-8 text-center hover:scale-105 transition-transform duration-300 animate-fade-in"
            style={{ animationDelay: "100ms" }}
          >
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg shadow-primary-500/30">
              <span className="text-4xl">✨</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Fresh Quality</h3>
            <p className="text-gray-600 leading-relaxed">
              We source only the freshest products from trusted suppliers.
            </p>
          </div>
          <div
            className="card p-8 text-center hover:scale-105 transition-transform duration-300 animate-fade-in"
            style={{ animationDelay: "200ms" }}
          >
            <div className="bg-gradient-to-br from-primary-500 to-primary-600 w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg shadow-primary-500/30">
              <span className="text-4xl">💰</span>
            </div>
            <h3 className="text-2xl font-bold mb-3">Best Prices</h3>
            <p className="text-gray-600 leading-relaxed">
              Competitive prices on all your favorite grocery items.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
