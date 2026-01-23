"""
Product Matching Pipeline
==========================
Automates the complete product matching process:
1. Load products from MongoDB
2. Build matching indices (LSH, Exact, Semantic)
3. Generate product matches
4. Save matches to database

Usage: python main.py [--skip-save] [--top-k N]
"""

import sys

sys.path.insert(0, "venv/Lib/site-packages")

import argparse
from datetime import datetime
from pymongo import MongoClient
from tqdm import tqdm

from data_loader import ProductDataLoader
from product_matcher import ProductMatcher
from price_comparator import PriceComparator
from preprocessing import extract_product_attributes


def print_header(text):
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80)


def print_step(step_num, total, text):
    print(f"\n[{step_num}/{total}] {text}")
    print("-" * 80)


class ProductMatchingPipeline:
    """
    Handles the complete product matching pipeline from data loading to database storage.
    """

    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="Grocy"):
        """Initialize MongoDB connection."""
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.loader = None
        self.products = []
        self.matcher = None

    def step1_load_products(self):
        """Step 1: Load products from MongoDB."""
        print_step(1, 4, "Loading products from MongoDB")

        print("Connecting to MongoDB...")
        self.loader = ProductDataLoader()

        print("Loading products from all stores...")
        print("  - Al-Fatah")
        print("  - Jalal Sons")
        print("  - Metro")
        print("  - Rahim Store")
        print("  - Raja Sahib")

        self.products = self.loader.load_products_from_stores()

        print(f"\n Loaded {len(self.products):,} products")

        # Show breakdown by store
        stores = {}
        for product in self.products:
            store = product["availableAt"]
            stores[store] = stores.get(store, 0) + 1

        print("\nProducts by store:")
        for store, count in sorted(stores.items(), key=lambda x: x[1], reverse=True):
            print(f"  {store}: {count:,}")

        return True

    def step2_build_indices(self):
        """Step 2: Build matching indices (LSH, Exact, Semantic)."""
        print_step(2, 4, "Building matching indices")

        print("Initializing 4-stage matching system...")
        print("  Stage 1: LSH Blocking (MinHash)")
        print("  Stage 2: Exact Matching (Canonical Keys)")
        print("  Stage 3: Semantic Matching (Sentence Transformers)")
        print("  Stage 4: Price Comparison (Price-per-unit)")

        self.matcher = ProductMatcher()

        print(f"\nBuilding indices for {len(self.products):,} products...")
        self.matcher.build_index(self.products)

        print("\n Matching system ready!")
        print(f"  LSH index built")
        print(f"  Exact match index built")
        print(f"  Semantic embeddings generated")
        print(f"  FAISS index created")

        return True

    def step3_generate_matches(self, top_k=10):
        """Step 3: Generate product matches."""
        print_step(3, 4, "Generating product matches")

        print(f"  Configuration:")
        print(f"  Products: {len(self.products):,}")
        print(f"  Matches per product: {top_k}")
        print(f"  Match types: Exact + Semantic")

        documents = []
        comparator = PriceComparator()

        print("\nProcessing products...")
        for product in tqdm(self.products, desc="Generating matches"):
            product_id = product["productID"]

            price_data = self.matcher.get_price_comparison(product_id)

            if not price_data:
                continue

            query_product = price_data["query_product"]
            matches = price_data["matches"][:top_k]
            price_comparison = price_data["price_comparison"]
            savings = price_data["savings_analysis"]

            query_attrs = extract_product_attributes(query_product["productName"])
            query_price_info = comparator.calculate_price_per_unit(query_product)

            exact_matches = []
            semantic_matches = []

            for match in matches:
                match_product = match["product"]
                match_type = match["match_type"]
                confidence = match["confidence"]

                match_attrs = extract_product_attributes(match_product["productName"])
                match_price_info = comparator.calculate_price_per_unit(match_product)

                savings_amount = (
                    query_product["originalPrice"] - match_product["originalPrice"]
                )
                savings_pct = (
                    (savings_amount / query_product["originalPrice"] * 100)
                    if query_product["originalPrice"] > 0
                    else 0
                )

                match_doc = {
                    "product_id": match_product["productID"],
                    "name": match_product["productName"],
                    "store": match_product["availableAt"],
                    "price": float(match_product["originalPrice"]),
                    "discounted_price": float(match_product.get("discountedPrice", 0)),
                    "discount": float(match_product.get("discount", 0)),
                    "url": match_product.get("productURL", ""),
                    "image": match_product.get("productImage", ""),
                    "brand": match_attrs["brand"],
                    "size": float(match_attrs["size"]) if match_attrs["size"] else None,
                    "unit": match_attrs["unit"],
                    "match_type": match_type,
                    "confidence": float(confidence),
                    "savings": float(savings_amount),
                    "savings_percent": float(savings_pct),
                    "price_per_unit": (
                        float(match_price_info["price_per_unit"])
                        if match_price_info["price_per_unit"]
                        else None
                    ),
                    "unit_label": match_price_info["unit_label"],
                }

                if match_type == "exact":
                    exact_matches.append(match_doc)
                else:
                    semantic_matches.append(match_doc)

            best_deal = None
            if price_comparison and len(price_comparison) > 1:
                best_price_comparison = price_comparison[0]
                best_product = best_price_comparison["product"]
                best_price_info = best_price_comparison["price_info"]

                if best_product["productID"] != product_id:
                    best_attrs = extract_product_attributes(best_product["productName"])
                    best_deal = {
                        "product_id": best_product["productID"],
                        "name": best_product["productName"],
                        "store": best_product["availableAt"],
                        "price": float(best_product["originalPrice"]),
                        "price_per_unit": (
                            float(best_price_info["price_per_unit"])
                            if best_price_info["price_per_unit"]
                            else None
                        ),
                        "unit_label": best_price_info["unit_label"],
                        "size": (
                            float(best_attrs["size"]) if best_attrs["size"] else None
                        ),
                        "unit": best_attrs["unit"],
                        "url": best_product.get("productURL", ""),
                        "image": best_product.get("productImage", ""),
                    }

            savings_analysis = None
            if savings["has_savings"]:
                savings_analysis = {
                    "savings_per_unit": float(savings["savings_per_unit"]),
                    "savings_percentage": float(savings["savings_percentage"]),
                }

            document = {
                "product_id": product_id,
                "product_name": query_product["productName"],
                "store": query_product["availableAt"],
                "price": float(query_product["originalPrice"]),
                "discounted_price": float(query_product.get("discountedPrice", 0)),
                "discount": float(query_product.get("discount", 0)),
                "url": query_product.get("productURL", ""),
                "image": query_product.get("productImage", ""),
                "brand": query_attrs["brand"],
                "size": float(query_attrs["size"]) if query_attrs["size"] else None,
                "unit": query_attrs["unit"],
                "price_per_unit": (
                    float(query_price_info["price_per_unit"])
                    if query_price_info["price_per_unit"]
                    else None
                ),
                "unit_label": query_price_info["unit_label"],
                "exact_matches": exact_matches,
                "semantic_matches": semantic_matches,
                "best_deal": best_deal,
                "savings_analysis": savings_analysis,
                "total_exact_matches": len(exact_matches),
                "total_semantic_matches": len(semantic_matches),
                "total_matches": len(exact_matches) + len(semantic_matches),
                "model_version": "v1_4stage",
                "created_at": datetime.now(),
                "last_updated": datetime.now(),
            }

            documents.append(document)

        print(f"\n Generated matches for {len(documents):,} products")

        # Statistics
        total_exact = sum(doc["total_exact_matches"] for doc in documents)
        total_semantic = sum(doc["total_semantic_matches"] for doc in documents)
        total_matches = sum(doc["total_matches"] for doc in documents)
        avg_matches = total_matches / len(documents) if documents else 0
        products_with_matches = sum(1 for d in documents if d["total_matches"] > 0)
        products_with_deals = sum(1 for d in documents if d["best_deal"] is not None)

        print(f"\nMatch Statistics:")
        print(f"  Total exact matches: {total_exact:,}")
        print(f"  Total semantic matches: {total_semantic:,}")
        print(f"  Total matches: {total_matches:,}")
        print(f"  Average per product: {avg_matches:.1f}")
        print(
            f"  Products with matches: {products_with_matches:,} ({products_with_matches / len(documents) * 100:.1f}%)"
        )
        print(
            f"  Products with best deals: {products_with_deals:,} ({products_with_deals / len(documents) * 100:.1f}%)"
        )

        return documents

    def step4_save_to_mongodb(
        self, documents, collection_name="Product Matches", auto_overwrite=False
    ):
        """Step 4: Save matches to MongoDB."""
        print_step(4, 4, "Saving matches to MongoDB")

        if collection_name in self.db.list_collection_names():
            print(f"Collection '{collection_name}' already exists")

            if auto_overwrite:
                print("  Auto-overwrite enabled, dropping existing collection...")
                self.db[collection_name].drop()
                print(" Dropped existing collection")
            else:
                response = input("  Overwrite? (y/n): ")
                if response.lower() != "y":
                    print(" Cancelled")
                    return False

                self.db[collection_name].drop()
                print(" Dropped existing collection")

        collection = self.db[collection_name]

        print(f"\nInserting {len(documents):,} documents...")
        batch_size = 1000

        for i in tqdm(range(0, len(documents), batch_size), desc="Inserting batches"):
            batch = documents[i : i + batch_size]
            collection.insert_many(batch)

        print(f"\n Saved {len(documents):,} documents to MongoDB")

        print("\nCreating indexes...")
        collection.create_index("product_id")
        collection.create_index("product_name")
        collection.create_index("store")
        collection.create_index("brand")
        collection.create_index([("price_per_unit", 1)])
        print(" Indexes created")

        return True

    def cleanup(self):
        """Cleanup resources."""
        if self.loader:
            self.loader.close()
        if self.client:
            self.client.close()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Product Matching Pipeline")
    parser.add_argument(
        "--skip-save", action="store_true", help="Skip saving to database"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=10,
        help="Number of matches per product (default: 10)",
    )
    parser.add_argument(
        "--auto-overwrite",
        action="store_true",
        help="Automatically overwrite existing collection",
    )
    args = parser.parse_args()

    print_header("PRODUCT MATCHING PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n4-Stage Matching System | Cross-Store Price Comparison")

    try:
        MONGO_URI = "mongodb://localhost:27017/"
        DB_NAME = "Grocy"
        COLLECTION_NAME = "Product Matches"

        pipeline = ProductMatchingPipeline(mongo_uri=MONGO_URI, db_name=DB_NAME)

        # Step 1: Load products
        success = pipeline.step1_load_products()
        if not success:
            print(" Failed to load products")
            return 1

        # Step 2: Build indices
        success = pipeline.step2_build_indices()
        if not success:
            print(" Failed to build indices")
            return 1

        # Step 3: Generate matches
        documents = pipeline.step3_generate_matches(top_k=args.top_k)
        if not documents:
            print(" Failed to generate matches")
            return 1

        # Step 4: Save to MongoDB (optional)
        if not args.skip_save:
            success = pipeline.step4_save_to_mongodb(
                documents, COLLECTION_NAME, auto_overwrite=args.auto_overwrite
            )
            if not success:
                print("  Saving to database was cancelled or failed")
        else:
            print("\n  Skipping database save (--skip-save flag)")

        # Cleanup
        pipeline.cleanup()

        # Summary
        print_header("PIPELINE SUMMARY")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Status: SUCCESS")
        print(f"\nResults:")
        print(f"  Products processed: {len(documents):,}")
        print(f"  MongoDB Collection: {COLLECTION_NAME}")
        if not args.skip_save:
            print(f"  Documents saved: {len(documents):,}")
        print(f"\n Product matching system is ready to use!")

        return 0

    except KeyboardInterrupt:
        print("\n\n  Pipeline interrupted by user")
        return 1
    except Exception as e:
        print(f"\n ERROR: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
