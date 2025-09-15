# config.py
"""
配置檔案 - 集中管理所有設定參數
"""

# 資料路徑設定
DATA_PATH = "data/anime_with_synopsis.csv"
EMBEDDINGS_PATH = "data/anime_description_embeddings.npy"

# 模型設定
EMBEDDING_MODEL = "all-mpnet-base-v2"
EMBEDDING_DIMENSION = 768

# 資料處理設定
MIN_SYNOPSIS_LENGTH = 100
EXCLUDE_PATTERN = "No synopsis information has been"

# Qdrant 設定
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "anime_description_collection"
DISTANCE_METRIC = "Cosine"

# 批次處理設定
BATCH_SIZE = 100
DEFAULT_SEARCH_LIMIT = 10
