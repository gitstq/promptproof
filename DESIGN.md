# PromptProof — 原创方案说明（DESIGN）

## 1. 选题依据（2026-10-28 公开调研）

公开 web 搜索 GitHub Trending 近期方向后观察到的共性：爆火的 AI 视频项目大多是
重型生成模型或巨型生产套件（高显存、数百文件、多服务），不适合单仓库轻量落地；
反而真正缺人做的，是生成模型「之上」的一层轻活儿——把想法整理成结构化任务、
先估算成本、批量校验、再决定哪些值得花钱生成。本项目只参考这一产品逻辑与痛点，
代码、结构、文案均为独立原创，未复制任何项目代码。

结合使用者的真实场景（ComfyUI + 按秒计费的图生视频、先用低清打样验片、确认后
才出 2K 成片），选题定为：**本地提示词结构化 + 批量任务清单工具**。它不调用任何
生成 API，因此不与已有的 ComfyUI 工作流重复——工作流负责「生成」，本工具负责
「生成之前先想清楚、算清楚」。

## 2. 技术栈选型

| 选择 | 理由 |
|---|---|
| Python 3.10+ | 创作者与开发者普遍已安装，跨 Windows / macOS / Linux |
| 仅标准库（argparse / json / csv / hashlib / dataclasses） | 零依赖 = 零安装陷阱，克隆下来就能跑，长期不会因依赖升级坏掉 |
| JSON 输入 | 机器可生成、人可手写，方便与 ComfyUI 等工具衔接 |
| unittest 测试 | 标准库自带，不逼用户为了跑测试再装东西；同时兼容 pytest |
| pyproject.toml | 现代 Python 打包标准，一条 `pip install .` 即可装成命令 |

## 3. 核心功能

1. **结构化镜头**：把自由文本提示词拆成 subject / action / camera / style /
   source_image / negative 等命名字段，缺项一眼可见。
2. **批量校验**：空主体、空动作、时长越界、分辨率不合法，一次列全。
3. **内容去重**：按创意字段指纹判重（同内容换时长不算新镜头），避免重复付费。
4. **成本估算**：单价表可配置，默认单价只是示例，必须按自己用的服务改。
5. **两阶段计划**：第一阶段全部镜头 768P 打样；第二阶段只有人工批准的镜头
   才生成最终分辨率；同时给出与「全部直出成片」相比的差额。
6. **清单导出**：Markdown 复选框清单（带可复制提示词）与 CSV 两种格式。

## 4. 技术架构

```
shots.json ──> models.load_shots ──> Shot.validate / find_duplicates
                                          │
prompt.compose_prompt <── Shot ──> planner.build_plan ──> cost.estimate_cost
                                          │
                              to_markdown_checklist / to_csv ──> 清单文件
                                          │
                                     cli.main (validate / prompt / plan)
```

- `promptproof/models.py` — 数据模型、校验、指纹去重、JSON 读取
- `promptproof/prompt.py` — 结构化字段拼装为带标签的提示词文本
- `promptproof/cost.py` — 单价表与单条成本计算
- `promptproof/planner.py` — 两阶段计划、直出对比、Markdown/CSV 导出
- `promptproof/cli.py` — 命令行入口（validate / prompt / plan）
- `tests/test_promptproof.py` — 9 个单元测试，覆盖提示词、校验、成本、计划、导出

## 5. 自测标准（已执行，见 TEST_REPORT.md）

- 全部单元测试通过；CLI 三条命令用示例数据实跑无报错；
- 示例计划的金额可手算复核：打样 2 条 × 5s × 0.20 = 2.00 元，
  成片 1 条 × 5s × 0.80 = 4.00 元，与直出两条成片（8.00 元）相比省 2.00 元。

## 6. 差异化亮点

- 不绑任何一家生成服务：单价、分辨率都是配置，换服务只改一个 JSON。
- 「省多少钱」算的是诚实账：全部批准时打样是额外质检成本，工具会如实显示。
- 完全离线、零依赖、不上传任何提示词内容，创作者的未发布创意不出本机。
