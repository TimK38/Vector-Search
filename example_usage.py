# example_usage.py
"""
簡單使用範例 - 展示如何使用 MAL_ID 進行動漫推薦
"""

from anime_recommender import AnimeRecommender

def main():
    """主要範例程式"""
    print("=== 動漫推薦系統使用範例 ===")
    
    # 1. 建立推薦系統實例
    recommender = AnimeRecommender()
    
    # 2. 設定系統 (首次執行需要時間載入資料和模型)
    print("正在設定系統...")
    recommender.setup_system()
    
    # 3. 使用 MAL_ID 進行推薦
    print("\n=== 推薦範例 ===")
    
    # Dragon Ball 的 MAL_ID 是 223
    mal_id = 223
    limit = 10  # 推薦 10 部相似動漫
    
    try:
        print(f"搜尋與 MAL_ID {mal_id} 相似的動漫...")
        recommendations = recommender.recommend_by_mal_id(mal_id, limit=limit)
        
        print(f"\n找到 {len(recommendations)} 部相似動漫:")
        recommender.display_recommendations(recommendations)
        
    except ValueError as e:
        print(f"發生錯誤: {e}")
    
    # 4. 查看動漫詳細資訊
    print(f"\n=== MAL_ID {mal_id} 的詳細資訊 ===")
    try:
        anime_info = recommender.get_anime_info(mal_id)
        if anime_info:
            print(f"名稱: {anime_info['Name']}")
            print(f"評分: {anime_info['Score']}")
            print(f"類型: {anime_info['Genres']}")
            print(f"簡介: {anime_info['sypnopsis'][:200]}...")
        else:
            print("找不到該動漫的詳細資訊")
    except Exception as e:
        print(f"查詢資訊時發生錯誤: {e}")


if __name__ == "__main__":
    main()
