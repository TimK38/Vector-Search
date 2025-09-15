# embedding_generator.py
"""
向量生成模組 - 負責將文本轉換為向量表示
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Optional
from config import EMBEDDING_MODEL, EMBEDDINGS_PATH, EMBEDDING_DIMENSION


class EmbeddingGenerator:
    """文本向量生成器"""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        """
        初始化向量生成器
        
        Args:
            model_name: 預訓練模型名稱
        """
        self.model_name = model_name
        self.model = None
        self.embeddings = None
    
    def load_model(self) -> None:
        """載入預訓練模型"""
        print(f"載入模型: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print("模型載入完成")
    
    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        生成文本向量
        
        Args:
            texts: 文本列表
            
        Returns:
            向量陣列
        """
        if self.model is None:
            self.load_model()
        
        print(f"開始生成 {len(texts)} 個文本的向量...")
        self.embeddings = self.model.encode(texts, show_progress_bar=True)
        print(f"向量生成完成，形狀: {self.embeddings.shape}")
        
        return self.embeddings
    
    def save_embeddings(self, file_path: str = EMBEDDINGS_PATH) -> None:
        """
        儲存向量到檔案
        
        Args:
            file_path: 儲存路徑
        """
        if self.embeddings is None:
            raise ValueError("請先生成向量")
        
        np.save(file_path, self.embeddings)
        print(f"向量已儲存至: {file_path}")
    
    def load_embeddings(self, file_path: str = EMBEDDINGS_PATH) -> np.ndarray:
        """
        從檔案載入向量
        
        Args:
            file_path: 檔案路徑
            
        Returns:
            向量陣列
        """
        print(f"載入向量: {file_path}")
        self.embeddings = np.load(file_path)
        print(f"向量載入完成，形狀: {self.embeddings.shape}")
        return self.embeddings
    
    def get_embeddings(self) -> Optional[np.ndarray]:
        """
        取得當前的向量
        
        Returns:
            向量陣列或 None
        """
        return self.embeddings
    
    def process_texts_to_embeddings(self, texts: List[str], 
                                   save_path: str = EMBEDDINGS_PATH) -> np.ndarray:
        """
        完整的文本向量化流程
        
        Args:
            texts: 文本列表
            save_path: 儲存路徑
            
        Returns:
            向量陣列
        """
        embeddings = self.generate_embeddings(texts)
        self.save_embeddings(save_path)
        return embeddings


if __name__ == "__main__":
    # 測試程式
    generator = EmbeddingGenerator()
    
    # 測試文本
    test_texts = [
        "This is a test sentence for embedding generation.",
        "Another test sentence to verify the functionality."
    ]
    
    embeddings = generator.process_texts_to_embeddings(test_texts, "test_embeddings.npy")
    print(f"測試完成！向量形狀: {embeddings.shape}")
