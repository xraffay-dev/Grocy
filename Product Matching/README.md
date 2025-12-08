# Product Matching System

A multi-stage product matching system for cross-store grocery price comparison. This system identifies identical products and size variants across multiple stores, enabling fair price comparisons using price-per-unit calculations.

## Overview

The Product Matching System uses a 4-stage pipeline to match products across grocery stores:

| Stage | Name                  | Description                        | Purpose                                                   |
| ----- | --------------------- | ---------------------------------- | --------------------------------------------------------- |
| 1     | **LSH Blocking**      | MinHash Locality-Sensitive Hashing | Reduces search space by 99%+                              |
| 2     | **Exact Matching**    | Canonical key matching             | Identifies identical products (same brand, product, size) |
| 3     | **Semantic Matching** | Sentence Transformers + FAISS      | Finds size variants (same product, different sizes)       |
| 4     | **Price Comparison**  | Price-per-unit calculation         | Determines best deals across stores                       |

## Features

- **Cross-store matching**: Compares products across 5 grocery stores
- **Size-agnostic matching**: Finds same products in different package sizes
- **Price-per-unit comparison**: Fair comparison regardless of package size
- **Best deal identification**: Automatically highlights cheapest options
- **Savings analysis**: Calculates potential savings percentage
- **High coverage**: 60%+ of products can be compared across stores
- **Fast processing**: ~4 minutes for 20,000 products

## Project Structure

```
Product Matching/
├── config.py                 # Configuration settings (MongoDB, LSH parameters)
├── data_loader.py            # Load products from MongoDB collections
├── preprocessing.py          # Text preprocessing, brand extraction, unit normalization
├── blocking.py               # Stage 1: MinHash LSH blocking
├── exact_matcher.py          # Stage 2: Exact matching with canonical keys
├── semantic_matcher.py       # Stage 3: Semantic matching with Sentence Transformers
├── price_comparator.py       # Stage 4: Price comparison and ranking
├── product_matcher.py        # Unified matcher combining all 4 stages
├── save_matches_to_db.py     # Generate and save matches to MongoDB
├── show_statistics.py        # Display matching statistics
├── test_fast.py              # Fast interactive testing (uses MongoDB)
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Requirements

- Python 3.10+
- MongoDB 4.0+
- ~2GB RAM for processing
- ~500MB disk space for virtual environment

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/product-matching.git
cd product-matching
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example environment file and update with your MongoDB settings:

```bash
cp .env.example .env
```

Edit `.env`:

```
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=Grocy
```

### 5. Prepare MongoDB

Ensure MongoDB is running and has the following collections with product data:

- `Al-Fatah`
- `Jalal Sons`
- `Metro`
- `Rahim Store`
- `Raja Sahib`

Each product document should have:

```javascript
{
  "productID": "string",
  "productName": "string",
  "availableAt": "string",      // Store name
  "originalPrice": number,
  "discountedPrice": number,    // Optional
  "discount": number,           // Optional percentage
  "productURL": "string",       // Optional
  "productImage": "string"      // Optional
}
```

## Usage

### Quick Start

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Generate matches and save to MongoDB (run once, takes ~4 minutes)
python save_matches_to_db.py

# View statistics
python show_statistics.py

# Interactive testing
python test_fast.py
```

### Generate Product Matches

Run once to generate all matches and save to MongoDB:

```bash
python save_matches_to_db.py
```

This will:

1. Load all products from MongoDB (~20,000 products)
2. Build the 4-stage matching pipeline
3. Generate matches for every product
4. Save results to `Product Matches` collection
5. Create indexes for fast queries

**Expected output:**

```
Total products: 20,095
Products with exact matches: 1,523 (7.6%)
Products with semantic matches: 11,540 (57.4%)
Products with any matches: 12,062 (60.0%)
Products with best deals: 6,239 (31.0%)
```

### View Statistics

```bash
python show_statistics.py
```

Shows:

- Overall match statistics
- Breakdown by store
- Savings analysis

### Interactive Testing

```bash
python test_fast.py
```

Menu options:

1. Interactive search and matching
2. Test specific product by name
3. Test random products
4. Show statistics
5. Exit

### Use in Your Application

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["Grocy"]
matches = db["Product Matches"]

# Find matches for a product
product = matches.find_one({"product_name": {"$regex": "Banana Jelly", "$options": "i"}})

print(f"Product: {product['product_name']}")
print(f"Store: {product['store']}")
print(f"Price: Rs. {product['price']}")
print(f"Exact matches: {product['total_exact_matches']}")
print(f"Semantic matches: {product['total_semantic_matches']}")

if product['best_deal']:
    deal = product['best_deal']
    print(f"\nBest Deal: {deal['name']} at {deal['store']}")
    print(f"Price per unit: Rs. {deal['price_per_unit']} {deal['unit_label']}")
```

## How It Works

### Stage 1: LSH Blocking

Uses MinHash Locality-Sensitive Hashing to quickly identify candidate product pairs:

- Generates character-level 3-grams from product names
- Creates MinHash signatures (128 permutations)
- Builds LSH index with threshold 0.5
- **Result**: Reduces comparison pairs from 200M to ~64K (99.97% reduction)

### Stage 2: Exact Matching

Identifies identical products across stores using canonical keys:

```python
# Example canonical key generation
"National Banana Jelly 80gm" -> "national_banana_jelly_80_g"
```

- Extracts brand, product type, size, and unit
- Normalizes units (gm->g, ml->ml, L->ml\*1000)
- Groups products by canonical key
- **Result**: 7.6% of products have exact matches

### Stage 3: Semantic Matching

Finds same products in different sizes using Sentence Transformers:

```python
# Size-agnostic comparison
"National Banana Jelly 80gm" matches "National Banana Jelly 160gm"
```

- Removes size information before embedding
- Uses all-MiniLM-L6-v2 model (384 dimensions)
- FAISS index for fast similarity search
- Brand verification prevents false matches
- **Result**: 57.4% of products have semantic matches

### Stage 4: Price Comparison

Calculates price-per-unit for fair comparison:

```python
# Example comparison
80gm at Rs. 170 = Rs. 212.50 per 100g
160gm at Rs. 320 = Rs. 200.00 per 100g  # Better value!
```

- Normalizes to standard units (per 100g or per liter)
- Ranks by lowest price-per-unit
- Calculates savings percentage
- **Result**: 31% of products have cheaper alternatives

## MongoDB Schema

### Product Matches Collection

Each document in `Product Matches` contains:

```javascript
{
  "product_id": "string",
  "product_name": "string",
  "store": "string",
  "price": number,
  "brand": "string",
  "size": number,
  "unit": "string",
  "price_per_unit": number,
  "unit_label": "string",

  "exact_matches": [
    {
      "product_id": "string",
      "name": "string",
      "store": "string",
      "price": number,
      "match_type": "exact",
      "confidence": 1.0,
      "savings": number,
      "savings_percent": number,
      "price_per_unit": number
    }
  ],

  "semantic_matches": [
    {
      "product_id": "string",
      "name": "string",
      "store": "string",
      "size": number,
      "unit": "string",
      "price": number,
      "match_type": "semantic",
      "confidence": 0.85-0.95,
      "price_per_unit": number
    }
  ],

  "best_deal": {
    "product_id": "string",
    "name": "string",
    "store": "string",
    "price_per_unit": number
  },

  "savings_analysis": {
    "savings_per_unit": number,
    "savings_percentage": number
  },

  "total_exact_matches": number,
  "total_semantic_matches": number,
  "total_matches": number,
  "created_at": ISODate,
  "last_updated": ISODate
}
```

## Performance

| Metric                 | Value      |
| ---------------------- | ---------- |
| Total Products         | ~20,000    |
| Index Build Time       | ~4 minutes |
| Query Time             | < 100ms    |
| Coverage               | 60%        |
| Exact Match Rate       | 7.6%       |
| Semantic Match Rate    | 57.4%      |
| Best Deals             | 31%        |
| Search Space Reduction | 99.97%     |

## Statistics Explained

| Statistic            | Meaning                                          |
| -------------------- | ------------------------------------------------ |
| **Exact Matches**    | Same product, same size, different stores        |
| **Semantic Matches** | Same product, different sizes                    |
| **Any Matches**      | Has either exact or semantic matches             |
| **Best Deals**       | Found cheaper alternative (lower price-per-unit) |
| **Coverage**         | % of products that can be compared               |

## Dependencies

| Package               | Version  | Purpose                |
| --------------------- | -------- | ---------------------- |
| pymongo               | >=4.0.0  | MongoDB connection     |
| datasketch            | >=1.6.0  | MinHash LSH            |
| sentence-transformers | >=2.2.0  | Semantic embeddings    |
| faiss-cpu             | >=1.7.0  | Fast similarity search |
| rapidfuzz             | >=3.0.0  | Fuzzy string matching  |
| python-dotenv         | >=1.0.0  | Environment variables  |
| numpy                 | >=1.24.0 | Numerical operations   |
| tqdm                  | >=4.0.0  | Progress bars          |

## Troubleshooting

### "No data found" error

Run `python save_matches_to_db.py` first to generate matches.

### MongoDB connection error

Check that MongoDB is running and `.env` has correct settings.

### Slow performance

- Ensure virtual environment is activated
- First run builds indices (takes ~4 minutes)
- Subsequent queries use MongoDB (instant)

### Missing matches

- Check product names have brand and size info
- Products without size info can't be matched by size

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Create Pull Request
