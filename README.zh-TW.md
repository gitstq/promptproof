[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# PromptProof

> 先打樣，再花錢。把 AI 影片提示詞整理成清單，算清成本，只給過關的鏡頭付成片的錢。

## 🎉 專案介紹

AI 影片生成是按秒計費的，但多數人的做法是：腦中冒出一個想法，寫一段文字，
直接用最高解析度生成，不滿意再來一次。錢就燒在那些「其實看一眼低解析打樣
就能否決」的鏡頭上。

PromptProof 是一個完全在本機運作的小工具，站在生成工具的前面，幫你做三件事：
把提示詞從「一段話」拆成主體、動作、鏡頭、風格分開的結構化鏡頭；把一整批鏡頭
先驗證、去重，再排成「全部 768P 打樣 → 人工確認 → 只有過關的才出成片」的
兩階段清單；在真正動手之前，先算好這批工作要花多少錢。

它的靈感來自真實的圖生影片工作方式——先低成本驗片，再付費成片——但它不綁定
任何一家生成服務，也不呼叫任何 API。無論你用 ComfyUI、網頁版工具或任何平台，
它只負責生成之前的那一步。**差異化亮點：零相依套件、完全離線、單價可自訂、
省多少錢算誠實帳（全部過關時打樣就是額外的品檢成本，不粉飾）。**

## ✨ 核心特性

- 🧩 **結構化鏡頭**：主體／動作／鏡頭／風格／首幀圖／反向詞分欄位寫，缺哪項一眼就看到
- ✅ **批次驗證**：主體空白、動作空白、時長超限、解析度寫錯，一條指令全部列出
- 🧹 **自動去重**：依創意內容指紋判重，同內容只換時長也算重複，不重複花錢
- 💰 **成本預估**：依每秒單價表估算，單價用你自己服務的真實價格，改一個 JSON 即可
- 🎬 **兩階段計畫**：先全部打樣、只給核准的鏡頭出成片，並算出與全部直出相比的差額
- 📋 **清單匯出**：Markdown 核取清單（提示詞可直接複製）或 CSV，方便排工與對帳
- 🔒 **完全離線**：不連網、不上傳，未發表的創意不離開你的電腦

## 🚀 快速開始

環境需求：Python 3.10 或以上，Windows／macOS／Linux 皆可，無需安裝任何相依套件。

```bash
# 1. 取得程式碼（發布到 GitHub 後可用 git clone；本機使用直接進入目錄即可）
cd promptproof

# 2. 驗證範例鏡頭檔案
python -m promptproof validate examples/shots.json

# 3. 產生兩階段計畫：只核准 cat-desk 出成片
python -m promptproof plan examples/shots.json --approve cat-desk --rates examples/rates.json --out plan.md

# 4. 打開 plan.md，照清單先跑打樣、確認後再跑成片
```

可選：安裝成系統指令：

```bash
pip install .
promptproof validate examples/shots.json
```

## 📖 詳細使用指南

### 鏡頭檔案格式（JSON）

```json
[
  {
    "id": "cat-desk",
    "subject": "an orange cat sitting at a small wooden desk",
    "action": "turns its head towards the camera and blinks slowly",
    "camera": "slow push-in, medium shot",
    "style": "warm natural light, cinematic",
    "source_image": "cat_first_frame.png",
    "negative": "no text, no watermark",
    "duration_sec": 5,
    "final_resolution": "2K"
  }
]
```

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | 是 | 鏡頭編號，核准成片時用它點名 |
| `subject` / `action` | 是 | 主體與動作，空白會被驗證攔下 |
| `camera` / `style` | 否 | 鏡頭運動與風格，camera 預設為 static |
| `source_image` | 否 | 圖生影片的首幀圖檔名 |
| `negative` | 否 | 不希望出現的元素 |
| `duration_sec` | 否 | 時長（秒），1–15，預設 5 |
| `final_resolution` | 否 | 成片解析度：768P／1080P／2K，預設 2K |

### 三條指令

```bash
# 驗證：有問題時結束碼為 1，適合放在腳本最前面把關
python -m promptproof validate my_shots.json

# 只看單一鏡頭組好的提示詞，可直接複製到生成工具
python -m promptproof prompt my_shots.json cat-desk

# 匯出 CSV 清單（--format csv），或不加 --out 直接印在畫面上
python -m promptproof plan my_shots.json --approve cat-desk,harbour-dawn --format csv
```

### 單價設定

複製 `examples/rates.json`，改成你實際使用的服務每秒價格（單位自訂，全表統一即可）：

```json
{ "768P": 0.20, "1080P": 0.40, "2K": 0.80 }
```

> 倉庫裡的數字只是算例，不代表任何服務商的真實報價，務必改成你自己的。

### 典型場景

1. **批次圖生影片**：把一週要做的 20 個鏡頭寫成一個 JSON，先驗證去重，
   打樣總價一目了然，否決一半後成片費直接省下來。
2. **接案對帳**：CSV 清單就是報價依據，打樣花多少、成片花多少，清清楚楚。
3. **提示詞沉澱**：結構化鏡頭檔本身就是可重用的資產庫，比在聊天紀錄裡翻一段話可靠。

_運行截圖／示範動圖：待補（在本機執行 `plan` 指令的終端輸出即為清單效果）。_

## 💡 設計思路與迭代規劃

設計上只堅持三條：**零相依套件**（標準函式庫能做完的事絕不引包，工具活得比
相依套件長）、**先算帳再執行**（任何要花錢的批次工作，都應該先有一張看得懂的
清單）、**不綁服務商**（單價、解析度全是設定，今天用 A 家明天換 B 家，工具不用改）。

後續迭代計畫：

- [ ] 支援從 CSV 表格匯入鏡頭（許多創作者習慣用表格排片）
- [ ] 把核准狀態寫回鏡頭檔，形成可追溯的驗片紀錄
- [ ] 匯出 ComfyUI 工作流可讀的批次說明檔
- [ ] 多幣別與預算上限提醒（超預算時驗證直接示警）

社群貢獻方向：新的匯出格式、更多驗證規則、真實使用場景的範例鏡頭庫。

## 📦 打包與部署指南

本專案是**工具／腳本類專案**，無需打包執行檔，也沒有 Release 附件，依下列方式整合即可：

- **直接執行**：複製目錄後 `python -m promptproof ...`，適合臨時使用。
- **安裝為指令**：在專案根目錄 `pip install .`，之後任何目錄都能用 `promptproof` 指令；
  移除用 `pip uninstall promptproof`。
- **嵌入自己的腳本**：

```python
from promptproof.models import load_shots
from promptproof.planner import build_plan, to_markdown_checklist

shots = load_shots("my_shots.json")
plan = build_plan(shots, approved_ids={"cat-desk"})
print(plan.total_cost, to_markdown_checklist(plan))
```

- **相容環境**：Python 3.10+，Windows／macOS／Linux；不需要網路，可在離線機器上執行。
- **常見問題**：出現 `no rate configured` 是單價表缺了該解析度，補上即可；
  出現重複鏡頭不是錯誤，而是同一個創意寫了兩遍，刪掉一條或改動創意欄位即可。

## 🤝 貢獻指南

歡迎 Issue 與 PR，細則見 [CONTRIBUTING.md](CONTRIBUTING.md)。簡單說：先開 Issue
說明問題或想法；PR 保持改動單一、附帶測試；提交訊息使用 `feat:`／`fix:`／`docs:`
等前綴。提交前請跑通 `python -m unittest discover -s tests -v`。

## 📄 開源協議說明

本專案採用 MIT 授權條款開源，見 [LICENSE](LICENSE)。你可以自由使用、複製、修改與
散布，包括商業用途，只需保留版權與授權聲明；軟體依「現狀」提供，不附帶任何擔保。
