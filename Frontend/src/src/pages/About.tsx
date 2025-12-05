import { Link } from 'react-router-dom';
import { ShoppingBag, Heart, Award, Users } from 'lucide-react';

const About = () => {
  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-6">About Grocy</h1>
          <p className="text-xl text-primary-100 max-w-3xl mx-auto">
            We're on a mission to make grocery shopping easier, faster, and more convenient for everyone.
          </p>
        </div>
      </section>

      {/* Our Story */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-6">Our Story</h2>
          <div className="prose prose-lg max-w-none">
            <p className="text-gray-700 mb-4 leading-relaxed">
              Grocy was founded with a simple vision: to bring fresh, quality groceries directly to your doorstep. 
              We understand that life can be busy, and grocery shopping shouldn't be a chore.
            </p>
            <p className="text-gray-700 mb-4 leading-relaxed">
              Since our inception, we've been committed to sourcing the freshest products from trusted suppliers, 
              ensuring that every item you receive meets our high standards for quality and freshness.
            </p>
            <p className="text-gray-700 leading-relaxed">
              We believe in building lasting relationships with our customers and community. Your satisfaction 
              is our top priority, and we're constantly working to improve our service and expand our product range.
            </p>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Our Values</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <ShoppingBag className="text-primary-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Quality First</h3>
              <p className="text-gray-600">
                We never compromise on quality. Every product is carefully selected and inspected.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Heart className="text-primary-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Customer Care</h3>
              <p className="text-gray-600">
                Your satisfaction is our priority. We're here to help whenever you need us.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Award className="text-primary-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Excellence</h3>
              <p className="text-gray-600">
                We strive for excellence in everything we do, from product selection to delivery.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-primary-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="text-primary-600" size={32} />
              </div>
              <h3 className="text-xl font-semibold mb-2">Community</h3>
              <p className="text-gray-600">
                We're proud to be part of your community and support local suppliers.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Why Choose Grocy?</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold mb-3">Fresh Products</h3>
              <p className="text-gray-600">
                We work directly with local farms and trusted suppliers to bring you the freshest products available.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-3">Fast Delivery</h3>
              <p className="text-gray-600">
                Get your groceries delivered within hours. We offer same-day delivery for orders placed before 2 PM.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-3">Competitive Prices</h3>
              <p className="text-gray-600">
                We offer competitive prices on all products without compromising on quality.
              </p>
            </div>
            <div>
              <h3 className="text-xl font-semibold mb-3">Easy Returns</h3>
              <p className="text-gray-600">
                Not satisfied? We offer hassle-free returns within 7 days of purchase.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-primary-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Shopping?</h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of satisfied customers and experience the convenience of online grocery shopping.
          </p>
          <Link to="/products" className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors inline-block">
            Shop Now
          </Link>
        </div>
      </section>
    </div>
  );
};

export default About;

