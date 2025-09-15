# qdrant_manager.py
"""
Qdrant 資料庫管理模組 - 負責向量資料庫的所有操作
"""

import numpy as np
from typing import List, Dict, Any, Optional
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, PointStruct
from config import (
    QDRANT_HOST, QDRANT_PORT, COLLECTION_NAME, 
    DISTANCE_METRIC, BATCH_SIZE, DEFAULT_SEARCH_LIMIT,
    EMBEDDING_DIMENSION
)


class QdrantManager:
    """Qdrant 資料庫管理器"""
    
    def __init__(self, host: str = QDRANT_HOST, port: int = QDRANT_PORT):
        """
        初始化 Qdrant 管理器
        
        Args:
            host: Qdrant 主機位址
            port: Qdrant 端口
        """
        self.host = host
        self.port = port
        self.client = None
    
    def connect(self) -> None:
        """建立與 Qdrant 的連線"""
        print(f"連接到 Qdrant: {self.host}:{self.port}")
        self.client = QdrantClient(host=self.host, port=self.port)
        print("連線建立成功")
    
    def create_collection(self, 
                         collection_name: str = COLLECTION_NAME,
                         vector_size: int = EMBEDDING_DIMENSION,
                         distance: str = DISTANCE_METRIC) -> None:
        """
        建立向量集合
        
        Args:
            collection_name: 集合名稱
            vector_size: 向量維度
            distance: 距離計算方式
        """
        if self.client is None:
            self.connect()
        
        # 檢查集合是否存在
        collections = self.client.get_collections()
        existing_names = [col.name for col in collections.collections]
        
        if collection_name in existing_names:
            print(f"集合 '{collection_name}' 已存在，將刪除後重建")
            self.client.delete_collection(collection_name=collection_name)
        
        # 建立新集合
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=distance)
        )
        print(f"集合 '{collection_name}' 建立成功")
    
    def batch_upsert(self, 
                    embeddings: np.ndarray,
                    metadata: List[Dict[str, Any]],
                    collection_name: str = COLLECTION_NAME,
                    batch_size: int = BATCH_SIZE) -> None:
        """
        批次上傳向量資料
        
        Args:
            embeddings: 向量陣列
            metadata: 元資料列表
            collection_name: 集合名稱
            batch_size: 批次大小
        """
        if self.client is None:
            self.connect()
        
        total = len(embeddings)
        print(f"開始批次上傳 {total} 個向量，批次大小: {batch_size}")
        
        for start in tqdm(range(0, total, batch_size), desc="上傳批次"):
            end = min(start + batch_size, total)
            batch_embeddings = embeddings[start:end]
            batch_metadata = metadata[start:end]
            
            points = [
                PointStruct(
                    id=meta['MAL_ID'], 
                    vector=vec.tolist(), 
                    payload=meta
                )
                for vec, meta in zip(batch_embeddings, batch_metadata)
            ]
            
            self.client.upsert(collection_name=collection_name, points=points)
        
        print("批次上傳完成")
    
    def search_similar(self, 
                      mal_id: int,
                      collection_name: str = COLLECTION_NAME,
                      limit: int = DEFAULT_SEARCH_LIMIT) -> List[Dict[str, Any]]:
        """
        搜尋相似動漫
        
        Args:
            mal_id: 目標動漫的 MAL_ID
            collection_name: 集合名稱
            limit: 回傳結果數量
            
        Returns:
            相似動漫列表
        """
        if self.client is None:
            self.connect()
        
        # 確保 mal_id 是標準 Python int 類型
        mal_id = int(mal_id)
        
        # 取得目標動漫的向量
        search_result = self.client.retrieve(
            collection_name=collection_name,
            ids=[mal_id],
            with_payload=True,
            with_vectors=True
        )
        
        if not search_result:
            raise ValueError(f"MAL_ID {mal_id} 在集合中不存在")
        
        # 使用向量搜尋相似項目
        query_vector = search_result[0].vector
        similar_results = self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
        
        # 格式化結果
        results = []
        for r in similar_results:
            results.append({
                'MAL_ID': r.payload["MAL_ID"],
                'Name': r.payload.get("Name", ""),
                'Score': r.score
            })
        
        return results
    
    def get_collections(self) -> List[str]:
        """
        取得所有集合名稱
        
        Returns:
            集合名稱列表
        """
        if self.client is None:
            self.connect()
        
        collections = self.client.get_collections()
        return [col.name for col in collections.collections]
    
    def delete_collection(self, collection_name: str = COLLECTION_NAME) -> None:
        """
        刪除集合
        
        Args:
            collection_name: 集合名稱
        """
        if self.client is None:
            self.connect()
        
        self.client.delete_collection(collection_name=collection_name)
        print(f"集合 '{collection_name}' 已刪除")
    
    def get_collection_info(self, collection_name: str = COLLECTION_NAME) -> Dict[str, Any]:
        """
        取得集合資訊
        
        Args:
            collection_name: 集合名稱
            
        Returns:
            集合資訊
        """
        if self.client is None:
            self.connect()
        
        return self.client.get_collection(collection_name=collection_name)


if __name__ == "__main__":
    # 測試程式
    manager = QdrantManager()
    
    # 測試連線
    manager.connect()
    
    # 列出所有集合
    collections = manager.get_collections()
    print(f"現有集合: {collections}")
