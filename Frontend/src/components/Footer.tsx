import { Link } from 'react-router-dom';
import { Facebook, Twitter, Instagram, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-gray-300 mt-auto border-t border-gray-700/50">
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* About */}
          <div>
            <h3 className="text-white text-3xl font-extrabold mb-4 gradient-text">Grocy</h3>
            <p className="text-gray-400 mb-6 leading-relaxed">
              Your trusted online grocery store. Fresh products delivered to your doorstep.
            </p>
            <div className="flex gap-3">
              <a href="#" className="bg-gray-800 hover:bg-primary-600 p-3 rounded-xl transition-all duration-300 hover:scale-110">
                <Facebook size={20} />
              </a>
              <a href="#" className="bg-gray-800 hover:bg-primary-600 p-3 rounded-xl transition-all duration-300 hover:scale-110">
                <Twitter size={20} />
              </a>
              <a href="#" className="bg-gray-800 hover:bg-primary-600 p-3 rounded-xl transition-all duration-300 hover:scale-110">
                <Instagram size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white font-bold text-lg mb-6">Quick Links</h4>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/products" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  All Products
                </Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  Contact Us
                </Link>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h4 className="text-white font-bold text-lg mb-6">Customer Service</h4>
            <ul className="space-y-3">
              <li>
                <Link to="/account" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  My Account
                </Link>
              </li>
              <li>
                <Link to="/orders" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  Order History
                </Link>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  Shipping Info
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors duration-200 hover:translate-x-1 inline-block">
                  Returns
                </a>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-white font-bold text-lg mb-6">Contact Us</h4>
            <ul className="space-y-4">
              <li className="flex items-start gap-3">
                <div className="bg-primary-600/20 p-2 rounded-lg">
                  <MapPin size={18} className="text-primary-400" />
                </div>
                <span className="text-gray-400">123 Grocery Street, Food City, FC 12345</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="bg-primary-600/20 p-2 rounded-lg">
                  <Phone size={18} className="text-primary-400" />
                </div>
                <span className="text-gray-400">+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center gap-3">
                <div className="bg-primary-600/20 p-2 rounded-lg">
                  <Mail size={18} className="text-primary-400" />
                </div>
                <span className="text-gray-400">support@grocy.com</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-700/50 mt-12 pt-8 text-center">
          <p className="text-gray-500">&copy; 2024 Grocy. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

