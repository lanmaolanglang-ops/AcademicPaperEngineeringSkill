# 方法与有限复算

由数据审计/技术角色按研究类型选择适用项：设计、样本/纳排、材料设备/校准、工况、对照、重复、采集预处理、单位、公式定义/适用性、中间量、误差、统计假设/异常、结论外推、局限和适用伦理。selection_reason解释选择，不要求每篇填全项；投稿声明未知仍未知，不自动写伦理批准/数据公开。

`check_method_review.py --input method.json --output new-result.json --allowed-root task-root`。
输入：method_review_id、CLM-ID、target、research_type、selection_reason；sources复用SRC-ID/kind/document_ref；evidence为EVID-ID/SRC-ID/ref(含pointer、line_start或xml_path)；data为DATA-ID/EVID-ID/value/unit，可有standard_uncertainty。原始数据字段必须是含同DATA-ID/value/unit的实际JSON对象，不能拿报告转录数字自证；不适配的真实原数据记材料不足，交人工溯源，不伪造JSON为原始实验。

sources的kind为synthetic/local_artifact/external。前两者必须description；外部原件若有literature_ref，必须通过原文献助手的实际reading绑定。只有acquisition_ref时仅核已取得的字节，来源归属仍待审；方法发现不能从这种文件定位自动变成主张Verified。来源上下文包括发表与版本，改变会使旧方法复核失效。

findings逐项包含dimension、outcome、reason、scope、reviewer、reviewed_at、EVID-IDs。七种方法结果：SUPPORTED、PARTIALLY_SUPPORTED、INTERNAL_CONTRADICTION、NOT_REPORTED、INSUFFICIENT_MATERIAL、NOT_APPLICABLE、EXPERT_REVIEW，仅属于方法维度。它们是有范围的审查人判断，脚本核证据/上下文一致性，不自动作科学判断。“未报告”限实际审查范围，不等于未发生；无法复算不等于造假。既有主张五态、数据四态、Gate与发表状态不变。

calculations有calculation_id、expression、variables(变量→DATA-ID)、variable_definitions、applicability、reported_value、reported_unit、absolute_tolerance、precision_note。仅允许+ - * /和常量整数幂-4..4，无eval/函数调用；支持kg/g、m/cm/mm、s/min/h、K、J/kJ、W/kW、Pa和乘除幂组合。摄氏温度偏移、复杂统计、相关误差需专家。输出SI中间量、量纲、换算、算术差异；有效数字由明确约定复核，不把浮点容差当精度认证。

误差法只实现uncertainty_method=independent-first-order及independence=explicit_assumption；所有参与量须有原件standard_uncertainty，使用实际表达式导数，重复变量保持相关。缺输入不是零误差。模型适用、独立性与结论范围由专家复核，算对不会自动支持结论。

首次检查返回context_sha256；实际审查后另存review_ref(method_review_id/context_sha256/reviewer/reviewed_at/reason)。CURRENT仅表明该保存复核与当前输入相容；改变主张、数值、单位、方法、来源/发表上下文后为REVIEW_REQUIRED。历史只读。findings在未提供复核时仍为原始待审观察，不自动升级。工具始终输出claim_support Unknown和paper_gate NOT RUN。
