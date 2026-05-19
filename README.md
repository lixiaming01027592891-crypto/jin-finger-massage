# 金手指按摩 - 24小時專業按摩養生會館 SEO 網站

![金手指按摩](public/images/og-image.jpg)

以 Astro 框架建構的高效能 SEO 優化靜態網站，專為「金手指按摩」品牌打造。

## 網站預覽

**線上預覽**: https://5clhdz5nsfr64.kimi.page

## 技術架構

| 技術 | 版本 |
|------|------|
| Astro | 4.16 |
| Tailwind CSS | 3.4 |
| React | 19 (用於互動組件) |
| TypeScript | 5.x |

## 頁面結構

| 頁面 | 路徑 | SEO 重點 |
|------|------|---------|
| 首頁 | `/` | Hero、服務介紹、顧客評價、FAQ |
| 服務項目 | `/services/` | 4大服務詳情、價目表、組合優惠 |
| 關於我們 | `/about/` | 品牌故事、里程碑、師傅團隊 |
| 環境展示 | `/environment/` | 環境照片、設施介紹、交通資訊 |
| 聯絡我們 | `/contact/` | 聯絡方式、營業時間、10題 FAQ |

## SEO 優化項目

- 每頁獨立 Title / Description / Keywords
- Schema.org LocalBusiness + WebSite 結構化資料
- Open Graph + Twitter Card 社群分享標籤
- 自動 Sitemap 生成
- Canonical URL
- 響應式手機版設計
- 法律免責聲明

## 推送到 GitHub

### 方式一：一鍵推送腳本（推薦）

```bash
cd /mnt/agents/output/app
python3 push-to-github.py
# 按照提示輸入 GitHub Token 即可
```

### 方式二：手動推送

```bash
# 1. 創建 GitHub 倉庫 (在網頁上操作)
# 2. 推送代碼
cd /mnt/agents/output/app
git remote add origin https://github.com/YOUR_USERNAME/jin-finger-massage.git
git branch -M master
git push -u origin master
```

### 方式三：使用 GitHub CLI

```bash
gh auth login
cd /mnt/agents/output/app
gh repo create jin-finger-massage --public --source=. --push
```

## GitHub Pages 部署

推送後，前往 `Settings > Pages` 啟用 GitHub Pages，或直接使用已設定的 GitHub Actions 自動部署。

## 本機開發

```bash
npm install
npm run dev
```

## 建置

```bash
npm run build
# 輸出到 dist/ 目錄
```

## 法律聲明

本網站僅供放鬆舒壓之保健養生服務，非醫療行為。效果因人而異。

---

金手指按摩 &copy; 2026 All Rights Reserved.
