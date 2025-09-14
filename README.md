# 動漫推薦向量搜尋系統

使用 Qdrant 向量資料庫建立的智能動漫推薦系統。透過分析動漫劇情簡介的語義相似度，為用戶推薦相似的動漫作品。

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

1. **啟動系統**：確保 Qdrant 容器運行中
2. **執行程式**：運行 `generate_embedding.ipynb`
3. **體驗搜尋**：輸入喜愛動漫，獲得智能推薦

### 進階應用
- **混合搜尋**：結合向量搜尋與條件篩選
- **多模態整合**：支援文字、圖片等多種資料
- **即時更新**：動態新增或更新動漫資料庫
