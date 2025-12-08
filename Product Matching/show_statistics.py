"""
Product Matching System - Statistics Report
============================================
Shows detailed statistics about the matching system from MongoDB.
"""

from pymongo import MongoClient


def show_statistics():
    """Display comprehensive matching statistics."""
    print("\n" + "=" * 80)
    print(" PRODUCT MATCHING SYSTEM - STATISTICS REPORT")
    print("=" * 80)
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Grocy"]
    collection = db["Product Matches"]
    
    total = collection.count_documents({})
    
    if total == 0:
        print("\n No data found! Run 'python save_matches_to_db.py' first.")
        return
    
    with_exact = collection.count_documents({"total_exact_matches": {"$gt": 0}})
    with_semantic = collection.count_documents({"total_semantic_matches": {"$gt": 0}})
    with_any = collection.count_documents({"total_matches": {"$gt": 0}})
    with_deals = collection.count_documents({"best_deal": {"$ne": None}})
    
    print(f"\n{'=' * 80}")
    print(" OVERALL STATISTICS")
    print("=" * 80)
    print(f"\n Total Products: {total:,}")
    print(f"\n Products with Exact Matches:    {with_exact:,} ({with_exact/total*100:.1f}%)")
    print(f" Products with Semantic Matches: {with_semantic:,} ({with_semantic/total*100:.1f}%)")
    print(f" Products with Any Matches:      {with_any:,} ({with_any/total*100:.1f}%)")
    print(f" Products with Best Deals:       {with_deals:,} ({with_deals/total*100:.1f}%)")
    print(f" Products with No Matches:       {total - with_any:,} ({(total-with_any)/total*100:.1f}%)")
    
    pipeline = [
        {"$group": {
            "_id": None,
            "total_exact": {"$sum": "$total_exact_matches"},
            "total_semantic": {"$sum": "$total_semantic_matches"},
            "total_all": {"$sum": "$total_matches"},
            "avg_exact": {"$avg": "$total_exact_matches"},
            "avg_semantic": {"$avg": "$total_semantic_matches"},
            "avg_total": {"$avg": "$total_matches"}
        }}
    ]
    
    stats = list(collection.aggregate(pipeline))
    
    if stats:
        s = stats[0]
        print(f"\n{'=' * 80}")
        print(" MATCH COUNTS")
        print("=" * 80)
        print(f"\n Total Exact Matches:    {s['total_exact']:,.0f}")
        print(f" Total Semantic Matches: {s['total_semantic']:,.0f}")
        print(f" Total All Matches:      {s['total_all']:,.0f}")
        print(f"\n Average Exact Matches per Product:    {s['avg_exact']:.2f}")
        print(f" Average Semantic Matches per Product: {s['avg_semantic']:.2f}")
        print(f" Average Total Matches per Product:    {s['avg_total']:.2f}")
    
    store_pipeline = [
        {"$group": {
            "_id": "$store",
            "count": {"$sum": 1},
            "with_matches": {"$sum": {"$cond": [{"$gt": ["$total_matches", 0]}, 1, 0]}},
            "with_deals": {"$sum": {"$cond": [{"$ne": ["$best_deal", None]}, 1, 0]}},
            "total_matches": {"$sum": "$total_matches"}
        }},
        {"$sort": {"count": -1}}
    ]
    
    store_stats = list(collection.aggregate(store_pipeline))
    
    print(f"\n{'=' * 80}")
    print(" STATISTICS BY STORE")
    print("=" * 80)
    print(f"\n {'Store':<20} {'Products':>10} {'With Matches':>15} {'With Deals':>12} {'Total Matches':>15}")
    print(" " + "-" * 75)
    
    for store in store_stats:
        pct_matches = store['with_matches'] / store['count'] * 100 if store['count'] > 0 else 0
        pct_deals = store['with_deals'] / store['count'] * 100 if store['count'] > 0 else 0
        print(f" {store['_id']:<20} {store['count']:>10,} {store['with_matches']:>10,} ({pct_matches:>4.1f}%) {store['with_deals']:>7,} ({pct_deals:>4.1f}%) {store['total_matches']:>15,}")
    
    savings_pipeline = [
        {"$match": {"savings_analysis": {"$ne": None}}},
        {"$group": {
            "_id": None,
            "avg_savings_pct": {"$avg": "$savings_analysis.savings_percentage"},
            "max_savings_pct": {"$max": "$savings_analysis.savings_percentage"},
            "avg_savings_per_unit": {"$avg": "$savings_analysis.savings_per_unit"}
        }}
    ]
    
    savings_stats = list(collection.aggregate(savings_pipeline))
    
    if savings_stats and savings_stats[0]:
        s = savings_stats[0]
        print(f"\n{'=' * 80}")
        print(" SAVINGS ANALYSIS")
        print("=" * 80)
        print(f"\n Average Savings Percentage: {s['avg_savings_pct']:.2f}%")
        print(f" Maximum Savings Percentage: {s['max_savings_pct']:.2f}%")
        print(f" Average Savings per Unit:   Rs. {s['avg_savings_per_unit']:.2f}")
    
    print(f"\n{'=' * 80}")
    print(" SUMMARY")
    print("=" * 80)
    print(f"\n Coverage: {with_any/total*100:.1f}% of products can be compared across stores")
    print(f" Savings Opportunities: {with_deals/total*100:.1f}% of products have cheaper alternatives")
    print(f" Average Matches: {stats[0]['avg_total']:.1f} matches per product" if stats else "")
    
    print(f"\n{'=' * 80}")
    print(" REPORT COMPLETE")
    print("=" * 80 + "\n")
    
    client.close()


if __name__ == "__main__":
    show_statistics()
