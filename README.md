<div align="center">

# 📓 NoteVault-CLI

**轻量级终端 Markdown 笔记与知识库管理引擎**

*Lightweight Terminal Markdown Note & Knowledge Base Management Engine*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-brightgreen)](requirements.txt)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-lightgrey)](setup.py)

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**NoteVault-CLI** 是一款专为开发者和技术写作者打造的**纯终端 Markdown 笔记与知识库管理工具**。灵感来源于 Obsidian、Logseq 等优秀知识管理工具，但完全聚焦于终端环境，零 GUI 依赖，让你在任何 SSH 会话、远程服务器或本地终端中都能高效管理知识。

**解决的痛点：**
- ❌ GUI 笔记工具无法在服务器/远程环境使用
- ❌ 现有 CLI 笔记工具功能简陋，缺乏搜索和关联
- ❌ 笔记之间无法建立链接关系，知识呈孤岛状态
- ❌ 依赖复杂，安装配置耗时

**自研差异化亮点：**
- ✅ **零依赖** - 纯 Python 标准库实现，无需 pip 安装任何包
- ✅ **TF-IDF 全文搜索** - 智能中文分词 + 英文单词匹配，标题匹配加权
- ✅ **双向链接** - 支持 `[[笔记标题]]` 语法，自动构建知识图谱
- ✅ **标签系统** - `#标签` 自动提取，支持标签筛选浏览
- ✅ **多格式导出** - HTML / JSON / TXT / Markdown 一键导出
- ✅ **交互式 TUI** - 美观的终端界面，菜单导航零学习成本
- ✅ **批量导入** - 从目录批量导入现有 Markdown 文件

### ✨ 核心特性

| 特性 | 说明 | 状态 |
|------|------|------|
| 📝 **Markdown 原生支持** | 完整支持 Markdown 语法，笔记即文件 | ✅ |
| 🔍 **智能全文搜索** | TF-IDF 评分 + 中文分词 + 标题加权 | ✅ |
| 🔗 **双向链接** | `[[笔记标题]]` 语法，自动反向链接追踪 | ✅ |
| 🏷️ **智能标签** | `#标签` 自动提取，支持标签云浏览 | ✅ |
| 📊 **TUI 仪表板** | 终端可视化统计与最近笔记展示 | ✅ |
| 📤 **多格式导出** | HTML / JSON / TXT / MD 四种格式 | ✅ |
| 📥 **批量导入** | 从目录一键导入 Markdown 文件 | ✅ |
| 🗄️ **SQLite 后端** | 高性能本地存储，自动文件同步 | ✅ |
| 🧪 **完整测试覆盖** | 9 个核心功能单元测试全部通过 | ✅ |

### 🚀 快速开始

#### 环境要求
- **Python 3.8+**
- **操作系统**: Windows / macOS / Linux

#### 安装步骤

```bash
# 方式一: pip 安装 (推荐)
pip install notevault-cli

# 方式二: 从源码安装
git clone https://github.com/gitstq/NoteVault-CLI.git
cd NoteVault-CLI
pip install -e .

# 方式三: 直接运行 (零依赖)
git clone https://github.com/gitstq/NoteVault-CLI.git
cd NoteVault-CLI
python -m notevault
```

#### 快速启动

```bash
# 启动交互式菜单
notevault

# 或简写
nv

# 快速创建笔记
notevault -n "我的第一篇笔记" -c "这是内容 #标签"

# 搜索笔记
notevault -s "关键词"

# 列出所有笔记
notevault -l

# 查看统计
notevault --stats
```

### 📖 详细使用指南

#### 交互式菜单操作

启动 `notevault` 后，你将看到主菜单：

```
┌──────────────── 主菜单 ────────────────┐
│  [1] 📝 新建笔记        [2] 📋 列出笔记 │
│  [3] 🔍 搜索笔记        [4] 🏷️  标签浏览 │
│  [5] 📊 统计信息        [6] 📥 导入笔记 │
│  [7] 📤 导出笔记        [0] ❌ 退出     │
└────────────────────────────────────────┘
```

#### Markdown 语法支持

```markdown
# 一级标题
## 二级标题

**粗体文字** 和 *斜体文字*

- 列表项 1
- 列表项 2

`行内代码` 和 ```代码块```

[外部链接](https://example.com)

#标签1 #标签2

[[另一篇笔记]]  <-- 双向链接
```

#### 双向链接示例

创建笔记 A：
```
标题: 编程语言比较
内容: Python 和 JavaScript 都是流行的语言。
更多细节参见 [[Python入门指南]]
```

查看 "Python入门指南" 时，会自动显示：
```
🔗 反向链接 (1):
   ← 编程语言比较
```

#### 导入现有笔记

```bash
# 从目录导入所有 Markdown 文件
notevault --import-dir /path/to/notes --pattern "*.md"
```

#### 导出笔记

```bash
# 导出为 HTML
notevault --export 1 --format html > note.html

# 导出为 JSON
notevault --export 1 --format json

# 导出为纯文本
notevault --export 1 --format txt
```

### 💡 设计思路与迭代规划

#### 技术选型原因
- **Python 标准库**: 确保零依赖，任何有 Python 的环境都能运行
- **SQLite**: 轻量级嵌入式数据库，无需额外服务
- **文件同步**: 每条笔记同时保存为 `.md` 文件，数据完全可控
- **TF-IDF 搜索**: 轻量级但有效的搜索方案，无需引入 Elasticsearch

#### 后续迭代计划
- [ ] **Git 同步集成** - 自动 commit/push 到远程仓库
- [ ] **Web UI** - 可选的浏览器界面
- [ ] **插件系统** - 支持自定义扩展
- [ ] **模板功能** - 笔记模板快速创建
- [ ] **每日回顾** - 随机展示历史笔记
- [ ] **图形化知识图谱** - ASCII 关系图升级

### 📦 打包与部署

```bash
# 本地安装
pip install -e .

# 构建分发包
python setup.py sdist bdist_wheel

# 运行测试
python tests/test_core.py
```

### 🤝 贡献指南

欢迎提交 Issue 和 PR！请遵循以下规范：

- **Issue**: 描述问题、复现步骤、期望行为
- **PR**: 使用 Angular Commit 规范 (`feat:`, `fix:`, `docs:` 等)
- **代码风格**: 遵循 PEP 8，添加类型注解

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

**NoteVault-CLI** 是一款專為開發者與技術寫作者打造的**純終端 Markdown 筆記與知識庫管理工具**。靈感來自 Obsidian、Logseq 等優秀知識管理工具，但完全聚焦於終端環境，零 GUI 依賴，讓你在任何 SSH 連線、遠端伺服器或本地終端中都能高效管理知識。

**解決的痛點：**
- ❌ GUI 筆記工具無法在伺服器/遠端環境使用
- ❌ 現有 CLI 筆記工具功能簡陋，缺乏搜尋與關聯
- ❌ 筆記之間無法建立連結關係，知識呈孤島狀態
- ❌ 依賴複雜，安裝配置耗時

**自研差異化亮點：**
- ✅ **零依賴** - 純 Python 標準庫實現，無需 pip 安裝任何套件
- ✅ **TF-IDF 全文搜尋** - 智慧中文分詞 + 英文單字匹配，標題匹配加權
- ✅ **雙向連結** - 支援 `[[筆記標題]]` 語法，自動構建知識圖譜
- ✅ **標籤系統** - `#標籤` 自動提取，支援標籤篩選瀏覽
- ✅ **多格式匯出** - HTML / JSON / TXT / Markdown 一鍵匯出
- ✅ **互動式 TUI** - 美觀的終端介面，選單導航零學習成本
- ✅ **批次匯入** - 從目錄批次匯入現有 Markdown 檔案

### ✨ 核心特性

| 特性 | 說明 | 狀態 |
|------|------|------|
| 📝 **Markdown 原生支援** | 完整支援 Markdown 語法，筆記即檔案 | ✅ |
| 🔍 **智慧全文搜尋** | TF-IDF 評分 + 中文分詞 + 標題加權 | ✅ |
| 🔗 **雙向連結** | `[[筆記標題]]` 語法，自動反向連結追蹤 | ✅ |
| 🏷️ **智慧標籤** | `#標籤` 自動提取，支援標籤雲瀏覽 | ✅ |
| 📊 **TUI 儀表板** | 終端視覺化統計與最近筆記展示 | ✅ |
| 📤 **多格式匯出** | HTML / JSON / TXT / MD 四種格式 | ✅ |
| 📥 **批次匯入** | 從目錄一鍵匯入 Markdown 檔案 | ✅ |
| 🗄️ **SQLite 後端** | 高效能本地儲存，自動檔案同步 | ✅ |
| 🧪 **完整測試覆蓋** | 9 個核心功能單元測試全部通過 | ✅ |

### 🚀 快速開始

#### 環境要求
- **Python 3.8+**
- **作業系統**: Windows / macOS / Linux

#### 安裝步驟

```bash
# 方式一: pip 安裝 (推薦)
pip install notevault-cli

# 方式二: 從原始碼安裝
git clone https://github.com/gitstq/NoteVault-CLI.git
cd NoteVault-CLI
pip install -e .

# 方式三: 直接執行 (零依賴)
git clone https://github.com/gitstq/NoteVault-CLI.git
cd NoteVault-CLI
python -m notevault
```

#### 快速啟動

```bash
# 啟動互動式選單
notevault

# 或簡寫
nv

# 快速建立筆記
notevault -n "我的第一篇筆記" -c "這是內容 #標籤"

# 搜尋筆記
notevault -s "關鍵詞"

# 列出所有筆記
notevault -l

# 查看統計
notevault --stats
```

### 📖 詳細使用指南

#### Markdown 語法支援

```markdown
# 一級標題
## 二級標題

**粗體文字** 和 *斜體文字*

- 清單項目 1
- 清單項目 2

`行內程式碼` 和 ```程式碼區塊```

[外部連結](https://example.com)

#標籤1 #標籤2

[[另一篇筆記]]  <-- 雙向連結
```

#### 雙向連結範例

建立筆記 A：
```
標題: 程式語言比較
內容: Python 和 JavaScript 都是熱門的語言。
更多細節參見 [[Python入門指南]]
```

查看 "Python入門指南" 時，會自動顯示：
```
🔗 反向連結 (1):
   ← 程式語言比較
```

### 💡 設計思路與迭代規劃

#### 技術選型原因
- **Python 標準庫**: 確保零依賴，任何有 Python 的環境都能執行
- **SQLite**: 輕量級嵌入式資料庫，無需額外服務
- **檔案同步**: 每條筆記同時儲存為 `.md` 檔案，資料完全可控
- **TF-IDF 搜尋**: 輕量級但有效的搜尋方案，無需引入 Elasticsearch

#### 後續迭代計畫
- [ ] **Git 同步整合** - 自動 commit/push 到遠端倉庫
- [ ] **Web UI** - 可選的瀏覽器介面
- [ ] **外掛系統** - 支援自定義擴充套件
- [ ] **範本功能** - 筆記範本快速建立
- [ ] **每日回顧** - 隨機展示歷史筆記
- [ ] **圖形化知識圖譜** - ASCII 關係圖升級

### 📦 打包與部署

```bash
# 本地安裝
pip install -e .

# 建構分發包
python setup.py sdist bdist_wheel

# 執行測試
python tests/test_core.py
```

### 🤝 貢獻指南

歡迎提交 Issue 和 PR！請遵循以下規範：

- **Issue**: 描述問題、復現步驟、期望行為
- **PR**: 使用 Angular Commit 規範 (`feat:`, `fix:`, `docs:` 等)
- **程式碼風格**: 遵循 PEP 8，添加型別註解

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

**NoteVault-CLI** is a **pure terminal Markdown note & knowledge base management tool** designed for developers and technical writers. Inspired by excellent knowledge management tools like Obsidian and Logseq, it focuses entirely on the terminal environment with zero GUI dependencies, allowing you to efficiently manage knowledge in any SSH session, remote server, or local terminal.

**Pain Points Solved:**
- ❌ GUI note tools cannot be used on servers/remote environments
- ❌ Existing CLI note tools are too simplistic, lacking search and linking
- ❌ Notes cannot establish relationships, knowledge remains isolated
- ❌ Complex dependencies, time-consuming installation and configuration

**Differentiation Highlights:**
- ✅ **Zero Dependencies** - Pure Python standard library, no pip packages required
- ✅ **TF-IDF Full-Text Search** - Smart Chinese tokenization + English word matching with title weighting
- ✅ **Bidirectional Linking** - `[[Note Title]]` syntax with automatic knowledge graph building
- ✅ **Tag System** - `#tag` auto-extraction with tag cloud browsing
- ✅ **Multi-Format Export** - One-click export to HTML / JSON / TXT / Markdown
- ✅ **Interactive TUI** - Beautiful terminal interface with zero learning curve
- ✅ **Batch Import** - Import existing Markdown files from directory

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📝 **Native Markdown** | Full Markdown syntax support, notes as files | ✅ |
| 🔍 **Smart Full-Text Search** | TF-IDF scoring + Chinese tokenization + title weighting | ✅ |
| 🔗 **Bidirectional Links** | `[[Note Title]]` syntax with automatic backlink tracking | ✅ |
| 🏷️ **Smart Tags** | `#tag` auto-extraction with tag cloud browsing | ✅ |
| 📊 **TUI Dashboard** | Terminal visualization with stats and recent notes | ✅ |
| 📤 **Multi-Format Export** | HTML / JSON / TXT / MD formats | ✅ |
| 📥 **Batch Import** | One-click import from directory | ✅ |
| 🗄️ **SQLite Backend** | High-performance local storage with file sync | ✅ |
| 🧪 **Full Test Coverage** | 9 core function unit tests all passing | ✅ |

### 🚀 Quick Start

#### Requirements
- **Python 3.8+**
- **OS**: Windows / macOS / Linux

#### Installation

```bash
# Method 1: pip install (recommended)
pip install notevault-cli

# Method 2: Install from source
git clone https://github.com/gitstq/NoteVault-CLI.git
cd NoteVault-CLI
pip install -e .

# Method 3: Run directly (zero dependencies)
git clone https://github.com/gitstq/NoteVault-CLI.git
cd NoteVault-CLI
python -m notevault
```

#### Quick Commands

```bash
# Launch interactive menu
notevault

# Or shorthand
nv

# Quick create note
notevault -n "My First Note" -c "This is content #tag"

# Search notes
notevault -s "keyword"

# List all notes
notevault -l

# View stats
notevault --stats
```

### 📖 Detailed Usage Guide

#### Interactive Menu

Launch `notevault` to see the main menu:

```
┌──────────────── Main Menu ────────────────┐
│  [1] 📝 New Note        [2] 📋 List Notes │
│  [3] 🔍 Search Notes    [4] 🏷️  Browse Tags│
│  [5] 📊 Statistics      [6] 📥 Import Notes│
│  [7] 📤 Export Note     [0] ❌ Exit       │
└───────────────────────────────────────────┘
```

#### Markdown Syntax Support

```markdown
# Heading 1
## Heading 2

**Bold text** and *italic text*

- List item 1
- List item 2

`Inline code` and ```code blocks```

[External link](https://example.com)

#tag1 #tag2

[[Another Note]]  <-- Bidirectional link
```

#### Bidirectional Linking Example

Create Note A:
```
Title: Programming Languages Comparison
Content: Python and JavaScript are both popular languages.
See more details in [[Python Beginner Guide]]
```

When viewing "Python Beginner Guide", it automatically shows:
```
🔗 Backlinks (1):
   ← Programming Languages Comparison
```

#### Import Existing Notes

```bash
# Import all Markdown files from directory
notevault --import-dir /path/to/notes --pattern "*.md"
```

#### Export Notes

```bash
# Export as HTML
notevault --export 1 --format html > note.html

# Export as JSON
notevault --export 1 --format json

# Export as plain text
notevault --export 1 --format txt
```

### 💡 Design Philosophy & Roadmap

#### Technical Choices
- **Python Standard Library**: Ensures zero dependencies, runs anywhere with Python
- **SQLite**: Lightweight embedded database, no additional services needed
- **File Sync**: Each note saved as `.md` file, data fully under your control
- **TF-IDF Search**: Lightweight yet effective search without Elasticsearch

#### Future Roadmap
- [ ] **Git Sync Integration** - Auto commit/push to remote repository
- [ ] **Web UI** - Optional browser interface
- [ ] **Plugin System** - Support custom extensions
- [ ] **Templates** - Quick note creation from templates
- [ ] **Daily Review** - Random historical note showcase
- [ ] **Graph Visualization** - ASCII relationship graph upgrade

### 📦 Packaging & Deployment

```bash
# Local install
pip install -e .

# Build distribution
python setup.py sdist bdist_wheel

# Run tests
python tests/test_core.py
```

### 🤝 Contributing

Issues and PRs are welcome! Please follow these guidelines:

- **Issue**: Describe the problem, reproduction steps, expected behavior
- **PR**: Use Angular Commit convention (`feat:`, `fix:`, `docs:`, etc.)
- **Code Style**: Follow PEP 8, add type annotations

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

Made with ❤️ by NoteVault Team

</div>
