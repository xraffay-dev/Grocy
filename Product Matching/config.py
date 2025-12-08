"""
Configuration settings for the product matching system.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'Grocy')

# Store collection names
STORE_COLLECTIONS = [
    'Al-Fatah',
    'Jalal Sons',
    'Metro',
    'Rahim Store',
    'Raja Sahib'
]

# MinHash LSH Parameters
LSH_NUM_PERM = 128  # Number of permutations (balance between speed and accuracy)
LSH_THRESHOLD = 0.5  # Jaccard similarity threshold for candidate generation
N_GRAM_SIZE = 3  # Character-level n-gram size for tokenization

# Performance Settings
BATCH_SIZE = 1000  # Batch size for processing products
