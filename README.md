# ArXiv Daily Chef 🍳

[English](#english) | [中文说明](#chinese)

<a name="english"></a>
## English

**ArXiv Daily Chef** is a streamlined research assistant designed for researchers to efficiently track, read, and organize ArXiv papers. Built with Streamlit, it allows users to subscribe to specific topics, automatically fetch the latest papers, and leverage Large Language Models (LLM) for instant summaries.

### ✨ Key Features

- **Topic Subscription**: Customize and manage your list of research topics (e.g., "LLM Agents", "Diffusion Models").
- **LLM Summarization**: Generate concise, easy-to-read summaries using popular LLMs (OpenAI, DeepSeek, Moonshot, GLM, SiliconFlow).
- **Visual Teaser**: Automatically extracts and displays the first figure/teaser image from the paper PDF for a quick visual overview.
- **Trend Radar**: Visualizes research hotspots with dynamic word clouds based on current paper batches.
- **Conference Tracker**: Tracks upcoming deadlines for major AI conferences, with filters for CCF rankings (A/B/C).
- **Favorites System**: Save and categorize important papers locally for future reference.
- **Code Available Badge**: Automatically detects if a paper has open-source code and provides direct links.
- **Multi-language UI**: Fully localized interface in English, Simplified Chinese, Traditional Chinese, Japanese, and Korean.
- **Theming**: Choose from multiple built-in themes (Light, Dark, Ocean, Forest) to suit your preference.

### 🚀 Quick Start

1.  **Clone the repository**
    ```bash
    git clone https://github.com/JayYu686/ArxivChef.git
    cd ArxivChef
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    streamlit run app.py
    ```

### ⚙️ Configuration

Once the app is running, use the **Sidebar** to configure:
- **API Settings**: Enter your LLM API Key and Base URL. Presets are available for OpenAI, DeepSeek, Moonshot (Kimi), and ZhipuGLM.
- **Language**: Switch the interface language.
- **Theme**: Toggle between different visual themes.

### ☁️ Deployment

You can deploy this app for free on **Streamlit Community Cloud**:

1.  Push your code to GitHub.
2.  Visit [share.streamlit.io](https://share.streamlit.io/).
3.  Click **New app** and select your repository (`ArxivChef`).
4.  Click **Deploy**!

> [!WARNING]
> **Data Persistence Warning**:
> By default, this app uses local JSON files (`topics.json`, `favorites.json`) to store data. On Streamlit Community Cloud, **files are reset when the app restarts**. Subscription lists and favorites will not be saved permanently in this version.

---

<a name="chinese"></a>
## 中文说明

**ArXiv Daily Chef (ArXiv 每日私厨)** 是一款专为科研人员打造的高效论文追踪工具。基于 Streamlit 开发，它能够帮助你订阅感兴趣的研究领域，自动拉取最新发布的 ArXiv 论文，并利用大语言模型（LLM）生成精准的中文摘要。

### ✨ 核心功能

- **领域订阅**: 灵活管理你关注的研究方向（如 "Large Language Models", "Computer Vision"），定制你的论文日报。
- **智能摘要**: 支持对接 OpenAI, DeepSeek, Kimi (Moonshot), 智谱 GLM 等大模型，一键生成论文核心摘要。
- **可视化预览**: 自动提取论文 PDF 中的首图（Teaser Image），让你在阅读摘要前先看图懂意，大幅提升筛选效率。
- **趋势雷达**: 基于当前拉取的论文摘要生成词云，直观展示当前领域的研究热点。
- **会议追踪**: 内置 AI 会议日历，实时显示即将截稿的顶级会议（支持 CCF A/B/C 类筛选）。
- **收藏夹**: 支持自定义分类收藏论文，构建你的本地科研知识库。
- **代码探测**:自动检测论文是否附带开源代码，并提供直接跳转链接。
- **多语言界面**: 界面支持简体中文、繁体中文、日文和韩文切换。
- **个性化主题**: 提供浅色、深色、海洋、森林等多种高颜值主题。

### 🚀 快速开始

1.  **克隆项目**
    ```bash
    git clone https://github.com/JayYu686/ArxivChef.git
    cd ArxivChef
    ```

2.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3.  **启动应用**
    ```bash
    streamlit run app.py
    ```

### ⚙️ 设置说明

启动应用后，在左侧边栏（Sidebar）可以进行配置：
- **API 设置**: 选择预设（如 DeepSeek, Kimi 等）或自定义配置，输入 API Key 即可使用 AI 摘要功能。
- **语言设置**: 切换界面显示语言。
- **主题设置**: 选择你喜欢的主题风格。

### ☁️ 部署指南

你可以将本项目免费部署到 **Streamlit Community Cloud**：

1.  确保代码已上传到 GitHub。
2.  访问 [share.streamlit.io](https://share.streamlit.io/) 并登录。
3.  点击 **New app**，选择你的仓库 (`ArxivChef`)。
4.  点击 **Deploy** 即可！

> [!WARNING]
> **数据持久化警告**:
> 当前版本默认使用本地 JSON 文件 (`topics.json`, `favorites.json`) 存储数据。在 Streamlit Community Cloud 上，**应用重启后（更新代码或长时间未访问）本地文件会被重置**。这意味着你的订阅列表和收藏夹可能会丢失。如需持久化存储，建议自行对接 MongoDB 或 Streamlit Secrets。

---
*Made with ❤️ by [JayYu686](https://github.com/JayYu686)*
