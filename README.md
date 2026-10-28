[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md)

# PromptProof

> 先打样，再花钱。把 AI 视频提示词整理成清单，算清成本，只给通过的镜头付成片的钱。

## 🎉 项目介绍

AI 视频生成是按秒收费的，可大多数人干活的方式是：脑子里冒一个想法，写一段话，
直接用最高分辨率生成，不满意再来一遍。钱就烧在「其实看一眼低清打样就能否掉」
的镜头上。

PromptProof 是一个完全在本地运行的小工具，它站在生成工具的前面，帮你做三件事：
把提示词从「一段话」变成主体、动作、镜头、风格分开的结构化镜头；把一批镜头先
校验、去重，再排成「全部 768P 打样 → 人工确认 → 只有通过的才出成片」的两阶段
清单；动手之前先把这批活儿要花多少钱算出来。

它的灵感来自真实的图生视频工作方式——先低成本验片、再付费成片——但它不绑定任何
一家生成服务，也不调用任何 API，你用 ComfyUI、用网页版工具、用什么都行，它只
负责生成之前的那一步。**差异化亮点：零依赖、完全离线、单价可配置、省多少钱算诚
实账（全部通过时打样就是额外质检成本，不粉饰）。**

## ✨ 核心特性

- 🧩 **结构化镜头**：主体 / 动作 / 镜头 / 风格 / 首帧图 / 反向词分字段写，缺哪项一眼看到
- ✅ **批量校验**：空主体、空动作、时长越界、分辨率写错，一条命令全列出来
- 🧹 **自动去重**：按创意内容指纹判重，同内容换个时长也算重复，不重复花钱
- 💰 **成本预估**：按秒单价表估算，单价是你自己服务的真实价格，改一个 JSON 就行
- 🎬 **两阶段计划**：先全部打样、只给批准的镜头出成片，并给出与全部直出相比的差额
- 📋 **清单导出**：Markdown 复选框清单（提示词可直接复制）或 CSV，方便排活儿和对账
- 🔒 **完全离线**：不联网、不上传，未发布的创意不出你的电脑

## 🚀 快速开始

环境要求：Python 3.10 或更高版本，Windows / macOS / Linux 均可，无需安装任何依赖。

```bash
# 1. 拿到代码（发布到 GitHub 后可用 git clone；本地使用直接进目录即可）
cd promptproof

# 2. 校验示例镜头文件
python -m promptproof validate examples/shots.json

# 3. 生成两阶段计划：只批准 cat-desk 出成片
python -m promptproof plan examples/shots.json --approve cat-desk --rates examples/rates.json --out plan.md

# 4. 打开 plan.md，照清单先跑打样、确认后再跑成片
```

可选安装为系统命令：

```bash
pip install .
promptproof validate examples/shots.json
```

## 📖 详细使用指南

### 镜头文件格式（JSON）

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

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 镜头编号，批准成片时用它点名 |
| `subject` / `action` | 是 | 主体与动作，空着会被校验拦下 |
| `camera` / `style` | 否 | 镜头运动与风格，默认 camera 为 static |
| `source_image` | 否 | 图生视频的首帧图文件名 |
| `negative` | 否 | 不希望出现的元素 |
| `duration_sec` | 否 | 时长（秒），1–15，默认 5 |
| `final_resolution` | 否 | 成片分辨率：768P / 1080P / 2K，默认 2K |

### 三条命令

```bash
# 校验：有问题退出码为 1，适合接在脚本前面把关
python -m promptproof validate my_shots.json

# 只看某一个镜头拼好的提示词，可直接复制去生成工具
python -m promptproof prompt my_shots.json cat-desk

# 导出 CSV 清单（--format csv），或不写 --out 直接打印到屏幕
python -m promptproof plan my_shots.json --approve cat-desk,harbour-dawn --format csv
```

### 单价配置

复制 `examples/rates.json` 改成你实际用的服务的每秒价格（单位自定，全表统一即可）：

```json
{ "768P": 0.20, "1080P": 0.40, "2K": 0.80 }
```

> 仓库里的数字只是算例，不代表任何服务商的真实报价，务必改成你自己的。

### 典型场景

1. **批量图生视频**：把一周要做的 20 个镜头写成一个 JSON，先校验去重，
   打样总价一目了然，否掉一半后成片费直接省下来。
2. **接单对账**：CSV 清单就是报价依据，打样花了多少、成片花了多少，分得清清楚楚。
3. **提示词沉淀**：结构化镜头文件本身就是可复用的资产库，比聊天记录里翻一段话靠谱。

_运行截图 / 演示动图：待补（本地运行 `plan` 命令的终端输出即为清单效果）。_

## 💡 设计思路与迭代规划

设计上只坚持三条：**零依赖**（标准库能干完的事绝不引包，工具活得比依赖久）、
**先算账后执行**（任何要花钱的批量活儿都应该先有一张能看懂的清单）、
**不绑服务商**（单价、分辨率全是配置，今天用 A 家明天换 B 家，工具不用改）。

后续迭代计划：

- [ ] 支持从 CSV 表格导入镜头（很多创作者习惯用表格排片）
- [ ] 批准状态写回镜头文件，形成可追溯的验片记录
- [ ] 导出 ComfyUI 工作流可读的批次说明文件
- [ ] 多币种与预算上限提醒（超预算时校验直接报警）

社区贡献方向：新的导出格式、更多校验规则、真实使用场景的示例镜头库。

## 📦 打包与部署指南

本项目是**工具 / 脚本类项目**，无需打包可执行文件，也没有 Release 附件，按下面方式集成即可：

- **直接运行**：克隆或复制目录后 `python -m promptproof ...`，适合临时使用。
- **安装为命令**：在项目根目录 `pip install .`，之后任何目录都能用 `promptproof` 命令；
  卸载用 `pip uninstall promptproof`。
- **嵌进自己的脚本**：

```python
from promptproof.models import load_shots
from promptproof.planner import build_plan, to_markdown_checklist

shots = load_shots("my_shots.json")
plan = build_plan(shots, approved_ids={"cat-desk"})
print(plan.total_cost, to_markdown_checklist(plan))
```

- **兼容环境**：Python 3.10+，Windows / macOS / Linux；无网络要求，可在离线机器上跑。
- **常见问题**：报 `no rate configured` 是单价表里缺了那个分辨率，补上即可；
  报重复镜头不是出错，是同一创意写了两遍，删掉一条或改掉创意字段。

## 🤝 贡献指南

欢迎 Issue 和 PR，细则见 [CONTRIBUTING.md](CONTRIBUTING.md)。简单说：先开 Issue
说清问题或想法；PR 保持改动单一、附带测试；提交信息用 `feat:` / `fix:` / `docs:`
等前缀。提交前请跑通 `python -m unittest discover -s tests -v`。

## 📄 开源协议说明

本项目采用 MIT 协议开源，见 [LICENSE](LICENSE)。你可以自由使用、复制、修改和
分发，包括商用，只需保留版权与协议声明；软件按「现状」提供，不附带任何担保。
