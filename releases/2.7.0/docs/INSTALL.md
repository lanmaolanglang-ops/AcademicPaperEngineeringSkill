# 2.7.0 安装与调用

从 [v2.7.0 Release](https://github.com/lanmaolanglang-ops/AcademicPaperEngineeringSkill/releases/tag/v2.7.0) 下载 `AcademicPaperEngineeringSkill_2.7.0.zip` 和同名 `.sha256`，先校验 ZIP SHA256 再解压。当前版本检查为完整字符串严格相等，不把旧版或其他candidate视为同版。

## 实际分发格式

本发行包采用独立Skill目录格式，入口为`skill/academic-paper-engineering-v2-5/SKILL.md`。它是工作流资料，不是桌面软件、联网服务或Office插件。不提供自动全局安装，也不预装模型或文档工具。

## Codex 项目内安装

1. 解压ZIP，确认完整目录可读。
2. 在准备打开的项目中建立`.agents/skills`。
3. 将发布包的`skill/academic-paper-engineering-v2-5`整个目录放入其中；避免多嵌套一层skill目录。
4. 在该项目调用`$academic-paper-engineering-v2-5`；如未显示，检查项目位置、嵌套和SKILL.md元数据，再按宿主提示刷新或重启。
5. 同名旧版本不合并。不要直接覆盖唯一副本；先在独立试用项目检查版本，必要时让Agent报告实际入口及metadata.version。

安装路径及显式调用方式依据[官方OpenAI文档](https://learn.chatgpt.com/docs/build-skills)。宿主版本/界面可能不同；复制路径只是安装动作，不等于已经验证自动发现。本发行包实际验证范围见[验证摘要](VALIDATION.md)。

## 临时按文件路径使用

不想安装时，可以让具备文件读取工具的Agent按实际可访问路径读取SKILL.md并按需读取支持文件。这是手动加载使用，不等于宿主自动发现或注册。不要只粘贴入口后假设其相对引用资源也已提供。

## 其他Agent

兼容读取Markdown资源的宿主可以尝试手动加载，但本发行包没有认证所有宿主的技能发现、上下文、文件、联网或Office能力。不要把Codex的目录说明当成其他产品的安装保证。

## 升级与依赖

升级时先备份已有同名 Skill，再将新包完整目录放入独立试用项目，确认 metadata.version 为 2.7.0 后切换使用。不要合并新旧目录。旧稳定版与原论文保持独立，回退使用保留的旧目录。

## 依赖与权限

读取规则无Python依赖。执行数据处理或DOCX/PDF任务时，Agent需要已有的读取、计算、导出及页面预览工具。缺少工具就保留未运行，不自动安装组件或修改安全配置。网络来源、插件授权和账户资源由宿主及你当前授权决定。可选依赖的许可见[第三方说明](../THIRD_PARTY_NOTICES.md)，尤其 PDF 功能使用 PyMuPDF 时须遵守 AGPL／商业许可。

## 验证版本与移除

要求Agent指出实际SKILL.md位置与metadata.version，应为2.7.0。旧文档2.5.1是过期断言，当前检查不接受；历史包应按其自身版本另行验证。项目安装不改变全局版本。需要回退时继续使用你保留的原版；移除的对象只是本次项目内复制的Skill目录，先确认路径，不删除论文原件和原版Skill。此文档不会自动执行删除或回滚。

## 可复现的只读版本验证

把以下代码另存到临时 verify-version.ps1，再用 PowerShell 传入实际 Skill 目录：`pwsh -NoProfile -File verify-version.ps1 -SkillRoot <目录>`。只读当前分发格式的 YAML frontmatter 中 metadata.version；没有通用YAML解析或自动升级行为。源码包没有另一个安装版本比较器。输出实际/预期/匹配；不匹配退出2，格式错误停止。

```powershell
param(
    [Parameter(Mandatory=$true)][string]$SkillRoot,
    [string]$ExpectedVersion = '2.7.0'
)
$EntryPath = Join-Path $SkillRoot 'SKILL.md'
$EntryText = Get-Content -LiteralPath $EntryPath -Raw -Encoding UTF8 -ErrorAction Stop
$Frontmatter = [regex]::Match($EntryText, '(?s)\A---\r?\n(.*?)\r?\n---')
if (-not $Frontmatter.Success) { throw 'Missing SKILL frontmatter' }
$Versions = [regex]::Matches($Frontmatter.Groups[1].Value, '(?m)^  version: "([^"]+)"[ \t]*\r?$')
if ($Versions.Count -ne 1 -or $Frontmatter.Groups[1].Value -notmatch '(?m)^metadata:[ \t]*\r?$') { throw 'Expected one metadata.version in the distributed frontmatter format' }
$ActualVersion = $Versions[0].Groups[1].Value
$Matched = $ActualVersion -ceq $ExpectedVersion
[pscustomobject]@{ entry=$EntryPath; actual=$ActualVersion; expected=$ExpectedVersion; match=$Matched } | ConvertTo-Json -Compress
if (-not $Matched) { exit 2 }
exit 0
```
