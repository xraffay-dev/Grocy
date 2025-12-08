"""
Semantic matching system using Sentence Transformers and FAISS.
Matches same products in different sizes with brand verification.
"""
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Tuple
import time
from preprocessing import extract_product_attributes, extract_size_info, fuzzy_brand_match


class SemanticMatcher:
    """
    Semantic matching using Sentence Transformers and FAISS.
    Identifies same products in different sizes.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize semantic matcher.
        
        Args:
            model_name: Sentence Transformer model name
        """
        print(f"Loading Sentence Transformer model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        self.index = None
        self.products = {}
        self.product_ids = []
        self.embeddings = None
        
        print(f"Model loaded. Embedding dimension: {self.dimension}")
    
    def create_size_agnostic_name(self, product_name: str) -> str:
        """
        Remove size information from product name for semantic matching.
        
        Args:
            product_name: Product name string
            
        Returns:
            Product name without size
        """
        size_info = extract_size_info(product_name)
        return size_info['name_without_size']
    
    def generate_embeddings(self, products: List[Dict]) -> np.ndarray:
        """
        Generate embeddings for all products.
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Numpy array of embeddings
        """
        print(f"\nGenerating embeddings for {len(products)} products...")
        start_time = time.time()
        
        size_agnostic_names = []
        for product in products:
            name = self.create_size_agnostic_name(product['productName'])
            size_agnostic_names.append(name)
        
        embeddings = self.model.encode(
            size_agnostic_names,
            show_progress_bar=True,
            batch_size=32
        )
        
        elapsed_time = time.time() - start_time
        print(f"Embeddings generated in {elapsed_time:.2f} seconds")
        print(f"  Average: {elapsed_time/len(products)*1000:.2f} ms per product")
        
        return embeddings
    
    def build_faiss_index(self, products: List[Dict]) -> None:
        """
        Build FAISS index for fast similarity search.
        
        Args:
            products: List of product dictionaries
        """
        print(f"\nBuilding FAISS index...")
        start_time = time.time()
        
        self.products = {p['productID']: p for p in products}
        self.product_ids = [p['productID'] for p in products]
        
        self.embeddings = self.generate_embeddings(products)
        
        faiss.normalize_L2(self.embeddings)
        
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(self.embeddings)
        
        elapsed_time = time.time() - start_time
        print(f"FAISS index built in {elapsed_time:.2f} seconds")
        print(f"  Index size: {self.index.ntotal} vectors")
    
    def find_similar_products(self, product_id: str, k: int = 50, 
                             min_similarity: float = 0.85) -> List[Tuple[str, float]]:
        """
        Find similar products using FAISS.
        
        Args:
            product_id: Product ID to query
            k: Number of candidates to return
            min_similarity: Minimum cosine similarity threshold
            
        Returns:
            List of (product_id, similarity_score) tuples
        """
        if product_id not in self.products:
            return []
        
        product_idx = self.product_ids.index(product_id)
        
        query_embedding = self.embeddings[product_idx:product_idx+1]
        
        distances, indices = self.index.search(query_embedding, k + 1)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            candidate_id = self.product_ids[idx]
            
            if candidate_id == product_id:
                continue
            
            if distance >= min_similarity:
                results.append((candidate_id, float(distance)))
        
        return results
    
    def verify_brand_match(self, product1: Dict, product2: Dict) -> bool:
        """
        Verify that two products have the same brand.
        
        Args:
            product1: First product dictionary
            product2: Second product dictionary
            
        Returns:
            True if brands match, False otherwise
        """
        attrs1 = extract_product_attributes(product1['productName'])
        attrs2 = extract_product_attributes(product2['productName'])
        
        return fuzzy_brand_match(attrs1['brand'], attrs2['brand'])
    
    def calculate_confidence(self, product1: Dict, product2: Dict, 
                           similarity_score: float) -> float:
        """
        Calculate confidence score for a match.
        
        Args:
            product1: First product dictionary
            product2: Second product dictionary
            similarity_score: Cosine similarity score
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        attrs1 = extract_product_attributes(product1['productName'])
        attrs2 = extract_product_attributes(product2['productName'])
        
        if attrs1['size'] == attrs2['size'] and attrs1['unit'] == attrs2['unit']:
            return similarity_score
        else:
            return similarity_score * 0.95
    
    def get_semantic_matches(self, product_id: str, k: int = 50, 
                            min_similarity: float = 0.85) -> List[Dict]:
        """
        Get semantic matches for a product with brand verification.
        
        Args:
            product_id: Product ID to query
            k: Number of candidates to consider
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of match dictionaries with confidence scores
        """
        if product_id not in self.products:
            return []
        
        product = self.products[product_id]
        
        similar_products = self.find_similar_products(product_id, k, min_similarity)
        
        matches = []
        for candidate_id, similarity in similar_products:
            candidate = self.products[candidate_id]
            
            if not self.verify_brand_match(product, candidate):
                continue
            
            confidence = self.calculate_confidence(product, candidate, similarity)
            
            matches.append({
                'product': candidate,
                'similarity': similarity,
                'confidence': confidence
            })
        
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        
        return matches
    
    def get_statistics(self) -> Dict:
        """
        Get semantic matching statistics.
        
        Returns:
            Dictionary with statistics
        """
        if not self.products:
            return {}
        
        total_products = len(self.products)
        
        products_with_matches = 0
        total_matches = 0
        
        for product_id in list(self.products.keys())[:100]:
            matches = self.get_semantic_matches(product_id, k=20, min_similarity=0.85)
            if matches:
                products_with_matches += 1
                total_matches += len(matches)
        
        sample_size = min(100, total_products)
        estimated_coverage = (products_with_matches / sample_size * 100) if sample_size > 0 else 0
        avg_matches = total_matches / products_with_matches if products_with_matches > 0 else 0
        
        return {
            'total_products': total_products,
            'estimated_coverage': estimated_coverage,
            'avg_matches_per_product': avg_matches,
            'sample_size': sample_size
        }


if __name__ == "__main__":
    sample_products = [
        {
            'productID': '1',
            'productName': 'National Banana Jelly 80gm',
            'availableAt': 'Rahim Store',
            'originalPrice': 170
        },
        {
            'productID': '2',
            'productName': 'National Banana Jelly 160gm',
            'availableAt': 'Metro',
            'originalPrice': 320
        },
        {
            'productID': '3',
            'productName': 'National Strawberry Jelly 80gm',
            'availableAt': 'Al-Fatah',
            'originalPrice': 175
        },
        {
            'productID': '4',
            'productName': 'Nestle KitKat 500ml',
            'availableAt': 'Raja Sahib',
            'originalPrice': 200
        }
    ]
    
    matcher = SemanticMatcher()
    
    matcher.build_faiss_index(sample_products)
    
    print("\nSemantic matches for 'National Banana Jelly 80gm':")
    matches = matcher.get_semantic_matches('1', k=10)
    for match in matches:
        print(f"  - {match['product']['productName']} at {match['product']['availableAt']}")
        print(f"    Similarity: {match['similarity']:.3f}, Confidence: {match['confidence']:.3f}")
