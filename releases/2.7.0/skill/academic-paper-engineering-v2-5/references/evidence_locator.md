# 实际文件定位

沿用Ledger的F06定位契约；本工具只补原件读取，不重定义主张支持。`locate_evidence.py --input locator.json --output new-location.json --allowed-root task-root`。文件只读，每次重核SHA，改后重新定位。输入EVID-ID、source(SRC-ID/kind/description/document_ref或外部来源绑定)、format、locator、quote。外部source同方法接口，来源归属与位置准确分别输出。

| format | locator | 实际边界 |
|---|---|---|
| markdown/txt | line_start、可选line_end | UTF-8实际物理行，摘录核对 |
| pdf | physical_page(从1开始)，可选page_label/section/region[x0,y0,x1,y1] | PyMuPDF原件文本层和物理页；页标签≠印刷页。区域用PyMuPDF页坐标点，输出rotation。拒绝提取行冒充原件行 |
| image | region_pixels | PIL实际像素区域，只返回区域和OCR未运行 |
| docx | kind=paragraph/paragraph/section_path 或 kind=table_cell/table/row/cell | word/document.xml正文直接子段落或简单表格；章节+摘录SHA+原件SHA，段落号不跨版本永久有效 |
| xlsx | sheet/range及可选headers(标签→单元格地址) | openpyxl最多100单元格；formula/value/cached_value分开，recalculated始终false |

PDF默认Partial/EXTRACTED_NOT_VISUALLY_CHECKED。扫描/图像默认Partial/REGION_ONLY_OCR_NOT_RUN，不执行OCR。输出render_sha256用于把真实图像检查绑定当前原件/页/区域。PDF图像按PyMuPDF 1.5倍、alpha=false生成PNG，独立图像按选区RGB像素哈希；实际查看后另存visual_review_ref(context_sha256/render_sha256/reviewer/reviewed_at/scope/reason/matches)。一致可记录Passed/实际视觉确认，不一致Failed/VISUAL_CONFLICT；未提供或过时不能继承确认。审核者真实性不由本脚本认证。

DOCX嵌套文本框、嵌套/合并表、脚注、页眉脚等未实现对象拒绝并交人工；不改任何XML或样式。没有渲染不得编DOCX页码。XLSX缓存值可能缺失/过时，没有公式重算。OCR、跨平台、隐藏文本与全部复杂版式没有通用自动保证。证据成功定位始终claim_support Unknown；需原引用与语义审查才能建立支持关系。
