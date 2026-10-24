# 三层审计视图

`render_audit_report.py --input index.json --output new-report.json --allowed-root task-root` 生成summary_markdown、technical_markdown、audit_evidence三个视图；原始输入/失败/响应不重写。调用者可把前两字段另存.md。适用于长报告；小任务继续合并现有报告。

索引含report_id、verdict、scope、next_step、limits、workstreams与records。每记录id/status/category/reason/evidence_ref；ref的path/sha256和可选pointer选中原始结果对象，其id/status/reason必须相同，原对象category/reason必须存在。五态沿用checking_contract。category表示本次索引的执行层，分层deterministic/real_material/live/regression/historical/repeat/independent/unexecuted，不计算混合总认证成绩。重复(id,execution_id)拒绝；历史结果不是新执行。BLOCKED/NOT RUN也要有真实阻断/未运行记录。

输出分别显示execution_layer、evidence_category、evidence_origin、current_result（只代表该条记录，不是覆盖历史的最终归约）。默认执行层必须与原对象category一致；原证据属性为unknown，不能凭字段猜测。若两者语义不同，提供classification_ref指向另存的分类复核：id/status/source_sha256/source_category/source_reason/execution_layer/evidence_origin均须精确绑定，另含rationale/reviewer/reviewed_at。evidence_origin限historical_record/current_record/first_failure/unknown。这是有身份的复核意见，不是工具自动证明。缺原始分类/理由的旧日志先另存规范复核记录，引用旧原件及SHA，不改旧日志。历史FAIL和重跑PASS使用独立记录及execution_id；不得用重跑结果改历史状态。生成的视图是当时快照；回查/复跑时重新验证全部证据哈希，文件被替换则旧输入失效。

ledger复用SRC-IDs/CLM-IDs，evidence为EVID-ID→SRC-ID；relations保存id/CLM-ID/EVID-ID/SRC-ID/status/原八维dimensions；citations为CIT-ID/SRC-ID/number；occurrences保存id/CLM-ID/location/CIT-IDs。机械检指向、唯一编号与所有实际出现，不能凭字段齐全判科学语义。“同上”不能替每边范围。原关系与出现记录完整在第三层，摘要不复制八维全文。

摘要显示所有非PASS记录和全部限制，技术表显示每条结果及证据。comparison仅比较同一规范记录重复公共头的基准与精简摘要长度，不冒充真实历史论文平均成本；实际总耗时另在运行记录。历史首错必须在索引保留，不为漂亮汇总隐藏FAIL。字段与关系一致、SHA匹配、HTTP200、未见通知均不能自动推出科学或论文PASS。最终verdict由实际验收者提供，工具不会替控制器归约。

需要证明摘要未漏掉某批记录时，提供inventory_ref指向已冻结的id/status/category/execution_id完整数组；逐项与records相等才输出BOUND_INVENTORY_COMPLETE。未提供时只核给定索引，标INDEX_ONLY_NOT_COMPLETENESS_VERIFIED，不能声称全部原始记录完整覆盖。
