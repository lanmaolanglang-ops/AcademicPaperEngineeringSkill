# 第五部分：Academic Paper Engineering Skill v2.0

核心入口：[SKILL.md](skill/academic-paper-engineering-v2/SKILL.md)。全部内容已保存为可执行的 Markdown Skill 文件，未安装到全局目录。

## 文件结构

```text
skill/academic-paper-engineering-v2/
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
│   └── document_formatter.md
├── templates/
│   ├── decision_record_template.md
│   ├── review_report_template.md
│   └── final_check_template.md
└── knowledge/
    ├── common_failure_modes.md
    ├── high_quality_paper_rules.md
    └── case_analysis_template.md
```

## 执行方式

先加载入口，按任务选择相应模块；修改管理负责全过程基线、决定和闭环。资料整理在需求、结构与写作中执行，图表从结构规划并在格式交付中验收。并非只做九个互不关联的动作。

从零写作时：材料检查 → 需求与问题 → 结构及证据 → 章节 → 数据、技术、引用与文本复核 → 整合与排版 → 最终验收。已有稿件先核当前状态，再进入实际需要的阶段。

角色文件提供可复用的 Prompt，由同一主 Agent 分阶段使用即可；不会自动创建五个 Agent，也不要求固定数量的审查轮次。模板复制到实际项目填写，空字段不是已经验收的结果。

## 包含的规则与范围

包含七类失败机制及执行中断等扩展案例、可定位的审查格式、四状态数据体系、来源与引用事件映射、参数与推论独立验收、AI 文本信息贡献检查、Word/PDF 和恢复链验收。

包内规则已去除原论文标题、领域专属数值、个人及课程信息；发布包不包含原始分享页、聊天导出或用户论文文件。前三部分记录依据，第四部分保留失败原案的诊断身份，第五部分仅运行已抽象的正确流程。

v1.0 保留原目录和 ZIP。v2.0 使用独立调用名 `academic-paper-engineering-v2`，便于在用户需要时与原版本区分；安装、上传或发布不在本次已执行范围。
