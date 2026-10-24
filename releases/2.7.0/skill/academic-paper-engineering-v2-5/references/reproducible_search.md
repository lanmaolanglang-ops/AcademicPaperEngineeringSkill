# 可复现检索

仅在实际检索/综述任务加载。先复用 SRC 台账，分别记研究问题与数据库原语法。新增 search_run_id 标识每次运行；不要给普通短文强加系统综述。

`collect_search.py --input config.json --output-dir new-run --allowed-root task-root` 为显式联网入口，只执行 Crossref HTTPS GET，最多3页、每页20条；原查询、filter/sort/order/select、时间时区、原响应、错误、Retry-After及恢复游标保留。运行目录必须不存在。默认只取题录字段，不取摘要或全文。已知 cursor 与 published/issued 排序组合会拒绝。429/超时停止，无隐式重试；重试用新目录并记前次运行。TLS校验必须开启。

配置包含 search_run_id、question、purpose、scope（数据库/学科/语言/年份/类型及未限制原因）、query（syntax、language、history；可选filter/sort/order）、limits（rows/max_pages）。工具补 started_at、tool、license_note、pages、claim_complete=false。Crossref许可见 https://www.crossref.org/documentation/retrieve-metadata/；摘要许可另归作者/出版社。本工具不宣称其他数据库已实现。

`check_search_run.py --input run.json --output new-result.json --allowed-root task-root` 离线重建。每page的 access_ref/response_ref 为相对path+sha256；access含url/final_url、checked_at、status_code、bytes、sha256、simulated。实际请求的query参数须等于原syntax，分页cursor连续；成功响应必须原始Crossref envelope。manual-export-v1只读取records数组，必须export_note，声明仅重建所给导出，不验证原检索。其数据来源和转换另附原件索引。

DOI规范化去重，保留每条来源响应/指针和元数据冲突。稳定官方ID/URL可用于无DOI记录；仅标题相同列歧义，不自动合并。Crossref is-preprint-of/has-preprint 显式关系归同一元数据研究组，仍保留所有版本；其余会议扩展/疑似关系待核，不自动算独立研究。study_groups是检索组织视图，不是科学身份认证。发表状态、阅读和支持继续按 literature_verification.md 实际核验。

screening逐条保存decision_id、stable_id、stage(metadata/abstract/full_text/final)、decision(include/exclude/pending)、reason、reviewer、reviewed_at、read_scope、reading_level及evidence(path/sha256/pointer)。metadata/abstract必须指当前记录；摘要必须实际存在才可说读过。全文/最终纳排要求source及现有有效文献原件绑定；无全文保持pending，不写不相关。重复决定用supersedes保存历史。计数按层与每条最终决定分别生成。

比较时compare_ref指旧输出(path+sha256)，query/raw/local_processing变化分别报告。固定字节可复现；实时元数据会变化，差异不自动意味着科学结论改变。INCOMPLETE保留恢复位置；RECORDED_RANGE_COMPLETE仅指已返回查询范围，exhaustive_literature_coverage永远false。网络失败不是不存在。
