# Recommendation Model

A deep learning-based product recommendation system using contrastive learning to recommend similar products across different grocery stores.

## Overview

This system analyzes 20,000+ products from 5 grocery stores and recommends similar products from other stores based on:

- Product name similarity
- Category matching
- Brand recognition
- Price comparison

**Model Performance (V5):**

- **99% accuracy** in category matching
- **2.83x category separation** (products cluster by category)
- **Cross-store recommendations** from 5 stores

## How It Works

### Architecture

```
Product Data → Feature Extraction → Contrastive AutoEncoder → Embeddings → Similarity Search
```

1. **Feature Extraction**: Extracts brand, category, size, and text features
2. **Contrastive Learning**: Trains AutoEncoder to cluster similar products
3. **L2 Normalization**: Normalizes embeddings for cosine similarity
4. **Similarity Search**: Finds top-k similar products from other stores

### Training Pipeline

```mermaid
graph LR
    A[MongoDB] --> B[mongodb_extract.py]
    B --> C[all_products.csv]
    C --> D[train_model_v5.py]
    D --> E[Model Files]
    E --> F[save_recommendations_to_db.py]
    F --> G[MongoDB: Product Recommendations]
```

## Project Structure

```
Recommendation Model/
├── main.py                         # Automated pipeline (runs all steps)
├── mongodb_extract.py              # Step 1: Extract products from MongoDB
├── feature_extraction_v5.py        # Feature extraction utilities
├── train_model_v5.py               # Step 2: Train the model
├── save_recommendations_to_db.py   # Step 3: Save recommendations to MongoDB
├── test_model_v5.py                # Interactive testing tool
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
└── models/                         # Trained model files
    ├── recommender_v5_encoder.keras
    ├── recommender_v5_autoencoder.keras
    ├── product_embeddings_v5.npy
    ├── features_scaled_v5.npy
    ├── semantic_embeddings_v5.npy
    └── feature_extractors_v5.pkl
```

## Requirements

- Python 3.10+
- MongoDB 4.0+
- TensorFlow 2.15+
- ~4GB RAM
- ~1GB disk space

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/grocy.git
cd "Grocy/Recommendation Model"
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

### 4. Configure MongoDB

Ensure MongoDB is running on `localhost:27017` with the `Grocy` database containing these collections:

- `Al-Fatah`
- `Jalal Sons`
- `Metro`
- `Rahim Store`
- `Raja Sahib`

## Usage

### Option 1: Automated Pipeline (Recommended)

Run the complete pipeline automatically:

```bash
python main.py
```

This will:

1. Extract products from MongoDB
2. Train the recommendation model
3. Save recommendations to database

**Options:**

```bash
python main.py --skip-extract  # Skip MongoDB extraction
python main.py --skip-train    # Skip model training
python main.py --skip-save     # Skip saving to database
python main.py --clean         # Clean generated files first
```

### Option 2: Step-by-Step

```bash
# Step 1: Extract products from MongoDB
python mongodb_extract.py

# Step 2: Train the model (takes ~10-15 minutes)
python train_model_v5.py

# Step 3: Save recommendations to MongoDB
python save_recommendations_to_db.py
```

### Interactive Testing

```bash
python test_model_v5.py
```

**Menu Options:**

1. Interactive search and recommendations
2. Test edge cases
3. Test specific product
4. Test random products
5. Exit

## Model Details

### Feature Extraction (1192 dimensions)

| Feature Type        | Dimensions | Description                     |
| ------------------- | ---------- | ------------------------------- |
| Semantic Embeddings | 384        | Sentence Transformer embeddings |
| Category One-Hot    | ~300       | Product categories              |
| Brand One-Hot       | ~400       | Brand identification            |
| Size Features       | 4          | Normalized size values          |
| Text Features       | ~100       | TF-IDF + keyword flags          |

### Model Architecture

```
Input (1192) → Dense(512) → Dense(256) → Dense(128) → L2Norm
                   ↓
              Encoder Output (128-dim embedding)
                   ↓
Dense(256) → Dense(512) → Dense(1192) → Output
                   ↓
              Reconstructed Features
```

### Training

- **Loss**: MSE + Contrastive Loss
- **Optimizer**: Adam (lr=0.001)
- **Epochs**: 100 with early stopping
- **Batch Size**: 64
- **Validation Split**: 20%

## MongoDB Schema

### Input Collections

Each store collection contains products with:

```javascript
{
  "productID": "string",
  "productName": "string",
  "availableAt": "string",
  "originalPrice": number,
  "discountedPrice": number,
  "discount": number,
  "productURL": "string",
  "productImage": "string"
}
```

### Output Collection: Product Recommendations

```javascript
{
  "product_id": "string",
  "product_name": "string",
  "store": "string",
  "price": number,
  "brand": "string",
  "category": "string",
  "embedding": [128 floats],
  "recommendations": [
    {
      "product_id": "string",
      "name": "string",
      "store": "string",
      "price": number,
      "category": "string",
      "similarity_score": float,
      "savings": float,
      "savings_percent": float
    }
  ],
  "best_deal": { ... },
  "total_recommendations": number,
  "model_version": "v5",
  "created_at": ISODate,
  "last_updated": ISODate
}
```

## Performance

| Metric                     | Value          |
| -------------------------- | -------------- |
| Training Time              | ~10-15 minutes |
| Embedding Generation       | ~2 minutes     |
| Recommendations Generation | ~5 minutes     |
| Total Pipeline             | ~20 minutes    |
| Accuracy                   | 99%            |
| Category Separation        | 2.83x          |
| Products                   | ~20,000        |

## Example Output

```
Query: Lindt Lindor Milk Chocolate 200gm

Store: Metro | Price: Rs. 1,850 | Category: chocolates

Recommendations:
1. Ferrero Rocher 200gm
   Store: Al-Fatah | Price: Rs. 1,650
   Similarity: 94.2% | Save: Rs. 200 (10.8%)

2. Toblerone Swiss Milk Chocolate 200gm
   Store: Jalal Sons | Price: Rs. 1,750
   Similarity: 92.1% | Save: Rs. 100 (5.4%)
```

## Troubleshooting

### "No module named X"

```bash
pip install -r requirements.txt
```

### MongoDB connection error

- Ensure MongoDB is running: `mongod`
- Check connection string in scripts

### Model files not found

```bash
python train_model_v5.py  # Regenerate model files
```

### Out of memory

- Close other applications
- Reduce batch size in train_model_v5.py

## Dependencies

| Package               | Version  | Purpose                 |
| --------------------- | -------- | ----------------------- |
| tensorflow            | >=2.15.0 | Deep learning framework |
| pandas                | >=2.0.0  | Data processing         |
| numpy                 | >=1.24.0 | Numerical operations    |
| pymongo               | >=4.0.0  | MongoDB connection      |
| scikit-learn          | >=1.3.0  | Feature scaling         |
| sentence-transformers | >=2.2.0  | Text embeddings         |
| tqdm                  | >=4.0.0  | Progress bars           |

## License

MIT License - See LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request
