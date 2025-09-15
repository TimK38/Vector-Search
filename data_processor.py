# data_processor.py
"""
資料處理模組 - 負責載入、清理和預處理動漫資料
"""

import pandas as pd
import numpy as np
from typing import Tuple
from config import DATA_PATH, MIN_SYNOPSIS_LENGTH, EXCLUDE_PATTERN


class AnimeDataProcessor:
    """動漫資料處理器"""
    
    def __init__(self, data_path: str = DATA_PATH):
        """
        初始化資料處理器
        
        Args:
            data_path: 資料檔案路徑
        """
        self.data_path = data_path
        self.data = None
    
    def load_data(self) -> pd.DataFrame:
        """
        載入動漫資料
        
        Returns:
            載入的 DataFrame
        """
        print(f"載入資料: {self.data_path}")
        self.data = pd.read_csv(self.data_path)
        print(f"原始資料筆數: {len(self.data)}")
        return self.data
    
    def calculate_synopsis_length(self) -> pd.DataFrame:
        """
        計算簡介長度
        
        Returns:
            添加簡介長度欄位的 DataFrame
        """
        if self.data is None:
            raise ValueError("請先載入資料")
        
        self.data['sypnopsis_length'] = self.data['sypnopsis'].apply(
            lambda x: len(str(x))
        )
        return self.data
    
    def filter_data(self, 
                   min_length: int = MIN_SYNOPSIS_LENGTH,
                   exclude_pattern: str = EXCLUDE_PATTERN) -> pd.DataFrame:
        """
        篩選高品質資料
        
        Args:
            min_length: 最小簡介長度
            exclude_pattern: 要排除的模式
            
        Returns:
            篩選後的 DataFrame
        """
        if self.data is None:
            raise ValueError("請先載入資料")
        
        # 篩選條件
        length_filter = self.data.sypnopsis_length > min_length
        pattern_filter = ~self.data.sypnopsis.str.contains(exclude_pattern, na=False)
        
        self.data = self.data[length_filter & pattern_filter]
        print(f"篩選後資料筆數: {len(self.data)}")
        return self.data
    
    def get_processed_data(self) -> pd.DataFrame:
        """
        執行完整的資料處理流程
        
        Returns:
            處理完成的 DataFrame
        """
        self.load_data()
        self.calculate_synopsis_length()
        self.filter_data()
        return self.data
    
    def get_synopsis_list(self) -> list:
        """
        取得簡介文本列表
        
        Returns:
            簡介文本列表
        """
        if self.data is None:
            raise ValueError("請先處理資料")
        
        return self.data.sypnopsis.tolist()
    
    def get_metadata(self) -> list:
        """
        取得 metadata
        
        Returns:
            包含 MAL_ID 和 Name 的字典列表
        """
        if self.data is None:
            raise ValueError("請先處理資料")
        
        return self.data[['MAL_ID', 'Name']].to_dict(orient="records")


if __name__ == "__main__":
    # 測試程式
    processor = AnimeDataProcessor()
    data = processor.get_processed_data()
    print(f"\n處理完成！最終資料形狀: {data.shape}")
    print(f"欄位: {list(data.columns)}")
