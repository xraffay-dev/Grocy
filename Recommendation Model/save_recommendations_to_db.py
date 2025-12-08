"""
Save product recommendations to MongoDB using the Phase 3 V5 model.

This script generates product recommendations for all products in the database
and saves them to a MongoDB collection for efficient retrieval.
"""

import numpy as np
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from tqdm import tqdm
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# Custom L2 normalization layer (required for V5 model)
class L2Normalization(layers.Layer):
    """L2 normalization layer for contrastive learning"""
    def call(self, inputs):
        return tf.nn.l2_normalize(inputs, axis=1)
    
    def compute_output_shape(self, input_shape):
        return input_shape
    
    def get_config(self):
        return super().get_config()


class RecommendationSaver:
    """
    Handles generation and storage of product recommendations using the V5 model.
    """
    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="Grocy"):
        """Initialize MongoDB connection and load the V5 model."""
        print("Connecting to MongoDB...")
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        
        print("Loading V5 recommendation model...")
        
        # Load V5 encoder with custom L2Normalization layer
        custom_objects = {'L2Normalization': L2Normalization}
        self.encoder = keras.models.load_model(
            'models/recommender_v5_encoder.keras',
            custom_objects=custom_objects
        )
        self.embeddings = np.load('models/product_embeddings_v5.npy')
        self.products_df = pd.read_csv('product_features_v5.csv')
        self.original_products_df = pd.read_csv('all_products.csv')
        
        print(f"✅ Loaded {len(self.products_df):,} products")
        print(f"   Model: V5 (99% accuracy, 2.83x category separation)\n")
    
    def generate_recommendations_for_all(self, top_k=10, max_price_ratio=1.5):
        """Generate recommendations for all products."""
        print("\n" + "="*70)
        print("GENERATING RECOMMENDATIONS FOR ALL PRODUCTS")
        print("="*70 + "\n")
        
        print(f"Configuration:")
        print(f"  Products: {len(self.products_df):,}")
        print(f"  Recommendations per product: {top_k}")
        print(f"  Max price ratio: {max_price_ratio}")
        
        documents = []
        
        for idx in tqdm(range(len(self.products_df)), desc="Generating recommendations"):
            query_product = self.products_df.iloc[idx]
            query_embedding = self.embeddings[idx]
            query_price = query_product['price']
            query_store = query_product['store']
            query_category = query_product['category']
            
            # Calculate similarities (cosine similarity)
            similarities = np.dot(self.embeddings, query_embedding) / (
                np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            similar_indices = np.argsort(similarities)[::-1]
            
            recommendations = []
            
            for sim_idx in similar_indices:
                if sim_idx == idx:
                    continue
                
                candidate = self.products_df.iloc[sim_idx]
                
                # Category filter (same category only)
                if candidate['category'] != query_category:
                    continue
                
                # Store filter
                if candidate['store'] == query_store:
                    continue
                
                # Price filter
                if candidate['price'] > query_price * max_price_ratio:
                    continue
                
                savings = query_price - candidate['price']
                savings_pct = (savings / query_price * 100) if query_price > 0 else 0
                
                orig_product = self.original_products_df[
                    self.original_products_df['_id'] == candidate['_id']
                ]
                
                if len(orig_product) > 0:
                    orig_product = orig_product.iloc[0]
                    
                    recommendations.append({
                        'product_id': str(candidate['_id']),
                        'name': candidate['name'],
                        'store': candidate['store'],
                        'price': float(candidate['price']),
                        'category': candidate['category'],
                        'url': orig_product.get('url', ''),
                        'image': orig_product.get('image', ''),
                        'similarity_score': float(similarities[sim_idx]),
                        'savings': float(savings),
                        'savings_percent': float(savings_pct)
                    })
                
                if len(recommendations) >= top_k:
                    break
            
            best_deal = None
            if recommendations:
                best_deal = max(recommendations, key=lambda x: x['savings'])
            
            orig_query = self.original_products_df[
                self.original_products_df['_id'] == query_product['_id']
            ]
            
            if len(orig_query) > 0:
                orig_query = orig_query.iloc[0]
                
                document = {
                    'product_id': str(query_product['_id']),
                    'product_name': query_product['name'],
                    'store': query_store,
                    'price': float(query_price),
                    'url': orig_query.get('url', ''),
                    'image': orig_query.get('image', ''),
                    'brand': query_product['brand'],
                    'category': query_category,
                    'embedding': query_embedding.tolist(),
                    'recommendations': recommendations,
                    'best_deal': best_deal,
                    'total_recommendations': len(recommendations),
                    'model_version': 'v5',
                    'created_at': datetime.now(),
                    'last_updated': datetime.now()
                }
                
                documents.append(document)
        
        print(f"\n✅ Generated recommendations for {len(documents):,} products")
        
        total_recs = sum(doc['total_recommendations'] for doc in documents)
        avg_recs = total_recs / len(documents) if documents else 0
        
        print(f"\nStatistics:")
        print(f"  Total recommendations: {total_recs:,}")
        print(f"  Average per product: {avg_recs:.1f}")
        print(f"  Products with recommendations: {sum(1 for d in documents if d['total_recommendations'] > 0):,}")
        
        return documents
    
    def save_to_mongodb(self, documents, collection_name='Product Recommendations'):
        """Save recommendation documents to MongoDB."""
        print("\n" + "="*70)
        print(f"SAVING TO MONGODB: {collection_name}")
        print("="*70 + "\n")
        
        if collection_name in self.db.list_collection_names():
            print(f"Collection '{collection_name}' already exists")
            response = input("  Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled")
                return
            
            self.db[collection_name].drop()
            print(f"Dropped existing collection")
        
        collection = self.db[collection_name]
        
        print(f"Inserting {len(documents):,} documents...")
        batch_size = 1000
        
        for i in tqdm(range(0, len(documents), batch_size), desc="Inserting batches"):
            batch = documents[i:i+batch_size]
            collection.insert_many(batch)
        
        print(f"\n✅ Saved {len(documents):,} documents to MongoDB")
        
        print("\nCreating indexes...")
        collection.create_index('product_id')
        collection.create_index('product_name')
        collection.create_index('store')
        collection.create_index('category')
        print("✅ Indexes created")


def main():
    """Main execution function."""
    print("="*70)
    print("SAVE RECOMMENDATIONS TO MONGODB - V5 MODEL")
    print("99% Accuracy | 2.83x Category Separation")
    print("="*70)
    
    try:
        MONGO_URI = "mongodb://localhost:27017/"
        DB_NAME = "Grocy"
        COLLECTION_NAME = "Product Recommendations"
        TOP_K = 10
        MAX_PRICE_RATIO = 1.5
        
        saver = RecommendationSaver(mongo_uri=MONGO_URI, db_name=DB_NAME)
        
        documents = saver.generate_recommendations_for_all(
            top_k=TOP_K,
            max_price_ratio=MAX_PRICE_RATIO
        )
        
        saver.save_to_mongodb(documents, COLLECTION_NAME)
        
        print("\n" + "="*70)
        print("✅ ALL DONE!")
        print("="*70)
        print(f"\nMongoDB Collection: {COLLECTION_NAME}")
        print(f"Total documents: {len(documents):,}")
        print("\nRecommendation system is ready to use!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())