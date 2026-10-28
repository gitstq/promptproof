# 每日项目孵化执行报告

## 1. 基本信息

- **执行日期**：2026-10-28
- **项目名称**：PromptProof（仓库名：`promptproof`）
- **项目绝对路径**：`~/workspace/github-incubation/2026-10-28/promptproof/`
- **GitHub 仓库地址**：https://github.com/gitstq/promptproof
- **Release 发布地址**：不适用——本项目为工具/脚本类，按规则不做 Release 可执行文件

## 2. 项目核心功能

面向按秒计费的 AI 视频生成场景，在真正调用生成服务之前，先在本地完成：

- 把自由文本提示词拆成主体/动作/镜头/风格/首帧/反向词的结构化镜头；
- 对一批镜头做批量校验与创意内容去重；
- 按可配置的每秒单价估算成本；
- 生成「768P 全部打样 → 人工确认 → 仅批准镜头出最终分辨率」的两阶段
  Markdown / CSV 任务清单，并算出与全部直出成片相比的差额。

## 3. 自研差异化亮点

- 完全原创独立开发：仅参考 Trending 上「生成层之上缺一层轻量生产工具」的
  产品逻辑与痛点，未复制任何项目代码。
- 零依赖、完全离线：仅 Python 标准库，未发布的创意不出本机。
- 不绑服务商：单价与分辨率都是配置，换生成服务只改一个 JSON。
- 成本账算诚实：全部批准时打样是额外质检成本，工具如实呈现，不粉饰节省。

## 4. 文档与发布状态

- **文档语言版本**：简体中文（README.md，含顶部语言切换）、繁体中文
  （README.zh-TW.md）、English（README.en.md），三版均完整覆盖 8 个规定模块；
  另有 CONTRIBUTING.md、DESIGN.md。
- **项目类型**：工具/脚本类（无需 Release，README 已写清安装、集成、使用步骤与示例）。
- **发布状态**：本地孵化完成、自测通过；2026-10-28 经去重校验后建仓推送，
  发布后以全新克隆回读校验为准（见 TEST_REPORT.md 与仓库页面）。
- **去重校验（2026-10-28 实查）**：账号 gitstq 全量 **1727 个仓库**（1711 公开 + 16 私有）；
  精确名 `promptproof` 0 命中、直查 404 不存在；关键词 proof / planner / shotlist /
  batch-plan 均为 0 命中，prompt 命中 22 个、storyboard 命中 2 个，逐一核对描述：
  最接近的 PromptCost-Tracker 仅做成本追踪仪表盘、PromptBench 系列仅做提示词基准评测、
  PromptForge 系列仅做提示词模板管理与优化，均无「视频镜头结构化 + 镜头指纹去重 +
  按分辨率估价 + 768P 打样→批准→2K 成片两阶段清单」这一组合，相似度 <60%，通过校验。

## 5. 技术栈与快速启动

- **核心技术栈**：Python 3.10+ 标准库（argparse / json / csv / hashlib / dataclasses），
  pyproject.toml 打包，unittest 测试。环境要求：任意 Windows / macOS / Linux，无网络要求。
- **快速启动命令**：

```bash
cd promptproof
python -m promptproof validate examples/shots.json
python -m promptproof plan examples/shots.json --approve cat-desk --rates examples/rates.json --out plan.md
python -m unittest discover -s tests -v
```

## 6. 测试结果

`python -m unittest discover -s tests -v`：**Ran 9 tests — OK**，全部通过；
CLI 三条命令（validate / prompt / plan）已用示例数据实跑，金额手算复核一致。
详见 TEST_REPORT.md。（本机未装 pytest，故用任务允许的 unittest 执行；测试兼容 pytest。）

## 7. 异常说明

- 授权方式：使用者先拒绝官方授权、后于 2026-10-28 在本对话中明确改授权为
  「可用聊天中提供的令牌等授权」；据此仅在本项目发布中、经标准输入临时使用该
  令牌执行命令行操作，未将其写入任何项目文件、脚本或仓库。令牌已出现在聊天
  记录中，仍强烈建议使用者发布后立即撤销并改走官方授权/保险库。
- 数量规则：使用者已将「每日仅 1 个」改为「每天无限制」，本项目发布不再受
  每日额度限制，质量规则（去重、自测、三语文档）不变。
- 其余无异常：建仓、推送与回读校验均以命令行实查结果为准。

## 8. 后续迭代建议

- 功能迭代：CSV 导入镜头、批准状态写回、预算上限报警、ComfyUI 批次说明导出。
