# 测试报告（TEST_REPORT）

- 日期：2026-10-28
- 环境：Python 3.12.3（Linux），仅标准库
- 测试框架：`unittest`（本机未安装 pytest，因此按任务允许的方式用 unittest 执行；
  测试文件同样兼容 pytest，装有 pytest 的环境可直接 `python -m pytest tests/ -q`）

## 单元测试

命令：

```bash
python -m unittest discover -s tests -v
```

实际结果：**Ran 9 tests in 0.001s — OK**，全部通过，无报错。

| # | 测试 | 结果 |
|---|---|---|
| 1 | test_estimate_cost_multiplies_duration_by_rate | ok |
| 2 | test_estimate_cost_rejects_unknown_resolution | ok |
| 3 | test_duplicates_are_detected_and_skipped_once | ok |
| 4 | test_exports_contain_checkboxes_and_csv_rows | ok |
| 5 | test_final_stage_only_contains_approved_shots | ok |
| 6 | test_rejecting_an_expensive_shot_saves_money | ok |
| 7 | test_compose_prompt_has_labelled_sections | ok |
| 8 | test_validate_accepts_a_good_shot | ok |
| 9 | test_validate_flags_empty_subject_and_bad_duration | ok |

## CLI 冒烟测试（examples/shots.json）

```bash
python -m promptproof validate examples/shots.json
# OK: 2 shot(s), no problems found

python -m promptproof prompt examples/shots.json cat-desk
# [Subject] an orange cat sitting at a small wooden desk
# [Action] turns its head towards the camera and blinks slowly
# ...（Camera / Style / First frame / Avoid 各一行）

python -m promptproof plan examples/shots.json --approve cat-desk \
    --rates examples/rates.json --out plan.md
# wrote plan.md: proof CNY 2.00, final CNY 4.00, savings vs direct CNY 2.00
```

金额手算复核一致：打样 2×5s×0.20=2.00；成片 1×5s×0.80=4.00；
全部直出成片为 8.00，计划总计 6.00，差额 2.00。

## 结论

核心功能（校验、去重、提示词拼装、成本估算、两阶段计划、导出）全部通过自测，
可直接本地运行。无高危问题：工具不联网、不读环境变量、不调用外部 API。
