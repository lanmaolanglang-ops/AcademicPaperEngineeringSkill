# 第三方依赖与材料边界

本发行 ZIP 提供项目工作流、模板和脚本源码，不包含第三方库源码、二进制、字体、论文全文或上游 Skill 文件。项目 MIT 只许可有权许可的项目内容，不授予下列依赖或链接作品的权利。

| 已有环境中的可选依赖 | 用途 | 核查的环境版本及许可 |
|---|---|---|
| lxml | 中文 DOCX 排版助手 | 6.1.1，BSD-3-Clause；底层库另有声明 |
| PyMuPDF / MuPDF | PDF 定位 | PyMuPDF 1.28.0，AGPL-3.0 或 Artifex 商业许可 |
| Pillow | 图像区域定位 | 12.3.0，MIT-CMU；随其发行的编解码库可能另有条款 |
| openpyxl | XLSX 单元格定位 | 3.1.5，MIT |

版本来自本轮运行环境，不是强制版本锁定或随包提供的组件。应读取实际安装版本的完整许可证及附带声明。检索、离线来源核验、方法核查、报告与 DOCX 定位使用 Python 标准库；Python 本身按其许可证使用。

PyMuPDF 官方说明为 [AGPL／商业双许可](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright)。本项目的 MIT 源码授权不表示组合后的 PDF 功能仍只受 MIT 约束。采用 AGPL 版本进行组合分发或网络服务部署时，应满足适用的源代码提供、许可及通知义务；不采用该许可路径时须取得相应商业许可。公共源码包未捆绑该库，本次未授予或推定商业许可。

其他上游许可入口：[lxml](https://lxml.de/copyright.html)、[Pillow](https://pillow.readthedocs.io/en/stable/about.html#license)、[openpyxl](https://openpyxl.readthedocs.io/en/stable/)。重新分发这些依赖时保留其自身版权与许可通知，不以本文件代替完整条款。

来源审计参考过四个固定提交的研究／引用 Skill；审查范围内未确认移植其具体代码或文本，因而没有凭设计方法相似添加第三方作者署名。网络检索结果、论文、摘要、用户材料及产品商标仍受各自权利和使用条件约束；Crossref 事实元数据与摘要／全文的权利分开。本包不携带实际论文、原始响应或私人证据。
