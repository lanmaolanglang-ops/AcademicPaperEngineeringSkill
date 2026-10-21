# Academic Paper Engineering Skill

## 排版修复维护候选 2026-10-21

当前可试用 **2.5.1-rc.1+typography.20261021**：无学校模板时默认正文宋体小四、标题黑体，并明确字体、字号、缩进与行距；用户模板优先。新增实际字体/段落核对及可选格式辅助脚本，同时保留此前提交验收和逐页检查的修复。

[下载修复版ZIP](packages/AcademicPaperEngineeringSkill_2.5.1-rc.1_typography_20261021.zip) · [SHA256](packages/AcademicPaperEngineeringSkill_2.5.1-rc.1_typography_20261021.zip.sha256) · [查看完整Skill](release-candidates/2.5.1-rc.1-typography.20261021/README.md) · [修复内容与验证边界](docs/typography-maintenance-20261021.md)

本机Word已实际核对55段、825项字体及段落参数；**本次排版补丁尚未重跑豆包，跨软件分页仍有差异，证据契约仍有PARTIAL**。这是维护候选源码和ZIP，不是新Release或稳定版。历史测试结果及未运行项保持原范围，不能据此认定论文可以提交。

## 已发布的预发布基线

**当前发布候选：论文工程化 + 证据审计 + 最终验收。**

[开始使用](release-candidates/2.5.1-rc.1/README.md) · [安装与调用](release-candidates/2.5.1-rc.1/docs/INSTALL.md) · [完整使用说明](release-candidates/2.5.1-rc.1/docs/USER_GUIDE.md) · [发布说明](release-candidates/2.5.1-rc.1/RELEASE_NOTES.md) · [MIT许可](release-candidates/2.5.1-rc.1/LICENSE)

当前版本为 **2.5.1-rc.1 Prerelease**，保持READY WITH LIMITATIONS。已测范围为23个普通功能Case；逐调用档案完整性PARTIAL 1项、六个补充覆盖NOT RUN，不代表跨模型、跨平台或OS隔离盲测验证，也不代表论文可以正式提交。详见[验证边界](release-candidates/2.5.1-rc.1/docs/VALIDATION.md)。

Copyright (c) 2026 lanmaolanglang-ops。MIT只覆盖[当前候选包内有权许可的项目内容](release-candidates/2.5.1-rc.1/LICENSE_STATUS.md)，不自动重新许可旧版本档案、真实论文、内部验收证据或第三方资料。原始RC独立ZIP和外侧SHA在[候选Release](https://github.com/lanmaolanglang-ops/AcademicPaperEngineeringSkill/releases/tag/v2.5.1-rc.1)提供。

以下完整保留原v2.1 README，作为历史说明；其中旧版入口不代表当前候选版本。

---

<div align="center">

# Academic Paper Engineering Skill

### 从研究问题，到有证据、有边界、可验收的论文成果。

一套覆盖规划、写作、审查、修改与交付的 AI 学术论文工程工作流。

**v2.1 · 中文优先 · 通用技术论文流程 · 主张证据追踪 · 当前版本验收**

[下载完整 Skill](packages/AcademicPaperEngineeringSkill_v2.1.zip) · [阅读核心规则](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/SKILL.md) · [选择调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md)

</div>

---

**让关键判断有依据，让修改过程可追踪，让最终交付有验收。**

Academic Paper Engineering Skill 将题目、资料和草稿组织成可复核的论文工程任务：先明确问题和要求，再建立结构、生成内容、核查数字与引用，最后完成文档交付和当前版本验收。

你可以从零开始，也可以带着已有论文进入相关阶段。它提供明确的步骤、角色、模板与检查规则，帮助支持读取这些文件的 AI Agent 持续推进工作。

## 目录

- [适用场景](#适用场景)
- [完整功能](#完整功能)
- [工作流程](#工作流程)
- [v2.1 增强能力](#v21-增强能力)
- [快速开始](#快速开始)
- [四种常用任务](#四种常用任务)
- [交付成果](#交付成果)
- [角色与模板](#角色与模板)
- [质量规则与验收](#质量规则与验收)
- [目录与版本说明](#目录与版本说明)
- [验证范围](#验证范围)

## 适用场景

| 场景 | 如何组织任务 |
| --- | --- |
| 工程类课程论文 | 从课程要求出发，收窄题目，设计论证主线，分章写作并核对提交规范 |
| 技术综述 | 围绕技术分类、比较、分歧和适用条件整理来源，说明证据覆盖与研究缺口 |
| 实验报告 | 依据真实方法、原始记录和测量条件处理结果、误差与结论 |
| 调研报告 | 说明问题、实际样本、数据口径和方法，控制从样本推广到总体的范围 |
| 科研初稿 | 明确研究问题、假设、方法、证据与贡献，区分设想和已完成成果 |
| 工程分析与专业报告 | 围绕机制、指标、比较基准、工程约束和取舍形成有依据的判断 |
| 已有稿件优化 | 先诊断结构、技术、数据与引用问题，再在授权范围内定向修正 |
| 提交前检查 | 对当前稿件只读审查，或在材料齐备时执行正式交付验收 |

流程按文种和任务调整。章节数量、图表数量、文献数量与篇幅以实际要求和论证需要为准。

## 完整功能

v2.1 保留九个基础模块，在原流程上增加证据台账、最终验收控制器与用户调用模板。

| 模块 | 主要能力 | 典型成果 |
| --- | --- | --- |
| [01 需求分析](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/01_requirement_analysis.md) | 清点实际材料，确认可读范围；明确文种、对象、边界、字数口径、格式、来源与改动范围 | 材料读取报告、需求契约、缺口清单 |
| [02 结构设计](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/02_structure_design.md) | 定义中心问题与暂定论点，将子问题、前提、证据和章职责连接起来；安排研究与图表计划 | 提纲、章节职责表、证据需求、篇幅预算 |
| [03 内容生成](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/03_content_generation.md) | 以主张、证据、解释和边界写作；校准核心章节，登记数字与引文，回查摘要和结论 | 可审草稿、主张台账、待核项、图表计划 |
| [04 数据审计](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/04_data_audit.md) | 核数值、对象、时期、单位、分母、口径、预测情景与精度；分别判断公式、算术、参数和外推 | 四状态数据表、计算复核、处置清单 |
| [05 技术审查](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/05_technical_review.md) | 检查概念、系统边界、模型层级、工程条件、因果关系与技术评价 | 分级问题、依据、修正建议与关闭标准 |
| [06 引用审查](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/06_citation_review.md) | 核文献真实、实际阅读范围和观点支持；按指定 GB/T 7714 版本或其他要求管理编号与双向覆盖 | 引用矩阵、参考文献表、编号映射 |
| [07 文本质量控制](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/07_ai_quality_control.md) | 压缩重复与空泛段落，收窄无据强结论，补有据的机制、比较、约束与反例分析 | 局部优化稿、意义变化记录 |
| [08 图表与格式交付](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/08_format_delivery.md) | 检查图表职责与来源；整合样式、目录、页码、题注、封面和文献；导出 PDF 并核实际页面 | 同版本 DOCX/PDF、源图、恢复版本、检查记录 |
| [09 修改管理](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/modules/09_revision_management.md) | 维护唯一当前版本，记录问题、决定与实际改动；按影响复核，支持中断恢复和最终接受 | 版本链、决策记录、问题闭环、冻结交付清单 |

### 贯穿全过程的能力

- **研究规划与资料整理：**记录来源身份、检索与阅读范围、冲突和证据缺口，围绕问题决定需要哪些资料。
- **图表设计：**明确每张图表承担的比较、关系或证据职责；源数据、绘制文件和正式题注可追踪。
- **审查后的定向修改：**先报告问题，再按已有授权落实修正，检查数字、引用、摘要、结论和页面受到的影响。
- **版本保护与恢复：**保留上游原稿，中断后先核实际完成点，再继续已授权工作。
- **按需执行：**支持单章节、单项数据核查、只读审查或仅排版，不强制重复整个流程。

## 工作流程

~~~mermaid
flowchart TB
    A["需求分析与材料读取"] --> B["研究规划、资料整理与结构设计"]
    B --> C["章节写作与图表规划"]
    C --> D["数据审计"]
    D --> E["专业技术审查"]
    E --> F["文献与引用审查"]
    F --> G["文本优化与定向修正"]
    G --> H["Word / PDF 排版与页面检查"]
    H --> I["当前版本最终验收"]
    I --> J["交付文件、检查记录与恢复版本"]

    L["证据台账：主张—证据—来源"] -.-> C
    L -.-> D
    L -.-> E
    L -.-> F
    L -.-> I
    R["修改管理：版本、决定与影响复核"] -.-> B
    R -.-> G
    R -.-> H
    R -.-> I
~~~

阶段可以迭代，但依赖必须成立。新数据、换来源、改观点或移章节，会触发相应范围复核；格式调整后也要重查受影响的页面与目录。

## v2.1 增强能力

### Evidence Ledger · 为关键主张建立依据链

证据台账回答三件事：**为什么写这句话？为什么采用这个数字？结论由哪些前提推出？**

每个主张关联具体证据与来源，记录实际支持的部分、条件、冲突和缺口。它可引用已有审核表，小任务也可以合并记录。

| 主张类型 | 记录重点 |
| --- | --- |
| Fact · 事实 | 对象、时期、条件和直接证据 |
| Prediction · 预测 | 发布机构、发布时点、预测期、情景与范围 |
| Assumption · 假设 | 明确设定、用途、理由及限制 |
| Calculation · 计算 | 公式、输入、单位、参数身份与复算 |
| Inference · 推论 | 前提、推导链、反例和结论边界 |
| Recommendation · 建议 | 目标、依据、权衡与适用条件 |

数字额外关联数值、单位、时间、对象、统计口径和来源位置。一个主张可以有多个来源；一个来源多次使用时，每条支持关系分别判断。

**台账管理主张与证据关系，数据审计检查数字与参数。**台账中一个条件计算已核，不会自动使未核参数成为可信事实。

→ [查看证据台账模板与完整规则](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/evidence_ledger_template.md)

### Final Acceptance Controller · 判断当前版本是否完成

控制器读取最终版本、需求、证据台账、数据／技术／引用／格式报告和修改记录，核对当前交付条件。

它只负责交付判定；有阻碍时返回对应角色处理，再对更新后的版本验收。

| 最终结论 | 判定条件 |
| --- | --- |
| **PASS** | 所有适用提交条件有当前有效证据且满足，无未关闭提交问题 |
| **CONDITIONAL PASS** | 主体可靠、硬要求全部满足，仅有明确、非硬要求、不影响可靠性与主要结论的低风险 Minor 残留 |
| **BLOCKED** | 关键证据或必检缺失、可靠性问题未解决、Critical/Major 未关闭，或提交硬要求未满足 |

检查记录绑定**对象、版本、范围、方法和证据**。上一轮通过、文字流畅或格式完成，不能自动让当前整篇通过。

→ [查看控制器](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/final_acceptance.md) · [查看验收报告模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/final_acceptance_report.md)

### User Prompt Templates · 填好要求就能开始

四种入口覆盖从零写作、已有稿优化、提交前只读审查和最终 Word/PDF 生成。

普通用户填写题目、学科、要求和实际材料；内部编号与台账可由执行任务的 Agent 维护。

→ [打开四种完整调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md)

## 快速开始

### 1. 下载并解压

[下载 v2.1 完整文件包](https://github.com/lanmaolanglang-ops/AcademicPaperEngineeringSkill/raw/refs/heads/main/packages/AcademicPaperEngineeringSkill_v2.1.zip)，解压到容易找到的位置。

入口在：

~~~text
AcademicPaperEngineeringSkill_v2.1/
└── skill/
    └── academic-paper-engineering-v2/
        └── SKILL.md
~~~

内部目录沿用 <code>academic-paper-engineering-v2</code>，用于兼容旧相对链接。v2.1 入口识别名为 **<code>academic-paper-engineering-v2-1</code>**，版本元信息为 **2.1**。

### 2. 让 Agent 读到规则

将完整 Skill 目录放入 Agent 可读取的工作文件夹，明确指定入口；或上传、粘贴规则文件，补充任务需要的关联模块与模板。

先要求材料读取报告：哪些文件实际可读、读到什么范围、有哪些缺口。下载完成或只发出技能名称，不等于已读取规则。

已安装并被识别的环境，可以使用 <code>$academic-paper-engineering-v2-1</code>。具体安装与发现方式遵循目标工具；本仓库提供规则包。

### 3. 提供真实要求与材料

- 题目或暂定方向、学科与目标读者。
- 字数及统计口径、格式模板、引用制度与指定版本。
- 当前稿件、实际来源、原始实验或调研记录。
- 截止时间与时区、允许修改范围。
- 需要的成果，如 DOCX、PDF、图表源和验收报告。

未知写未知；缺失如实标记。联网查证、Word/PDF 创建和页面查看，需要当前 Agent 环境具备相应工具。

### 4. 选择任务入口并推进

从[调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md)选择目标。核对需求、诊断结果和最终验收后，保存报告指定的文件与恢复版本。

<details>
<summary><strong>展开：最小调用示例</strong></summary>

下面是填写框架，方括号内容需换成实际信息：

~~~text
请使用 Academic Paper Engineering Skill v2.1。

本次目标：[从零写作 / 已有稿优化 / 只读审查 / Word与PDF交付]
题目与学科：[填写]
字数与统计口径：[填写，未知标未知]
格式与引用要求：[填写或提供实际模板]
已提供材料：[列实际文件，无则写无]
允许修改范围：[填写]
截止时间与时区：[填写]
交付文件：[填写]

先读取规则与材料，报告可读范围和缺口，再推进相关阶段。
关键主张用证据台账追踪，数字和参数独立审计。
保留原稿，记录修改及复核。
最终验收绑定当前对象、版本、范围、方法与证据，列未完成项。
~~~

</details>

## 四种常用任务

| 你现在的情况 | 选择入口 | 执行方式 |
| --- | --- | --- |
| 只有题目或资料，还没有正文 | [从零写课程论文](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md#模板1从零开始写课程论文) | 先问题、结构和证据，再生成内容，随后审计与交付 |
| 已有 Word 或完整正文，希望提升质量 | [已有论文深度优化](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md#模板2已有论文深度优化) | 先诊断结构、技术、数据和引用；再在授权范围内改新版本 |
| 提交前想知道问题，暂不改稿 | [论文提交前审查](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md#模板3论文提交前审查) | 只读检查，输出问题、证据、建议和关闭标准 |
| 内容候选已具备，需要正式文件 | [生成最终 Word/PDF](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md#模板4生成最终-wordpdf) | 保留原稿、管理源图，核同版 DOCX/PDF 和实际页面，再验收 |

只读审查交付的是报告；授权修改并复核后，才有修正稿。中途进入任务时，先确认可沿用成果和证据。

## 交付成果

根据任务范围与工具能力，可以组织以下成果：

| 类型 | 成果 |
| --- | --- |
| 规划 | 材料清单、需求契约、研究问题、提纲、篇幅与证据计划 |
| 内容 | 当前版本正文、摘要、结论、图表与待核清单 |
| 证据 | 主张—证据台账、数据与参数审计、计算复核、引用矩阵 |
| 审查 | 结构与技术报告、分级问题、修改建议与关闭标准 |
| 修改 | 决策记录、前后对照、版本链、影响复核与恢复位置 |
| 文档 | 可编辑 DOCX、同版本 PDF、必要图表源、提交文件清单 |
| 验收 | 当前范围的最终判定、依据、残留事项及未执行项 |

按需交付，表格和报告可以合并。关键关系、版本身份和检查证据应保留可定位性。

## 角色与模板

### 六个执行职责

| 角色 | 负责什么 |
| --- | --- |
| [Structure Optimizer](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/structure_optimizer.md) | 中心问题、章节职责和逻辑关系 |
| [Academic Reviewer](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/academic_reviewer.md) | 专业概念、技术条件、推论与表达 |
| [Data Auditor](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/data_auditor.md) | 数字、参数、计算与适用范围 |
| [Citation Checker](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/citation_checker.md) | 文献身份、阅读范围、主张支持与编号 |
| [Document Formatter](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/document_formatter.md) | 图表、排版、DOCX/PDF 与页面检查 |
| [Final Acceptance Controller](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/final_acceptance.md) | 只读判断当前成果能否交付 |

同一 Agent 可按阶段承担不同职责。审查角色先出报告，主 Agent 整合修改和当前版本；角色文件不会自动创建或派发其他 Agent。

### 六个可复用模板

[决策记录](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/decision_record_template.md) · [审核报告](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/review_report_template.md) · [最终检查](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/final_check_template.md) · [证据台账](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/evidence_ledger_template.md) · [最终验收报告](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/final_acceptance_report.md) · [用户调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md)

### 三份知识资源

[常见失败模式](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/knowledge/common_failure_modes.md)用于诊断数据、概念、引用、表述和交付问题；[高质量论文规则](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/knowledge/high_quality_paper_rules.md)提供判断标准；[案例分析模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/knowledge/case_analysis_template.md)帮助沉淀可推广经验。

## 质量规则与验收

### 所有判断回到实际材料

1. 先确认材料存在、可读及完整范围；不可读内容标为 <code>[NOT_AVAILABLE]</code>。
2. 事实、预测、目标、模型、实测、假设和推导保留身份；需要原始结果时不生成虚构观测。
3. 来源存在、来源已读、来源支持具体观点，分别判断。
4. 公式、算术、输入参数、外推结论，分别检查。
5. 问题发现、建议、写入、复核和最终接受，分别记录。
6. 任何 <code>Passed</code> 绑定对象、版本、范围、方法与证据。
7. 保留原稿；变更后复核影响项，验收后改动不自动继承旧结论。

### 状态各有用途

| 层次 | 状态 | 用途 |
| --- | --- | --- |
| 数据依据 | Verified / Partial Verified / Unsupported / Need Source | 当前数字与参数的依据 |
| 主张证据关系 | Verified / Partial Verified / Unsupported / Need Source / Unknown | 当前主张支持范围与缺口 |
| 逐项检查 | Passed / Failed / Not Run / Not Applicable | 实际检查是否执行、适用及结果 |
| 最终交付 | PASS / CONDITIONAL PASS / BLOCKED | 当前指定成果是否满足提交条件 |

Unknown 属于证据台账，不加入原数据四状态。核实预测仍是预测；合法的条件计算只支持所列条件，不能为无源现实参数背书。

### 使用边界

专业教师视角用于组织审查，不等于外部专家认证。流程以准确性、论证和可追溯交付为目标，不承诺查重或 AI 检测分数、成绩、录用、未执行打印或未测试平台结果。

当前 Agent 的文件、联网、计算和文档工具决定可执行范围；工具缺失或检查未运行要如实说明。

## 目录与版本说明

<details>
<summary><strong>展开完整 Skill 文件结构</strong></summary>

~~~text
AcademicPaperEngineeringSkill_v2.1/
├── 01_材料读取报告.md
├── 02_论文工程案例分析.md
├── 03_决策记录库.md
├── 04_失败模式库.md
├── 05_Skill交付说明.md
├── 06_v1.0到v2.0差异报告.md
├── v2.1升级说明.md
├── v2.1验收报告.md
└── skill/
    └── academic-paper-engineering-v2/
        ├── SKILL.md
        ├── modules/
        │   ├── 01_requirement_analysis.md
        │   ├── 02_structure_design.md
        │   ├── 03_content_generation.md
        │   ├── 04_data_audit.md
        │   ├── 05_technical_review.md
        │   ├── 06_citation_review.md
        │   ├── 07_ai_quality_control.md
        │   ├── 08_format_delivery.md
        │   └── 09_revision_management.md
        ├── agents/
        │   ├── academic_reviewer.md
        │   ├── data_auditor.md
        │   ├── citation_checker.md
        │   ├── structure_optimizer.md
        │   ├── document_formatter.md
        │   └── final_acceptance.md
        ├── templates/
        │   ├── decision_record_template.md
        │   ├── review_report_template.md
        │   ├── final_check_template.md
        │   ├── evidence_ledger_template.md
        │   ├── final_acceptance_report.md
        │   └── user_prompt_templates.md
        └── knowledge/
            ├── common_failure_modes.md
            ├── high_quality_paper_rules.md
            └── case_analysis_template.md
~~~

</details>

当前包包含 **33 个 Markdown 文件**：25 个 Skill 文件与 8 份顶层报告。

v2.1 在 v2.0 基础上保留九个模块、五个原角色与既有资源，增加四个 Skill 文件与增强路由。数据四状态及既有编号继续兼容。

原六份报告保留 v2.0 历史记录；旧版目录和检查数描述当时成果。当前增强范围以 [v2.1 升级说明](AcademicPaperEngineeringSkill_v2.1/v2.1升级说明.md)和[验收报告](AcademicPaperEngineeringSkill_v2.1/v2.1验收报告.md)为准。本仓库发布的是 v2.1 包。

## 验证范围

已执行的文件包检查包括目录与链接、旧版内容保护、去标识、规则兼容性和 ZIP 完整性。详情见 [v2.1 验收报告](AcademicPaperEngineeringSkill_v2.1/v2.1验收报告.md)。

这些结果验证 Skill 文件包与规则的相应范围。真实论文的内容、参数、页面和交付结果，需要针对实际材料与当前版本另行检查。

仓库案例资料已经去标识，不包含原始聊天导出、原论文、账户凭据或工作区中间文件。项目所需身份信息只保留在用户自己的项目资料中，不写回公开 Skill。

---

**用问题组织结构，用证据支撑判断，用复核推动修改，用验收结束交付。**

[现在开始：选择一个调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md)
