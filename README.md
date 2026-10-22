# Academic Paper Engineering Skill

> **2.5.1 · 中文优先 · 论文工程化 + 证据审计 + 最终验收**


**把题目、资料和草稿，推进成有依据、能复核、可交付的论文工程。**

Academic Paper Engineering Skill 是一套给 AI Agent 使用的工作流程。它帮助你明确研究问题、组织章节、核查数字和引用、管理修改，并对最终文件给出有范围的验收结论。它既支持从零开始，也支持已有稿件的诊断、优化和交付。

本发行包版本为 **2.5.1**。实际公开状态以 [GitHub Release](https://github.com/lanmaolanglang-ops/AcademicPaperEngineeringSkill/releases/tag/v2.5.1) 为准。正式发布、许可和验证范围见[发布说明](releases/2.5.1/RELEASE_NOTES.md)及[验证记录摘要](releases/2.5.1/docs/VALIDATION.md)。这是工作流程Skill，不自带模型、联网数据库、Word程序或自动评分器。

本发行包采用[MIT许可](releases/2.5.1/LICENSE)，Copyright (c) 2026 lanmaolanglang-ops。许可仅涵盖本包中有权授予的项目内容，[授权范围](releases/2.5.1/LICENSE_STATUS.md)不包括旧版本、真实论文或第三方资料。

[下载 2.5.1 ZIP](packages/AcademicPaperEngineeringSkill_2.5.1.zip) · [ZIP SHA256](packages/AcademicPaperEngineeringSkill_2.5.1.zip.sha256) · [三分钟开始](releases/2.5.1/docs/QUICKSTART.md) · [安装与调用](releases/2.5.1/docs/INSTALL.md) · [完整使用说明](releases/2.5.1/docs/USER_GUIDE.md) · [核心入口](releases/2.5.1/skill/academic-paper-engineering-v2-5/SKILL.md)

## 你可以让它做什么

| 你的目标 | 工作方式 | 典型成果 |
| --- | --- | --- |
| 我要写论文 | 先读需求和实际材料，建立问题、边界和证据计划 | 需求表、结构提纲、分章草稿、待核项 |
| 我要优化论文 | 先诊断结构、技术、数据和引用，再在授权范围内改副本 | 诊断报告、候选新稿、修改和复核记录 |
| 我要检查论文 | 按当前版本只读审查，不自动修改正文 | 有位置、严重程度、依据及关闭标准的报告 |
| 我要核查数据或引用 | 逐条比对来源、原句、对象、时期和条件 | 数据表、主张证据关系、引用核查与缺口 |
| 我要准备提交 | 生成所需文件并检查当前版本、页面和硬要求 | DOCX/PDF、恢复版本、最终验收报告 |

适用于课程论文、技术综述、实验报告、调研报告、科研初稿与工程分析。实验和调研仍需真实原始记录；不能让AI补造样本或结果。结构、图数、字数与文献数服从你的实际要求。

## 中文论文排版

学校、期刊或用户模板优先；没有模板时按[中文论文默认样式](releases/2.5.1/skill/academic-paper-engineering-v2-5/references/chinese_paper_format.md)设置正文宋体小四、标题黑体、明确行距与缩进，并检查DOCX实际字体及页面。它是可覆盖的产品默认，不是所有学校统一标准。缺字体与未检项明确记录，不以文件生成成功代替排版通过。

## 为什么不只用一句写作提示词

普通写作请求往往只得到一段文字。本Skill还要求保留这段文字的依据、版本和完成状态：

- **证据台账**：来源存在、实际已读和支持具体主张分别判断；支持、反驳、背景与缺源不混用。
- **逐次位置**：同一结论在摘要、正文、表格、图注和结论中复用，每个位置都能追溯；改数不能只改第一次。
- **审查和修订**：先指出问题，再落实授权修改，最后重新核查影响项；保留原稿及恢复依据。
- **最终验收**：草稿写完、Word保存或PDF导出都不能自动等于“可以提交”。

## 第一次怎么说

安装后直接说：“我要写论文”“我要优化论文”“我要检查论文”或“我要准备最终提交”，并提供实际文件。也可明确调用：

```text
请使用 $academic-paper-engineering-v2-5。
我要优化这篇技术综述。请先只读诊断，再在新副本中落实有依据的修正。
原稿和现有参考资料已附；格式不明确的地方请指出。
```

第一轮应告诉你：已读材料、当前目标、当前论文版本、缺失信息、下一步。资料不足时先完成可做的规划或诊断，不假称已经有参考文献或完整正文。[四种详细调用模板](releases/2.5.1/skill/academic-paper-engineering-v2-5/templates/user_prompt_templates.md)可以直接填写。

## 完整工作流

需求分析 → 结构设计 → 内容生成 → 数据审计 → 技术审查 → 引用审查 → 文本质量控制 → 格式交付 → 修改管理与当前版本验收。

阶段按依赖迭代。只查一个数字时不必重新做整篇；小任务可把台账、位置与检查结果合并在同一报告。六份角色文件是职责划分，不会自动启动六个Agent。

## 怎样看状态

| 最终验收状态 | 你应该如何理解 |
| --- | --- |
| PASS | 指定版本及明确要求均有有效检查证据；只覆盖所声明范围 |
| PARTIAL | 没有阻断项，但存在已说明的非硬要求低风险残留；不是正式PASS |
| BLOCKED | 必需文件、关键依据、页面或外部要求等尚未闭合，不能判断可以正式提交 |
| NOT RUN | 该项没有执行，不能当作通过 |

数据Verified只说明相应数字依据；关系Verified只说明该边目标受支持。算术正确不证明参数真实，引用编号闭环不证明观点有据。回归测试PASS也不是你的论文PASS。

## 工具和人工核实

Skill本身是Markdown规则，安装不需要Python或数据库。实际读Word、导出PDF、联网查源等依赖当前Agent已有能力。缺工具时必须说明限制，保留NOT RUN/BLOCKED；不能伪造产物或检查。

你仍需提供课程模板、原始实验/调查记录、订阅或不可访问资料，以及确实要求的身份字段；核实关键专业结论并承担最终提交决定。流程不保证成绩、录用、检测分数、所有平台兼容或论文零错误。

## 包内内容

`skill/academic-paper-engineering-v2-5/`包含核心入口、九模块、六角色、七模板、三知识库、脱敏案例与按需参考。`docs/`是用户指南；内部运行包、原论文、私人对话、评估者判据和安全研究材料不在公开ZIP中。

[更新记录](releases/2.5.1/CHANGELOG.md) · [已知验证范围](releases/2.5.1/docs/VALIDATION.md) · [故障排查](releases/2.5.1/docs/TROUBLESHOOTING.md) · [贡献指南](releases/2.5.1/CONTRIBUTING.md) · [MIT许可及范围](releases/2.5.1/LICENSE_STATUS.md)

## 历史版本（独立保留）

以上说明针对 2.5.1。包内目录说明以独立 ZIP 根目录为准，仓库中的对应位置为 `releases/2.5.1/`。MIT 的范围见该版本自己的 LICENSE_STATUS，根导航不将整个历史仓库一并重新许可。

- [2.5.1-rc.1 预发布](https://github.com/lanmaolanglang-ops/AcademicPaperEngineeringSkill/releases/tag/v2.5.1-rc.1)及[候选源码](release-candidates/2.5.1-rc.1/README.md)。
- [排版维护候选与当时限制](release-candidates/2.5.1-rc.1-typography.20261021/README.md)。
- [v2.1 历史包](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/SKILL.md)。

历史失败、PARTIAL、BLOCKED 与 NOT RUN 保持其原本范围，不回写历史结果。
