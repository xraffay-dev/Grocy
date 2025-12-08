"""
FILE 2: analyze_data.py
=======================
Analyzes product data to understand patterns and prepare for labeling

Run: python analyze_data.py
Input: all_products.csv
Output: Analysis report + candidate_pairs.cs
"""

import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from collections import Counter
import re

class DataAnalyzer:
    def __init__(self, products_csv='all_products.csv'):
        """
        Initialize analyzer with products data
        
        Args:
            products_csv: Path to products CSV
        """
        print("Loading products data...")
        self.products_df = pd.read_csv(products_csv)
        print(f"Loaded {len(self.products_df)} products\n")
    
    def analyze_basic_stats(self):
        """
        Analyze basic statistics about the products
        """
        print("="*70)
        print("BASIC STATISTICS")
        print("="*70 + "\n")
        
        df = self.products_df
        
        # Store distribution
        print("Products per store:")
        store_counts = df['store'].value_counts()
        for store, count in store_counts.items():
            print(f"  {store}: {count} products")
        
        # Product name characteristics
        df['name_length'] = df['name'].str.len()
        df['word_count'] = df['name'].str.split().str.len()
        
        print(f"\nProduct name characteristics:")
        print(f"  Length: {df['name_length'].min()}-{df['name_length'].max()} chars (avg: {df['name_length'].mean():.1f})")
        print(f"  Words: {df['word_count'].min()}-{df['word_count'].max()} words (avg: {df['word_count'].mean():.1f})")
        
        # Price distribution
        print(f"\nPrice distribution:")
        print(f"  Min: Rs. {df['price'].min():.2f}")
        print(f"  25%: Rs. {df['price'].quantile(0.25):.2f}")
        print(f"  50%: Rs. {df['price'].quantile(0.50):.2f}")
        print(f"  75%: Rs. {df['price'].quantile(0.75):.2f}")
        print(f"  Max: Rs. {df['price'].max():.2f}")
    
    def analyze_word_patterns(self):
        """
        Analyze common words and patterns in product names
        """
        print("\n" + "="*70)
        print("WORD PATTERN ANALYSIS")
        print("="*70 + "\n")
        
        # Extract all words
        all_words = []
        for name in self.products_df['name']:
            words = str(name).lower().split()
            all_words.extend(words)
        
        word_freq = Counter(all_words)
        
        print("Most common words (top 30):")
        for word, count in word_freq.most_common(30):
            if len(word) > 2:  # Skip very short words
                print(f"  {word}: {count} occurrences")
        
        # Detect size patterns
        print("\nSize/quantity patterns found:")
        size_patterns = [
            (r'\d+\s*gm?\b', 'grams'),
            (r'\d+\s*kg\b', 'kilograms'),
            (r'\d+\s*ml\b', 'milliliters'),
            (r'\d+\s*ltr?\b', 'liters'),
            (r'\d+\s*pcs?\b', 'pieces'),
        ]
        
        for pattern, unit in size_patterns:
            matches = sum(1 for name in self.products_df['name'] 
                         if re.search(pattern, str(name).lower()))
            if matches > 0:
                print(f"  {unit}: {matches} products")
    
    def find_potential_matches(self, n_candidates=1000):
        """
        Find product pairs that potentially match
        Uses string similarity to identify candidates
        
        Args:
            n_candidates: Number of candidate pairs to generate
        
        Returns:
            DataFrame with candidate pairs
        """
        print("\n" + "="*70)
        print("FINDING POTENTIAL MATCHING PAIRS")
        print("="*70 + "\n")
        
        print("This will help you with manual labeling...")
        print("Finding pairs with high similarity across different stores...\n")
        
        candidates = []
        stores = self.products_df['store'].unique()
        
        # Compare products across different stores
        for i, store1 in enumerate(stores):
            for store2 in stores[i+1:]:
                print(f"Comparing {store1} vs {store2}...")
                
                products1 = self.products_df[self.products_df['store'] == store1]
                products2 = self.products_df[self.products_df['store'] == store2]
                
                # Sample to keep it manageable
                sample_size1 = min(300, len(products1))
                sample_size2 = min(300, len(products2))
                
                products1_sample = products1.sample(n=sample_size1, random_state=42)
                products2_sample = products2.sample(n=sample_size2, random_state=42)
                
                for _, prod1 in products1_sample.iterrows():
                    for _, prod2 in products2_sample.iterrows():
                        # Calculate similarity
                        similarity = SequenceMatcher(
                            None,
                            str(prod1['name']).lower(),
                            str(prod2['name']).lower()
                        ).ratio()
                        
                        # Keep pairs with moderate to high similarity
                        # (0.5-0.95 range - these need human review)
                        if 0.5 <= similarity <= 0.95:
                            candidates.append({
                                'product1': prod1['name'],
                                'product2': prod2['name'],
                                'store1': store1,
                                'store2': store2,
                                'price1': prod1['price'],
                                'price2': prod2['price'],
                                'price_diff': abs(prod1['price'] - prod2['price']),
                                'similarity': similarity
                            })
                        
                        # Stop if we have enough candidates
                        if len(candidates) >= n_candidates * 2:
                            break
                    
                    if len(candidates) >= n_candidates * 2:
                        break
                
                if len(candidates) >= n_candidates * 2:
                    break
        
        # Convert to DataFrame
        candidates_df = pd.DataFrame(candidates)
        
        if len(candidates_df) == 0:
            print("No candidate pairs found. Try adjusting similarity thresholds.")
            return candidates_df
        
        # Remove duplicates
        candidates_df = candidates_df.drop_duplicates(subset=['product1', 'product2'])
        
        # Sort by similarity (descending)
        candidates_df = candidates_df.sort_values('similarity', ascending=False)
        
        # Take top N
        candidates_df = candidates_df.head(n_candidates)
        
        print(f"\nFound {len(candidates_df)} candidate pairs")
        print(f"  Similarity range: {candidates_df['similarity'].min():.2%} - {candidates_df['similarity'].max():.2%}")
        
        return candidates_df
    
    def analyze_candidate_quality(self, candidates_df):
        """
        Analyze the quality of candidate pairs
        """
        if len(candidates_df) == 0:
            return
        
        print("\n" + "="*70)
        print("CANDIDATE PAIR QUALITY")
        print("="*70 + "\n")
        
        # Similarity distribution
        print("Similarity distribution:")
        bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        for i in range(len(bins)-1):
            count = len(candidates_df[
                (candidates_df['similarity'] >= bins[i]) & 
                (candidates_df['similarity'] < bins[i+1])
            ])
            print(f"  {bins[i]:.1f}-{bins[i+1]:.1f}: {count} pairs")
        
        # Price difference analysis
        print(f"\nPrice difference:")
        print(f"  Min: Rs. {candidates_df['price_diff'].min():.2f}")
        print(f"  Average: Rs. {candidates_df['price_diff'].mean():.2f}")
        print(f"  Max: Rs. {candidates_df['price_diff'].max():.2f}")
        
        # Show some examples
        print("\nExample candidate pairs (High similarity):")
        for idx, row in candidates_df.head(5).iterrows():
            print(f"\n  Similarity: {row['similarity']:.2%}")
            print(f"  Product 1: {row['product1']} ({row['store1']}) - Rs. {row['price1']:.2f}")
            print(f"  Product 2: {row['product2']} ({row['store2']}) - Rs. {row['price2']:.2f}")
    
    def save_candidates(self, candidates_df, filename='candidate_pairs.csv'):
        """
        Save candidate pairs for manual labeling
        """
        if len(candidates_df) == 0:
            print("\nNo candidates to save")
            return None
        
        candidates_df.to_csv(filename, index=False)
        print(f"\nSaved {len(candidates_df)} candidate pairs to '{filename}'")
        print(f"  These will be used for manual labeling in the next step")
        
        return filename
    
    def generate_report(self):
        """
        Generate complete analysis report
        """
        print("\n" + "="*70)
        print("ANALYSIS SUMMARY")
        print("="*70 + "\n")
        
        print(f"Total products analyzed: {len(self.products_df)}")
        print(f"Stores: {self.products_df['store'].nunique()}")
        print(f"Unique product names: {self.products_df['name'].nunique()}")
        
        # Estimate matching potential
        duplicate_names = self.products_df[
            self.products_df.duplicated(subset=['name'], keep=False)
        ]
        exact_matches = len(duplicate_names) // 2
        
        print(f"\nEstimated matching potential:")
        print(f"  Exact name matches across stores: ~{exact_matches}")
        print(f"  Potential fuzzy matches: ~{len(self.products_df) * 0.3:.0f}")
        
        print("\nRECOMMENDATION:")
        print("  Aim to manually label 300-500 pairs for best results")
        print("  This will take approximately 1-2 hours")
        print("  You can do it in multiple sessions")


def main():
    """
    Main execution function
    """
    print("="*70)
    print("PRODUCT DATA ANALYSIS")
    print("="*70 + "\n")
    
    try:
        # Initialize analyzer
        analyzer = DataAnalyzer('all_products.csv')
        
        # Run all analyses
        analyzer.analyze_basic_stats()
        analyzer.analyze_word_patterns()
        
        # Find candidate pairs
        candidates_df = analyzer.find_potential_matches(n_candidates=1000)
        
        # Analyze candidate quality
        analyzer.analyze_candidate_quality(candidates_df)
        
        # Save candidates
        analyzer.save_candidates(candidates_df, 'candidate_pairs.csv')
        
        # Generate summary report
        analyzer.generate_report()
        
        print("\nANALYSIS COMPLETE!")
        print("\nNext step: Run manual_labeling_tool.py to start labeling")
        
    except FileNotFoundError:
        print("ERROR: all_products.csv not found!")
        print("Please run mongodb_extract.py first")
        return 1
    except Exception as e:
        print(f"ERROR: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())