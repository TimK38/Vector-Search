# demo_script.py
"""
示範腳本 - 展示如何使用動漫推薦系統
"""

from anime_recommender import AnimeRecommender


def demo_basic_usage():
    """基本使用示範"""
    print("=== 基本使用示範 ===")
    
    # 建立推薦系統
    recommender = AnimeRecommender()
    
    # 設定系統 (首次執行會需要較長時間)
    recommender.setup_system()
    
    # 示範: 根據 MAL_ID 推薦
    print("\n【示範】根據 MAL_ID 推薦:")
    
    # 測試多個熱門動漫的 MAL_ID
    test_anime = [
        (223, "Dragon Ball"),
        (813, "Dragon Ball Z"), 
        (1, "Cowboy Bebop"),
        (6, "Trigun")
    ]
    
    for mal_id, name in test_anime:
        print(f"\n--- {name} (MAL_ID: {mal_id}) 的推薦 ---")
        try:
            recommendations = recommender.recommend_by_mal_id(mal_id, limit=5)
            recommender.display_recommendations(recommendations)
        except ValueError as e:
            print(f"錯誤: {e}")


def demo_interactive():
    """互動式示範"""
    print("=== 互動式推薦系統 ===")
    
    recommender = AnimeRecommender()
    recommender.setup_system()
    
    while True:
        print("\n請選擇操作:")
        print("1. 根據 MAL_ID 搜尋推薦")
        print("2. 查看動漫詳細資訊")
        print("3. 退出")
        
        choice = input("請輸入選項 (1-3): ").strip()
        
        if choice == "1":
            try:
                mal_id = int(input("請輸入 MAL_ID: ").strip())
                limit = int(input("推薦數量 (預設 10): ") or 10)
                
                recommendations = recommender.recommend_by_mal_id(mal_id, limit)
                recommender.display_recommendations(recommendations)
            except (ValueError, TypeError) as e:
                print(f"錯誤: {e}")
        
        elif choice == "2":
            try:
                mal_id = int(input("請輸入 MAL_ID: ").strip())
                anime_info = recommender.get_anime_info(mal_id)
                
                if anime_info:
                    print(f"\n=== {anime_info['Name']} ===")
                    print(f"MAL_ID: {anime_info['MAL_ID']}")
                    print(f"評分: {anime_info['Score']}")
                    print(f"類型: {anime_info['Genres']}")
                    print(f"簡介長度: {anime_info['sypnopsis_length']} 字")
                    print(f"簡介: {anime_info['sypnopsis'][:200]}...")
                else:
                    print("找不到該動漫")
            except (ValueError, TypeError) as e:
                print(f"錯誤: {e}")
        
        elif choice == "3":
            print("感謝使用！")
            break
        
        else:
            print("無效選項，請重新選擇")


def demo_batch_search():
    """批次搜尋示範"""
    print("=== 批次搜尋示範 ===")
    
    recommender = AnimeRecommender()
    recommender.setup_system()
    
    # 預設的熱門動漫 MAL_ID
    popular_anime = [
        (223, "Dragon Ball"),
        (813, "Dragon Ball Z"),
        (1, "Cowboy Bebop"),
        (6, "Trigun"),
        (8, "Bouken Ou Beet")
    ]
    
    for mal_id, anime_name in popular_anime:
        print(f"\n--- {anime_name} (MAL_ID: {mal_id}) 的推薦 ---")
        try:
            recommendations = recommender.recommend_by_mal_id(mal_id, limit=4)
            for i, rec in enumerate(recommendations[1:], 1):  # 跳過自己
                print(f"{i}. {rec['Name']} (相似度: {rec['Score']:.3f})")
        except ValueError as e:
            print(f"錯誤: {e}")


if __name__ == "__main__":
    print("動漫推薦系統示範")
    print("請選擇示範模式:")
    print("1. 基本使用示範")
    print("2. 互動式示範") 
    print("3. 批次搜尋示範")
    
    mode = input("請選擇 (1-3): ").strip()
    
    if mode == "1":
        demo_basic_usage()
    elif mode == "2":
        demo_interactive()
    elif mode == "3":
        demo_batch_search()
    else:
        print("使用基本示範模式")
        demo_basic_usage()
