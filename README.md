# 動漫推薦向量搜尋系統

使用 Qdrant 向量資料庫建立的智能動漫推薦系統。透過分析動漫劇情簡介的語義相似度，為用戶推薦相似的動漫作品。

## 💡 為什麼分享這個專案？

### 向量搜尋的實務價值

在現今講求即時回應的數位時代，**向量搜尋技術已成為提升用戶體驗的關鍵**。傳統的搜尋方法在面對大規模資料時，往往無法滿足即時查詢的需求。根據實際經驗，**向量搜尋可以有效減少 99% 以上不必要的比對資源**，大幅提升查詢效率。

當業務場景需要即時回應以確保優質用戶體驗時，向量搜尋不再是選項，而是必需品。這項技術能夠：
- 🚀 **加速查找任務**：將搜尋時間從秒級縮短到毫秒級
- 💰 **降低運算成本**：減少 99% 以上的無效比對運算
- 🎯 **提升搜尋準確度**：基於語義理解的智能匹配

### 技術選型的實戰考量

在開發這個系統時，我實際測試了多個向量資料庫解決方案：

| 評估項目 | ChromaDB | MongoDB Atlas | **Qdrant** |
|---------|----------|---------------|-------------|
| 🔒 **資料隱私安全** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 🔧 **後續維護性** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| ⚡ **查詢速度** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 🎯 **搜尋正確性** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 💵 **總體成本** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**最終選擇 Qdrant 的核心原因**：
- ✅ **資料隱私**：可完全本地部署，資料不外流
- ✅ **維護簡單**：Docker 容器化部署，運維成本低
- ✅ **效能優異**：專為向量搜尋優化，速度表現卓越
- ✅ **準確度高**：先進的相似度計算算法
- ✅ **成本友善**：開源免費，無額外授權費用

### 分享的目的

希望透過這個實際案例，讓更多開發者了解：
1. **向量搜尋的實務應用價值**
2. **如何選擇適合的技術方案**
3. **Qdrant 在生產環境的實戰經驗**

這不僅是一個技術分享，更是一次實戰經驗的傳承。

## 🎯 系統功能

- **智能推薦**：根據劇情內容推薦相似動漫
- **語義理解**：不只比對關鍵字，更理解劇情含義  
- **快速搜尋**：毫秒級搜尋響應
- **大規模支援**：可處理萬部以上動漫資料

## 📊 系統流程

```
動漫資料 → 文本清理 → 向量轉換 → 資料庫儲存 → 相似度搜尋 → 推薦結果
```

## 📋 資料說明

<div align="center">
  <img src="動漫示意圖.jpg" alt="動漫角色集合" width="600">
  <p><i>涵蓋各種經典動漫角色的豐富資料集</i></p>
</div>

**資料來源**：MyAnimeList 動漫資料庫  
**資料規模**：11,722 部動漫作品  
**主要欄位**：
- **MAL_ID**：唯一識別碼
- **Name**：動漫名稱
- **Score**：評分
- **Genres**：類型標籤
- **Synopsis**：劇情簡介（推薦核心依據）

**資料品質**：已篩選出簡介完整且字數超過 100 字的高品質資料

## 🎬 推薦效果展示

**搜尋範例**：七龍珠 (Dragon Ball)

**推薦結果**：
1. Dragon Ball Kai (相似度: 79%)
2. Dragon Ball Z (相似度: 78%)  
3. Dragon Ball Super Movie: Broly (相似度: 67%)
4. Dragon Ball GT (相似度: 66%)
5. Dragon Ball Super (相似度: 64%)
6. 其他相似武俠冒險動漫...

**推薦品質**：系統成功識別同系列作品及具有相似劇情元素的動漫

## 🔧 實作步驟

### 步驟 1：資料準備
- 載入動漫資料集
- 清理無效資料（簡介過短或缺失）
- 篩選出高品質的劇情描述

### 步驟 2：文本向量化
**採用方法**：Sentence Transformers (all-mpnet-base-v2)
- **向量維度**：768 維
- **語言支援**：多語言
- **特色**：專為語義相似度搜尋優化

**其他可選方案**：
- **OpenAI Embeddings**：效果優秀，需 API 費用
- **Google Vertex AI**：企業級方案，需 GCP 帳號  
- **Hugging Face**：開源多樣，需手動調整

**方案選擇建議**：
- 🆓 **免費方案**：Sentence Transformers
- 💼 **商業應用**：OpenAI Embeddings
- 🏢 **企業級**：Google Vertex AI

### 步驟 3：建立向量資料庫
- 連接 Qdrant 資料庫
- 建立動漫向量集合（Collection）
- 批次上傳向量資料與 metadata

### 步驟 4：實現搜尋功能
- 根據輸入動漫 ID 取得對應向量
- 計算與資料庫中所有向量的相似度
- 排序並返回最相似的推薦結果

## 🐳 Qdrant 安裝設定

### 安裝步驟

1. **安裝 Docker Desktop**
   - 前往 [Docker 官網](https://www.docker.com/products/docker-desktop/) 下載
   - 選擇對應作業系統版本安裝
   - 啟動 Docker Desktop 應用程式

2. **驗證安裝**
   ```bash
   docker --version
   ```

3. **啟動 Qdrant（推薦方式）**
   ```bash
   # 背景執行，資料持久化
   docker run -d -p 6333:6333 \
     -v $(pwd)/qdrant_storage:/qdrant/storage \
     --name qdrant-server \
     qdrant/qdrant
   ```

4. **驗證服務**
   - 瀏覽器開啟：http://localhost:6333/dashboard
   - 檢查容器狀態：`docker ps`

### 常用管理命令

```bash
# 檢查容器狀態
docker ps

# 停止/重啟容器
docker stop qdrant-server
docker start qdrant-server

# 查看日誌
docker logs qdrant-server
```

### 故障排除

- **端口被佔用**：使用 `lsof -i :6333` 檢查，或改用其他端口
- **容器無法啟動**：使用 `docker logs qdrant-server` 查看錯誤
- **Docker 命令找不到**：確保 Docker Desktop 正在運行

## 🔍 搜尋原理說明

### 相似度計算
- **向量表示**：每部動漫簡介轉換為 768 維向量
- **餘弦相似度**：計算向量間夾角，範圍 0-1（1=完全相同）
- **搜尋流程**：輸入動漫 → 取得向量 → 計算相似度 → 排序推薦

### 推薦品質關鍵
1. **文本品質**：劇情簡介完整性
2. **模型能力**：語義理解深度
3. **相似度閾值**：推薦精準度控制
4. **多樣性平衡**：避免過度相似

### 系統優勢
- 🧠 **語義理解**：理解劇情含義，非僅關鍵字比對
- ⚡ **快速搜尋**：毫秒級響應速度
- 📈 **可擴展**：支援大規模資料集
- 🎯 **個性化**：可調整推薦權重

## 🚀 開始使用

### 環境準備

1. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

2. **啟動 Qdrant 容器**
   ```bash
   docker run -d -p 6333:6333 \
     -v $(pwd)/qdrant_storage:/qdrant/storage \
     --name qdrant-server \
     qdrant/qdrant
   ```

### 快速開始

#### 方法一：使用範例腳本
```bash
# 基本使用示範
python example_usage.py

# 完整功能示範  
python demo_script.py

# 主程式執行
python anime_recommender.py
```

#### 方法二：程式化使用
```python
from anime_recommender import AnimeRecommender

# 建立推薦系統
recommender = AnimeRecommender()
recommender.setup_system()

# 根據 MAL_ID 取得推薦 (223 = Dragon Ball)
recommendations = recommender.recommend_by_mal_id(223, limit=10)
recommender.display_recommendations(recommendations)
```

#### 方法三：互動式體驗
```bash
python demo_script.py
# 選擇選項 2 進入互動模式
```

### 常用 MAL_ID 參考

| MAL_ID | 動漫名稱 | 類型 |
|--------|----------|------|
| 223 | Dragon Ball | 冒險、武術 |
| 20 | Naruto | 動作、冒險 |
| 21 | One Piece | 動作、冒險 |
| 235 | Detective Conan | 冒險、推理、喜劇、警察 |

