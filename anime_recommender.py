# anime_recommender.py
"""
動漫推薦系統主程式 - 整合所有模組提供完整的推薦功能
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from data_processor import AnimeDataProcessor
from embedding_generator import EmbeddingGenerator
from qdrant_manager import QdrantManager
from config import COLLECTION_NAME, DEFAULT_SEARCH_LIMIT


class AnimeRecommender:
    """動漫推薦系統"""
    
    def __init__(self):
        """初始化推薦系統"""
        self.data_processor = AnimeDataProcessor()
        self.embedding_generator = EmbeddingGenerator()
        self.qdrant_manager = QdrantManager()
        self.data = None
        self.is_setup = False
    
    def setup_system(self, force_rebuild: bool = False) -> None:
        """
        設定推薦系統
        
        Args:
            force_rebuild: 是否強制重建資料庫
        """
        print("=== 動漫推薦系統設定 ===")
        
        # 1. 處理資料
        print("\n1. 處理動漫資料...")
        self.data = self.data_processor.get_processed_data()
        
        # 2. 生成向量
        print("\n2. 生成文本向量...")
        try:
            if force_rebuild:
                raise FileNotFoundError("強制重建")
            
            # 嘗試載入既有向量
            embeddings = self.embedding_generator.load_embeddings()
        except FileNotFoundError:
            # 重新生成向量
            texts = self.data_processor.get_synopsis_list()
            embeddings = self.embedding_generator.process_texts_to_embeddings(texts)
        
        # 3. 設定 Qdrant
        print("\n3. 設定向量資料庫...")
        self.qdrant_manager.connect()
        
        # 檢查集合是否存在
        collections = self.qdrant_manager.get_collections()
        if COLLECTION_NAME not in collections or force_rebuild:
            print("建立新的向量集合...")
            self.qdrant_manager.create_collection()
            
            # 上傳資料
            metadata = self.data_processor.get_metadata()
            self.qdrant_manager.batch_upsert(embeddings, metadata)
        else:
            print(f"使用既有集合: {COLLECTION_NAME}")
        
        self.is_setup = True
        print("\n=== 系統設定完成 ===")
    
    def recommend_by_mal_id(self, 
                           mal_id: int, 
                           limit: int = DEFAULT_SEARCH_LIMIT) -> List[Dict[str, Any]]:
        """
        根據 MAL_ID 取得推薦動漫
        
        Args:
            mal_id: 目標動漫的 MAL_ID
            limit: 推薦數量
            
        Returns:
            推薦動漫列表
        """
        if not self.is_setup:
            raise ValueError("請先設定系統")
        
        # 確保 mal_id 是標準 Python int 類型
        mal_id = int(mal_id)
        
        return self.qdrant_manager.search_similar(mal_id, limit=limit)
    
    def display_recommendations(self, recommendations: List[Dict[str, Any]]) -> None:
        """
        顯示推薦結果
        
        Args:
            recommendations: 推薦動漫列表
        """
        print(f"\n=== 推薦結果 (共 {len(recommendations)} 部) ===")
        for i, anime in enumerate(recommendations, 1):
            print(f"{i:2d}. {anime['Name']} (MAL_ID: {anime['MAL_ID']}) - 相似度: {anime['Score']:.4f}")
    
    def get_anime_info(self, mal_id: int) -> Optional[Dict[str, Any]]:
        """
        取得動漫詳細資訊
        
        Args:
            mal_id: MAL_ID
            
        Returns:
            動漫資訊字典
        """
        if self.data is None:
            raise ValueError("請先設定系統")
        
        anime_info = self.data[self.data.MAL_ID == mal_id]
        if anime_info.empty:
            return None
        
        return anime_info.iloc[0].to_dict()


def main():
    """主程式"""
    # 建立推薦系統
    recommender = AnimeRecommender()
    
    # 設定系統
    recommender.setup_system()
    
    # 示範推薦功能
    print("\n=== 示範：MAL_ID 223 (Dragon Ball) 推薦 ===")
    try:
        mal_id = 223  # Dragon Ball 的 MAL_ID
        recommendations = recommender.recommend_by_mal_id(mal_id, limit=10)
        recommender.display_recommendations(recommendations)
    except ValueError as e:
        print(f"錯誤: {e}")


if __name__ == "__main__":
    main()
