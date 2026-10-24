# 文献身份、发表后状态与版本核验契约

## 范围与既有能力

原引用审查已分开来源真实性、实际阅读、主张支持及格式/编号。本契约补发表后通知、版本身份及其证据身份链核验，不新增模块、角色、主张字段或第二套台账。数据依据四态、关系五态、问题闭环、行为五态及论文最终四态保持原义。

## SRC最小视图

沿用SRC-ID、原来源身份/版本、阅读范围和CIT/CLM/DATA/EVID。已有等价字段直接引用，否则在SRC记录增加：

| 字段 | 内容与边界 |
| --- | --- |
| canonical_identifier | 规范DOI（去doi:或resolver前缀，保留原值，DOI大小写归一）；无DOI用官方标识/ISBN/稳定官方地址，不编DOI。任意URL路径不可无条件小写 |
| version_relation | 当前使用版本、相关SRC及关系/依据；版本正确性与身份匹配另判 |
| publication_status | 已查范围内的事件及汇总、冲突和未知；不是关系Verified/Unsupported等业务状态 |
| checked_at | 每次实际查询/读取时间含时区，区分通知发布日期；只计划时不造访问时间 |
| authority_record | 实际查的URL/查询、机构、返回状态、快照/哈希、通知目标、覆盖范围及缺口，可引用已有检查记录 |

关系交接链：SRC-ID → 版本/发表记录 → 阅读证据 → CLM-ID/DATA-ID → 原件精确位置及EVID-ID → 支持五态/方向/强度 → CIT-ID。重要主张原16字段和每关系八维继续执行；普通来源视图不能替代它们。

## 实际执行步骤

1. 冻结当前引文与来源身份。对照可读权威记录的作者、题名、标识符、载体、日期与具体版本，逐字段保留差异。只凭题名、DOI可解析或相似度不能宣布身份一致；无DOI不是伪造。中文学位论文、标准、机构/政府报告优先官方原件/题录，缺作者字段与文档身份分清。
2. 按来源类型优先查出版社文章页和正式通知，再查Crossref明确更新关系、合适的领域库/官方档案。登记实际访问情况；原文记录未出现通知、搜索零结果或某库未收录都不是全网无通知证明。通知有独立标识，核其明确目标及关系方向，不能因正文出现retraction一词或引用某撤稿文章而把当前论文判撤稿。
3. 对通知原文实际阅读：撤稿、更正、关注声明和其他更新分别识别。出版社不可访问时可核其在官方档案的授权副本/元数据，明确实际来源及未读的出版社页，不假称两者都已访问。单一服务的范围限制持续保留。时间较旧、访问失败、付费墙、429、超时、TLS错误、分页未完均记实际缺口，不能说文献不存在；可离线核固定材料，但不得称实时通过。
4. 查预印本平台版本历史、发表链接和正式记录；用明确标识符关系，或实际多字段及关键内容对照建立关系。作者/标题改变可真实发生，需记录差异和明确对应依据；不能仅标题相似自动合并。疑似同研究而未证实就保留疑似，已核错配记录不同研究。同一研究两版本不计为两项独立研究；讨论版本变化可分别列SRC及关联。
5. 明确实际读到元数据、摘要、部分全文或完整全文，保留范围和精确锚点。提供全文文件不等于读完；只读摘要时身份可以匹配，全文方法/表格等主张仍待核。回到原Ledger对每个实际目标判支持，书目/DOI/发表状态不能传播为关系通过。引用格式与编号按实际指定且可读规范另判。
6. 状态/版本或文件身份改变后，记录受影响CLM/DATA/EVID/CIT及所有出现位置、变化前后依据；未复核关系Unknown。保留旧状态、检查时间与原报告，另加新检查，不能改旧Verified或直接沿用旧锚点。必要检查缺失对正式对象的影响由原Gate归约。

## 发表状态记录

事件列表可同时包含RETRACTED（撤稿）、CORRECTED（更正）、EXPRESSION_OF_CONCERN（关注声明）、OTHER_UPDATE（其它明确更新），每项绑定通知身份、目标、实际日期、权威记录和影响范围。没有机械优先级删除较早事件。

汇总用NOTICES_FOUND（列实际事件）、NO_NOTICE_FOUND_IN_CHECKED_SOURCES（仅已查范围未见）、CONFLICT（有明确互斥权威断言）、UNAVAILABLE（必要来源不可访问且未取得有效检查）、NOT_CHECKED（尚未查）、NOT_APPLICABLE（确不适用且有理由）。可部分取得材料时列已核范围及未访问尝试，不能用一个汇总掩盖缺口。一个库未见记录与另一个库检出通知不必然是冲突；缺失不等于明确否定。非适用不能用来跳过实际学术来源的发表核查。

撤稿不能无说明地为被撤销结果背书，也不自动证明其所有陈述为假。撤稿通知本身可作为研究对象引用，绑定通知自身SRC/CLM及用途，不能误作被撤销结论的有效支持。更正涉及所用数字/单位/公式/方法/结论时逐项重核；只改无关署名不能无依据说所有数值无效，但要保存范围评估。关注声明是风险信号，不等于撤稿，须审查其与当前目标的关系。其它更新同样核范围；未知影响不归Minor。

## 版本关系与正确性

记录PREPRINT_ONLY、PUBLISHED_COUNTERPART、MATERIAL_DIFFERENCE、CORRECTED_VERSION、SUSPECTED_SAME_RESEARCH、DIFFERENT_RESEARCH或UNKNOWN，以及相关标识、版本/日期、实际比较范围与依据。这是版本关系标签，不是论文或证据关系新状态。

识别正式版对应关系只证明版本关联，不能证明内容相同；未比较全文时明确未核内容等价性。关键数值、方法、结论变化触发原目标复核，旧版本支持不自动迁移。所用版本是否符合任务要求单列“正确/不符/待核”及依据，不由存在正式版自动禁止研究预印本本身。

## 五维输出与版本明细

每项至少输出：身份（匹配/不符/待核及字段差异）；发表状态（上述事件/范围）；阅读程度（实际范围）；主张支持（原Verified / Partial Verified / Unsupported / Need Source / Unknown及目标/证据/限制）；引用格式（原Passed / Failed / Not Run / Not Applicable及实际规范/编号范围）。版本正确性与关系作为身份旁的单独明细，六个逻辑问题均可追溯。某个维度Passed不能替代其它维度。

## 可选离线助手

[check_literature_record.py](../scripts/check_literature_record.py)仅标准库。输入为一个原SRC的JSON视图，不替代Ledger或建立数据库。使用命令：

```text
python scripts/check_literature_record.py --allowed-root package_root --input package_root/cases/inputs/source_record.json --output package_root/new_check.json
```

必须新输出路径，输入和history只读。退出0只表示写出无结构错误的检查记录，不是文献/论文PASS；errors非空退出2，待核关系仍须人工处理。errors/review_required须实际处理；相同输入和快照重复运行应一致。

接口：SRC-ID、citation（canonical_identifier/title/authors）、metadata_ref（已读元数据投影的path/sha256，投影含provenance原始获取证据）、authority_record（url/checked_at/coverage/access_ref及可选notice_ref）、version_relation、reading（level/evidence）、可选support_review与citation_format、history。证据引用使用path/sha256，JSON可给pointer，XML给xml_path，原生文本可给真实行范围；可给quote回查。路径相对输入文件。提取投影须保留原始来源及投影方法；哈希只核身份，不证明投影正确或网页权威。

notice_ref读取Crossref元数据中的明确update-to目标/type，不从标题猜。其它服务用人工实际核查并保留原通知与目标证据，不能伪装成Crossref响应；助手不自动理解任意出版社格式。身份MATCH只覆盖输入字段和已核原件投影，不是来源绝无伪造的认证。FULL_TEXT等阅读标签仍须有真实执行记录，脚本不会证明人确已读完。

support_review包括CLM-ID、target、原关系status、reason、可选旧source_sha256、登记证据引用、semantic_review_ref及requires_full_text；新绑定要求见下文。这是原职责角色的语义判定，助手只核锚点/身份/范围一致，不从短引文包含某词自动验证科学结论。状态/版本变化影响未闭合时输出Unknown并要求复核；复核完成须绑定update_review_evidence。EOC单列风险，不自动判撤稿。history原样输出不回写源文件。

version_correctness单列版本使用符合性；未给明确任务要求时Not Run，不从发现正式版自动推断用户必须使用正式版。可提供version_requirement的canonical_identifier、reason及可选source_sha256，核当前使用标识和已读文件身份是否满足该明确要求；不能据此声称两个版本文本一致或旧支持可迁移。相同DOI下的更正前后文件须按实际不同文件身份和更新复核证据区分。

ID-LINE-1仅为明确的本地测试/用户简式：`[n] | author | title | identifier`四列非空。助手仅判句法，不声称GB/T/APA合规，不由格式Passed反推身份；其它规范保留Not Run并用实际规范独立核验。编号首引/复用与双向覆盖仍按原引用模块，助手不自动重排。

## 维护验收

固定语料、模拟服务与有限实时请求分开。每次保存输入/快照哈希、原始响应、预期、实际五维/版本、差异、行为结果及失败。合成错误和权威冲突必须标synthetic，不能把注入值说成真实文献更正。真实通知身份、许可、引用信息须实际核验后才写预期。独立语义执行者只得到输入及最少原始来源，不给观察者答案；候选先冻结并核前后身份。未运行保持NOT RUN，外部阻断不改为文献不存在；不依靠降低判据制造通过。

## fix1：支持证据身份链

结构校验不能证明科学结论。先实际阅读，再保存明确目标、证据作用、支持判断及范围；助手只验证该判断与当前原件/锚点一致，不认证审查人或保证其判断正确。预填Verified、非空列表、题录匹配或正确SHA单独都不足以通过。旧无绑定记录仍能读取，但正向支持会成为Unknown/Need Source并要求补证，不自动把历史迁成当前通过。

沿用原SRC/EVID/CLM记录，不另建台账：

- `source_documents`：每个已读版本的`document_id`、`raw_ref`、`acquisition_ref`、`version`。raw_ref指实际原件或下述明确规范化表示的path/sha256；获取记录含真实url/checked_at/status_code/sha256。JATS核自身front/article-meta DOI及题名，不从正文参考文献中寻找自己的身份。
- `reading.evidence`：实际位置的path/sha256、XML/JSON/行锚点，以及唯一`EVID-ID`和对应`document_id`。引用必须属于该登记原件或经验证的派生文本。
- `support_sources`：需要跨来源时，平行登记额外SRC的citation/metadata_ref、source_documents、reading及实际发表/版本记录，不嵌套、不混用ID。每个来源独立核查。只复核当前主张明确依赖的来源，未使用条目不能清空其它关系或历史。
- `support_review.evidence`：只引用`{ "SRC-ID": "SRC-A", "EVID-ID": "E1", "role": "该来源对当前目标的具体贡献" }`。不能直接塞一份未登记的B文件替代A的证据。
- `support_review.semantic_review_ref`：实际阅读后的独立JSON记录path/sha256。内容为CLM-ID、target、status、reason、reviewer、reviewed_at、reading_scope及evidence；前三项须与当前主张完全一致。

语义记录中每个evidence指纹为：SRC-ID、EVID-ID、document_id、raw_sha256、read_sha256、anchor_sha256、context_sha256、role。必须与本次实际读取的来源/锚点/作用逐项一致，不能继承其它版本或其它目标的审查。anchor_sha256以实际选中的文本UTF-8字节计算；JSON非字符串用ensure_ascii=False、sort_keys=True、separators=(',', ':')规范序列化后计算。助手可在`support_binding_candidates`返回已核结构指纹；它仍不是语义支持判断。只有完成真实阅读和判断后，才用这些指纹另存审查记录。

JATS派生正文只支持可重复的`conversion: jats-body-text-v1`：按ElementTree `.//body//p`顺序对每段itertext拼接，再用换行连接，UTF-8无额外尾换行。`derived_ref`须与此结果逐字节一致，原件SHA和派生SHA分别保留。未知转换/任意提取文本不能偷偷继承原件身份。

现有无DOI官方语料保留`representation: official-limited-json-v1`：raw_ref是明确声明的有限规范化JSON，不称为整本官方出版物。核自身url/title/excerpt、实际嵌入获取记录和单独acquisition_ref一致、官方索引及章节地址的同站从属范围，并要求conversion_note。其SHA标识这份有限表示；原获取字节SHA单列，不能冒充同一个哈希或声称已读未附的整本原件。转换的真实性仍须实际审查；该兼容入口不是任意JSON的自动权威认证。其它格式继续按F06实际定位、阅读和人工核验；此助手不新增通用格式提取/语义引擎。

更正/版本/文件身份变化仍触发受影响CLM/DATA/EVID/CIT复核。原件不符、语义记录过时、锚点不符或依赖来源失效时，只把当前关系置待核并列明原因。旧history原样保留。正确来源上的实际Unsupported/Partial Verified也保留，不因身份成功自动升级。

## fix1：允许根与文件读取

输入内容不能授权新的根。CLI必须由调用方显式传`--allowed-root`，Python API `evaluate(record, base, allowed_root=...)`不传时只允许base目录。不得为适配坏路径而把根扩大到用户目录、盘符根或网络位置。

证据path相对其记录基准目录；metadata的provenance相对该metadata文件实际所在目录。元数据、原件、派生文件、获取记录、版本证据、语义审查均受同一个根约束。允许`cases/inputs`经`../../corpus`引用同包文件；先按实际平台解析，再核最终位置属于根，不按字符串前缀判断。引用拒绝绝对、盘符/驱动器相对、UNC、设备、ADS及歧义别名路径。

Windows使用已打开句柄的最终路径在读内容前复核根与文件身份；同一读取缓冲区同时核SHA与解析，读后复核文件标识/大小/时间及路径。POSIX仅在可确认最终打开路径的/proc环境有实现分支，本轮未实测；其它平台失败封闭，不能声称跨平台认证。符号链接/junction解析后越界必须拒绝，根内合法路径不因包含..而拒绝。

输出必须为根内新路径，既有报告不覆盖；越界/坏哈希/缺文件等失败保留明确错误、当前支持不为Verified、CLI退出2，不记录文件正文作为异常日志。调用方仍须保护授权根、输出父目录与可信审查记录不被其它进程恶意修改。前后复核降低竞态风险，不是对任意并发攻击/文件系统的形式化保证；不信任的根/平台应停止，不可关闭校验。


fix1上下文补充：每项证据的context_sha256由`source_context(source, checked_result)`计算，绑定当前实际核出的发表汇总/事件/覆盖缺口、版本关系、用途、update_impact及更新复核证据身份。相对文件路径写法不参与指纹，证据SHA/锚点参与。版本或更正上下文改变后，即使把update_impact改成reviewed_current，也不能沿用旧语义审查；须实际复核并另存带新上下文的判断。已有context缺失的记录同样待核，不自动升级。五维仍分别输出，格式成功不能修复过时的支持关系。


## fix2：发表状态来源、获取与复核上下文

沿用authority_record/access_ref/notice_ref，不把HTTP200、DOI或非空通知当成权威与科学支持认证。离线程序只能核对保存链的一致性，无法认证获取者、原服务器或审查者。真实获取与阅读仍需实际执行，合成访问必须标simulated，输出不得冒称新实时成功。

每次authority_record需要url、checked_at、access_ref、coverage及成功时的response_ref。response_ref是实际完整响应文件的path/sha256；access_ref读取实际获取JSON，其中url是请求URL、final_url是最终响应URL、checked_at是含时区的获取时刻、status_code及sha256对应真实响应字节；如有bytes必须相符。请求与最终URL不同时提供redirects有序列表，每步from/to/status_code（301/302/303/307/308），首尾与实际获取一致。来源声明可用链中URL；规范DOI也可用显式source_mapping:{kind:doi-via-crossref,canonical_identifier:实际DOI}映射至已取得Crossref work自身DOI。不得猜测其它映射或扩大授权根。没有重复增加请求URL字段；获取记录的url保持原义。

coverage改为可核的有界对象：metadata/notice_metadata配scope=returned_record、pointer=/message；query_results配scope=returned_items、pointer=/message/items；失败用kind=failed_attempt、scope=attempt_only。只核实际返回内容，complete必须false，不把单个响应变成全网/全部通知/全文已核。coverage.description与authority_record.display_label明确仅为显示文字，不能承载或扩大证据范围；实际范围写kind/scope/pointer。未结构化旧覆盖说明保持历史原文，当前须补核，不能自动猜其范围。查询返回少数记录不是完整检索，coverage_complete始终false。

当前自动路径只支持实际原始Crossref JSON envelope，核已选/message工作自身身份、查询items和明确update-to。响应原始字节SHA与获取sha256必须一致；JSON指针投影必须能从同一响应确定性重算。未知转换、任意出版社HTML/XML正文与归档API需真实人工核验，不用伪造Crossref形状替代来源。本补丁不增加通用提取引擎。无DOI官方文献身份与阅读仍按fix1独立核验，不能因发表状态未查而说其不存在。

notice_ref必须指向已取得响应中自己的/message或/message/items/N work对象，记录自身DOI及update-to的目标/type。与主访问同一次响应时其SHA必须与该响应一致；独立通知请求用notice_access_ref指自己的获取记录，通知SHA只与自己的响应核对，不要求它等于论文元数据SHA。旧notice_ref若本来就是同一已取得原始响应，可直接用作response_ref的等价引用，仍须通过哈希和作用域核验。通知与目标不符、缺关系或借用无关访问记录均待核，不能从RETRACTED字符串猜结论。

事件输出保留实际通知的请求/最终URL、获取时刻、access和响应SHA、已选投影SHA/指针及关系指针/SHA。authority_record事件字段指通知的实际最终来源，不能冒用论文元数据URL；各次访问原身份分开。错误尝试保留attempts及原因，当前不输出其未经证明事件，其它有效尝试仍可保留自己的事件。NOT_CHECKED/UNAVAILABLE不是撤稿或论文不存在。

publication_status.context_sha256覆盖目标规范标识、各次获取记录身份、请求/最终URL及重定向、响应/投影与通知SHA、获取/核验时刻、实际覆盖、通知目标/type和已核事件、冲突/非适用依据；版本关系与用途继续由fix1 source_context绑定至主张语义复核。相对路径拼写、明确显示标签不参与；等价时区规范为同一时刻。影响证据/结论的变化不能保留旧语义指纹。

如有独立发表状态复核，沿用引用方式增加publication_review_ref，指另存JSON（context_sha256、status、reviewer、reviewed_at、reason）。context及状态不符时review_status=REVIEW_REQUIRED，errors/review_required明确复核；已有实际观察仍按本次有据事件列出，不把旧复核过期推断为撤稿。没有复核记录时为NOT_SUPPLIED，只表示未提供人工复核，不冒称它已完成。CURRENT仅说明保存复核与当前有界上下文一致，不是论文最终验收或科学认证。

旧记录、旧指纹和原始响应不回写。新核验/复核用新文件并保留history。旧自由覆盖或缺响应绑定的输入可以读取并输出待核，不能无依据自动迁移成当前通过。fix1允许根、错误哈希拒绝、输入只读/新输出及支持证据链持续生效。旧接口新增的当前复核要求属于安全迁移，不回填旧测试成绩。
