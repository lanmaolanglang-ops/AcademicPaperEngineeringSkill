# Academic Paper Engineering Skill

用于课程论文、技术综述、实验报告、调研报告和工程分析报告的可复用 AI 论文工程工作流。

当前版本：**v2.1**。覆盖需求、结构、写作、数据、技术、引用、文本优化、文档交付和修改管理；用证据台账追踪主张依据，由最终验收控制器判断当前版本能否交付。

## 快速开始

1. [下载 v2.1 完整文件包](packages/AcademicPaperEngineeringSkill_v2.1.zip)。
2. 阅读 [SKILL.md](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/SKILL.md)。
3. 从 [用户调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md) 选择目标，填写实际材料与要求，再交给支持加载 Skill 或 Markdown 工作流的 Agent。

入口识别名为 `academic-paper-engineering-v2-1`。具体安装和发现机制遵循所用工具；此仓库不会自动安装技能或创建 Agent。包内保留 `skill/academic-paper-engineering-v2/` 路径，保持已有相对链接兼容。

## v2.1 补充能力

| 能力 | 作用 | 入口 |
| --- | --- | --- |
| Evidence Ledger | 记录主张、具体证据、来源支持范围、数字口径与推导链 | [证据台账](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/evidence_ledger_template.md) |
| Final Acceptance Controller | 只读核对当前版本和提交条件，输出 PASS、CONDITIONAL PASS 或 BLOCKED | [控制器](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/agents/final_acceptance.md) |
| User Prompt Templates | 从零写作、已有稿优化、提交审查、最终 Word/PDF 四种入口 | [调用模板](AcademicPaperEngineeringSkill_v2.1/skill/academic-paper-engineering-v2/templates/user_prompt_templates.md) |

数据审计保持原四状态；台账的 Unknown 表示主张关系尚未判断。来源真实不等于支持所有相关主张，计算正确不等于参数正确，结构完成不等于论文完成。所有 Passed 必须绑定对象、版本、范围、方法和证据。

## 内容结构

```text
AcademicPaperEngineeringSkill_v2.1/
├── 原六份已去标识的案例与版本报告
├── v2.1升级说明.md
├── v2.1验收报告.md
└── skill/academic-paper-engineering-v2/
    ├── SKILL.md
    ├── modules/     # 九个原模块
    ├── agents/      # 五个原角色与最终验收控制器
    ├── templates/   # 三个原模板与三个新增模板
    └── knowledge/   # 失败模式、质量规则、案例分析模板
```

完整文件树与兼容性说明见 [v2.1 升级说明](AcademicPaperEngineeringSkill_v2.1/v2.1升级说明.md)。

## 验收范围

文件包的结构、链接、旧版保护、去标识和 ZIP 完整性检查已经执行，结果见 [v2.1 验收报告](AcademicPaperEngineeringSkill_v2.1/v2.1验收报告.md)。文件包验收不代表真实论文运行效果已验证；没有承诺检测率、成绩、录用或未执行的页面与打印检查。

仓库提供完整技能、说明和已去标识的案例资料，不包含原始聊天导出、原论文文件、账户凭据或工作区中间材料。模板中需要的个人元数据只用于用户自己的论文项目，不应写回此 Skill。
