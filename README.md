# 🛒 Grocy - Smart Grocery Price Comparison Platform

<div align="center">

![Grocy Banner](./Grocy%20Architecture%20Diagram.png)

**An intelligent grocery shopping platform that helps you find the best deals across multiple stores using AI-powered product matching and recommendations.**

[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Components](#-components)
- [ML Models](#-ml-models)
- [API Documentation](#-api-documentation)
- [Performance Metrics](#-performance-metrics)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

**Grocy** is a comprehensive grocery price comparison platform that aggregates products from **5 major grocery stores** in Pakistan and uses advanced machine learning algorithms to help users find the best deals. With over **20,000 products** indexed, Grocy provides intelligent product matching, AI-powered recommendations, and real-time price comparisons.

### Why Grocy?

- 💰 **Save Money**: Compare prices across 5 stores and find the best deals automatically
- 🤖 **AI-Powered**: Deep learning recommendations and semantic product matching
- ⚡ **Fast & Accurate**: 99% accuracy in product matching with sub-100ms query times
- 📊 **Comprehensive**: 60% product coverage with cross-store comparisons
- 🎯 **Smart Matching**: Find identical products and size variants across different stores

---

## ✨ Key Features

### 🔍 **Intelligent Search**

- Full-text search across all stores
- Real-time search suggestions
- Category and brand filtering

### 🎯 **Product Matching**

- **4-stage matching pipeline** using LSH blocking, exact matching, semantic matching, and price comparison
- **99.97% search space reduction** for lightning-fast comparisons
- **Price-per-unit calculations** for fair size-variant comparisons
- Identifies **31% of products** with cheaper alternatives

### 🤖 **AI Recommendations**

- **Deep learning model** with 99% category accuracy
- **Contrastive learning** for semantic similarity
- Cross-store product recommendations
- "You May Also Like" suggestions

### 💰 **Price Comparison**

- Real-time price tracking across 5 stores
- Discount and savings calculations
- Best deal highlighting
- Price history (coming soon)

### 🛍️ **Shopping Features**

- Shopping cart with multi-store support
- User authentication and accounts
- Order history tracking
- Responsive mobile-first design

---

## 🏗️ System Architecture

Grocy follows a **3-tier architecture** with separate frontend, backend, and ML components:

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React + TypeScript)            │
│  • Vite + React Router • TailwindCSS • Context API              │
└─────────────────────────┬───────────────────────────────────────┘
                          │ REST API
┌─────────────────────────▼───────────────────────────────────────┐
│                      BACKEND (Node.js + Express)                 │
│  • RESTful API • MongoDB Integration • CORS Support             │
└─────────────────────────┬───────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼──────┐  ┌──────▼──────┐  ┌──────▼──────────┐
│   MongoDB    │  │   Product   │  │ Recommendation  │
│   Database   │  │   Matching  │  │     Model       │
│              │  │   (Python)  │  │    (Python)     │
│ 5 Store      │  │             │  │                 │
│ Collections  │  │ • LSH       │  │ • TensorFlow    │
│              │  │ • FAISS     │  │ • Transformers  │
│ • Al-Fatah   │  │ • MinHash   │  │ • AutoEncoder   │
│ • Metro      │  │             │  │                 │
│ • Jalal Sons │  │ 4-Stage     │  │ Contrastive     │
│ • Raja Sahib │  │ Pipeline    │  │ Learning        │
│ • Rahim Store│  │             │  │                 │
└──────────────┘  └─────────────┘  └─────────────────┘
```

---

## 🛠️ Technology Stack

### **Frontend**

- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Vite** - Lightning-fast build tool
- **React Router v6** - Client-side routing
- **TailwindCSS** - Utility-first styling
- **Lucide React** - Beautiful icons

### **Backend**

- **Node.js** - JavaScript runtime
- **Express 5** - Web framework
- **MongoDB** - NoSQL database
- **Mongoose** - MongoDB ODM
- **CORS** - Cross-origin support
- **dotenv** - Environment management

### **Machine Learning**

- **TensorFlow 2.15** - Deep learning framework
- **Sentence Transformers** - Semantic embeddings
- **FAISS** - Fast similarity search
- **MinHash LSH** - Locality-sensitive hashing
- **scikit-learn** - Feature engineering
- **pandas & numpy** - Data processing

### **Data Collection**

- **Jupyter Notebooks** - Web scraping
- **BeautifulSoup** - HTML parsing
- **Selenium** - Dynamic content scraping

---

## 📁 Project Structure

```
Grocy/
├── Frontend/                      # React TypeScript Frontend
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── Header.tsx        # Navigation header with search
│   │   │   ├── Footer.tsx        # Site footer
│   │   │   ├── ProductCard.tsx   # Product display card
│   │   │   ├── PriceComparison.tsx  # Price comparison widget
│   │   │   └── Layout.tsx        # Main layout wrapper
│   │   ├── pages/                # Route pages
│   │   │   ├── Home.tsx          # Landing page
│   │   │   ├── Products.tsx      # Product listing
│   │   │   ├── ProductDetail.tsx # Product details
│   │   │   ├── SearchResults.tsx # Search results
│   │   │   ├── Cart.tsx          # Shopping cart
│   │   │   ├── Checkout.tsx      # Checkout flow
│   │   │   ├── Login.tsx         # User login
│   │   │   ├── Register.tsx      # User registration
│   │   │   ├── Account.tsx       # User account
│   │   │   ├── OrderHistory.tsx  # Order history
│   │   │   ├── About.tsx         # About page
│   │   │   └── Contact.tsx       # Contact page
│   │   ├── contexts/             # React contexts
│   │   │   ├── AuthContext.tsx   # Authentication state
│   │   │   └── CartContext.tsx   # Shopping cart state
│   │   ├── services/             # API services
│   │   │   └── api.ts            # API client
│   │   ├── types/                # TypeScript types
│   │   ├── App.tsx               # Main app component
│   │   └── main.tsx              # Entry point
│   ├── package.json
│   └── vite.config.ts
│
├── Backend/                       # Node.js Express Backend
│   ├── config/
│   │   └── dbConfig.js           # MongoDB connection
│   ├── controllers/              # Route controllers
│   │   ├── alFatahController.js
│   │   ├── metroController.js
│   │   ├── jalalSonsController.js
│   │   ├── rajaSahibController.js
│   │   ├── rahimStoreController.js
│   │   ├── featuredController.js
│   │   ├── productMatchesController.js
│   │   └── searchController.js
│   ├── routes/                   # API routes
│   │   ├── alFatahRouter.js
│   │   ├── metroRouter.js
│   │   ├── jalalSonsRouter.js
│   │   ├── rajaSahibRouter.js
│   │   ├── rahimStoreRouter.js
│   │   ├── featuredRouter.js
│   │   ├── productMatchesRouter.js
│   │   └── searchRouter.js
│   ├── models/
│   │   └── productModel.js       # Product schema
│   ├── utils/
│   │   └── extractData.js        # CSV data import
│   ├── scrapped data/            # Raw scraped data
│   ├── app.js                    # Express app setup
│   └── package.json
│
├── Product Matching/              # ML Product Matching System
│   ├── config.py                 # Configuration
│   ├── data_loader.py            # MongoDB data loader
│   ├── preprocessing.py          # Text preprocessing
│   ├── blocking.py               # Stage 1: LSH blocking
│   ├── exact_matcher.py          # Stage 2: Exact matching
│   ├── semantic_matcher.py       # Stage 3: Semantic matching
│   ├── price_comparator.py       # Stage 4: Price comparison
│   ├── product_matcher.py        # Unified matcher
│   ├── save_matches_to_db.py     # Save to MongoDB
│   ├── show_statistics.py        # Display stats
│   ├── test_fast.py              # Interactive testing
│   ├── requirements.txt
│   └── README.md
│
├── Recommendation Model/          # ML Recommendation System
│   ├── main.py                   # Automated pipeline
│   ├── mongodb_extract.py        # Extract from MongoDB
│   ├── feature_extraction_v5.py  # Feature engineering
│   ├── train_model_v5.py         # Model training
│   ├── save_recommendations_to_db.py  # Save to MongoDB
│   ├── test_model_v5.py          # Interactive testing
│   ├── analyze_data.py           # Data analysis
│   ├── requirements.txt
│   └── README.md
│
├── Scrappers/                     # Web Scraping Scripts
│   ├── Al-Fatah.ipynb            # Al-Fatah scraper
│   ├── Metro.ipynb               # Metro scraper
│   ├── Jalal Sons.ipynb          # Jalal Sons scraper
│   ├── Raja Sahib.ipynb          # Raja Sahib scraper
│   └── Rahim Store.ipynb         # Rahim Store scraper
│
├── .gitignore
└── README.md                      # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** 16+ and npm
- **Python** 3.10+
- **MongoDB** 4.0+ (local or Atlas)
- **Git**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/xraffay-dev/Grocy.git
cd Grocy
```

### 2️⃣ Setup Backend

```bash
cd Backend

# Install dependencies
npm install

# Create .env file
echo "MONGODB_URI=mongodb://localhost:27017/Grocy" > .env
echo "PORT=8000" >> .env

# Start the server
npm run dev
```

The backend will run on `http://localhost:8000`

### 3️⃣ Setup Frontend

```bash
cd ../Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will run on `http://localhost:5173`

### 4️⃣ Setup Product Matching (Optional)

```bash
cd "../Product Matching"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure MongoDB
cp .env.example .env
# Edit .env with your MongoDB connection string

# Generate product matches (~4 minutes)
python save_matches_to_db.py

# View statistics
python show_statistics.py
```

### 5️⃣ Setup Recommendation Model (Optional)

```bash
cd "../Recommendation Model"

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run automated pipeline (~20 minutes)
python main.py

# Or run step-by-step:
python mongodb_extract.py
python train_model_v5.py
python save_recommendations_to_db.py
```

---

## 🧩 Components

### Frontend Components

#### **Header Component**

- Responsive navigation with mobile menu
- Real-time search with autocomplete
- Store navigation links
- Shopping cart indicator
- User authentication menu

#### **ProductCard Component**

- Product image with lazy loading
- Price display with discount badges
- Store information
- Quick add to cart
- Responsive grid layout

#### **PriceComparison Component**

- Side-by-side price comparison
- Best deal highlighting
- Savings calculations
- Store availability indicators

### Backend API Endpoints

#### **Store Endpoints**

```
GET /alfatah          - Get all Al-Fatah products
GET /alfatah/:id      - Get specific product
GET /metro            - Get all Metro products
GET /metro/:id        - Get specific product
GET /jalalsons        - Get all Jalal Sons products
GET /jalalsons/:id    - Get specific product
GET /rajasahib        - Get all Raja Sahib products
GET /rajasahib/:id    - Get specific product
GET /rahimstore       - Get all Rahim Store products
GET /rahimstore/:id   - Get specific product
```

#### **Featured & Recommendations**

```
GET /featured/random?limit=8              - Get random featured products
GET /featured/product/:id                 - Get product with recommendations
GET /featured/related/:id?category=...    - Get related products
```

#### **Product Matching**

```
GET /matches?limit=8                      - Get products with matches
GET /matches/product/:id                  - Get product matches
GET /matches/recommendations/:id          - Get "You May Also Like"
GET /matches/search?q=...                 - Search with matches
```

#### **Search**

```
GET /search?query=...&limit=50           - Search all stores
```

---

## 🤖 ML Models

### Product Matching System

A **4-stage pipeline** for cross-store product matching:

#### **Stage 1: LSH Blocking**

- **Technology**: MinHash Locality-Sensitive Hashing
- **Purpose**: Reduce search space by 99.97%
- **Method**: Character-level 3-grams with 128 permutations
- **Result**: 200M comparisons → 64K candidates

#### **Stage 2: Exact Matching**

- **Technology**: Canonical key matching
- **Purpose**: Find identical products across stores
- **Method**: Normalize brand, product, size, and unit
- **Result**: 7.6% of products have exact matches

#### **Stage 3: Semantic Matching**

- **Technology**: Sentence Transformers + FAISS
- **Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Purpose**: Find size variants of same product
- **Result**: 57.4% of products have semantic matches

#### **Stage 4: Price Comparison**

- **Technology**: Price-per-unit normalization
- **Purpose**: Fair comparison across different sizes
- **Method**: Normalize to per 100g or per liter
- **Result**: 31% of products have cheaper alternatives

### Recommendation Model

A **deep learning model** using contrastive learning:

#### **Architecture**

```
Input (1192 dims) → Dense(512) → Dense(256) → Dense(128) → L2 Norm
                                                    ↓
                                            Encoder Output
                                                    ↓
                    Dense(256) → Dense(512) → Dense(1192)
                                                    ↓
                                          Reconstructed Features
```

#### **Features**

- **Semantic Embeddings**: 384 dims (Sentence Transformers)
- **Category One-Hot**: ~300 dims
- **Brand One-Hot**: ~400 dims
- **Size Features**: 4 dims
- **Text Features**: ~100 dims (TF-IDF)

#### **Training**

- **Loss**: MSE + Contrastive Loss
- **Optimizer**: Adam (lr=0.001)
- **Epochs**: 100 with early stopping
- **Performance**: 99% category accuracy, 2.83x category separation

---

## 📊 Performance Metrics

### Product Matching

| Metric                   | Value      |
| ------------------------ | ---------- |
| Total Products           | ~20,000    |
| Index Build Time         | ~4 minutes |
| Query Time               | <100ms     |
| Coverage                 | 60%        |
| Exact Match Rate         | 7.6%       |
| Semantic Match Rate      | 57.4%      |
| Products with Best Deals | 31%        |
| Search Space Reduction   | 99.97%     |

### Recommendation Model

| Metric                     | Value          |
| -------------------------- | -------------- |
| Training Time              | ~10-15 minutes |
| Embedding Generation       | ~2 minutes     |
| Recommendations Generation | ~5 minutes     |
| Total Pipeline             | ~20 minutes    |
| Category Accuracy          | 99%            |
| Category Separation        | 2.83x          |
| Products Indexed           | ~20,000        |

### Frontend Performance

| Metric                 | Value  |
| ---------------------- | ------ |
| First Contentful Paint | <1.5s  |
| Time to Interactive    | <3s    |
| Lighthouse Score       | 90+    |
| Bundle Size            | <500KB |

---

## 📸 Screenshots

### Home Page

_Beautiful landing page with featured products and store navigation_

### Product Listing

_Grid view of products with filters and sorting options_

### Product Details

_Detailed product view with price comparison and recommendations_

### Search Results

_Real-time search with intelligent matching across all stores_

### Price Comparison

_Side-by-side comparison showing best deals and savings_

---

## 🎯 Use Cases

### For Shoppers

- 🛍️ **Compare prices** across 5 stores instantly
- 💰 **Find best deals** automatically
- 📦 **Discover alternatives** with similar products
- 🎯 **Get recommendations** based on your interests

### For Developers

- 🔧 **Learn ML integration** with web applications
- 📚 **Study product matching** algorithms
- 🎓 **Understand recommendation systems**
- 🚀 **Build scalable applications**

---

## 🔮 Future Enhancements

- [ ] **Price History Tracking** - Track price changes over time
- [ ] **Price Alerts** - Notify users when prices drop
- [ ] **Shopping Lists** - Create and manage shopping lists
- [ ] **Barcode Scanner** - Mobile app with barcode scanning
- [ ] **Delivery Integration** - Partner with delivery services
- [ ] **User Reviews** - Product ratings and reviews
- [ ] **Nutritional Info** - Display nutritional information
- [ ] **Recipe Suggestions** - Suggest recipes based on cart items
- [ ] **Budget Tracker** - Track spending and set budgets
- [ ] **Store Locator** - Find nearest stores with maps

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow existing code style and conventions
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

<!-- ## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

--- -->

## 👨‍💻 Author

**Abdul Rafay**

- GitHub: [@xraffay-dev](https://github.com/xraffay-dev)
- Project Link: [https://github.com/xraffay-dev/Grocy](https://github.com/xraffay-dev/Grocy)

---

## 🙏 Acknowledgments

- **Sentence Transformers** for semantic embeddings
- **TensorFlow** for deep learning framework
- **FAISS** for fast similarity search
- **React** and **Vite** for amazing developer experience
- **MongoDB** for flexible data storage
- All the grocery stores for providing product data

---

## 📞 Support

If you have any questions or need help, please:

1. Check the [documentation](./README.md)
2. Search [existing issues](https://github.com/xraffay-dev/Grocy/issues)
3. Open a [new issue](https://github.com/xraffay-dev/Grocy/issues/new)

---

<div align="center">

**Made with ❤️ and lots of ☕**

⭐ **Star this repo if you find it helpful!** ⭐

</div>
