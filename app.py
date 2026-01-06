"""
ArXiv Daily Chef - ArXiv 每日私厨
帮助科研人员订阅领域、拉取最新论文并生成多语言 LLM 摘要的 Streamlit 应用
支持语言：简体中文、繁体中文、日文、韩文
功能：论文浏览、收藏夹、Visual Teaser、代码链接检测
"""

import streamlit as st
from utils.topic_manager import load_topics, add_topic, delete_topic
from utils.arxiv_fetcher import fetch_papers, ArxivFetchError
from utils.llm_summarizer import summarize_abstract, LLMSummarizeError
from utils.i18n import get_text, SUPPORTED_LANGUAGES
from utils.pdf_image_extractor import get_teaser_image, image_to_base64
from utils.favorites_manager import (
    add_favorite, remove_favorite, is_favorited, 
    get_categories, get_favorites_by_category, get_all_favorites,
    get_favorites_count, load_favorites
)
from utils.conference_tracker import get_upcoming_deadlines, check_paper_conference_match, format_countdown
from utils.hyperparam_extractor import extract_hyperparams_from_pdf
from utils.trend_radar import generate_trend_radar, get_top_keywords, WORDCLOUD_AVAILABLE


# ==================== 页面配置 ====================
st.set_page_config(
    page_title="Arxiv Daily Chef 🍳",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义样式 ====================
st.markdown("""
<style>
    /* ==================== 隐藏 Streamlit 内置元素 ==================== */
    .stDeployButton { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header[data-testid="stHeader"] { background: transparent !important; }
    
    /* ==================== 紧凑布局 ==================== */
    /* 主内容区域紧凑 */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1000px;
    }
    
    /* 论文标题缩小 */
    .main h3 {
        font-size: 1.1rem !important;
        margin-bottom: 0.3rem !important;
        line-height: 1.3 !important;
    }
    
    /* 论文元信息更小 */
    .stCaption {
        font-size: 0.75rem !important;
    }
    
    /* 按钮更小 */
    .stButton > button {
        font-size: 0.8rem !important;
        padding: 0.3rem 0.8rem !important;
        border-radius: 16px;
    }
    
    /* 分隔线更细 */
    hr {
        margin: 0.5rem 0 !important;
    }
    
    /* ==================== 图片严格限制 ==================== */
    .stImage > img {
        max-height: 180px !important;
        max-width: 400px !important;
        object-fit: contain;
    }
    
    .element-container:has(.stImage) {
        display: flex;
        justify-content: center;
    }
    
    /* ==================== 应用样式 ==================== */
    .main-title {
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    .code-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 6px;
        text-decoration: none;
    }
    
    .code-badge:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: white;
    }
    
    /* Expander 内容更紧凑 */
    .streamlit-expanderContent {
        padding: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 初始化 Session State ====================
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = None
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = {}
if "teasers" not in st.session_state:
    st.session_state.teasers = {}
if "lang" not in st.session_state:
    st.session_state.lang = "zh-CN"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "browse"
if "selected_fav_category" not in st.session_state:
    st.session_state.selected_fav_category = None
if "hyperparams" not in st.session_state:
    st.session_state.hyperparams = {}
if "theme" not in st.session_state:
    st.session_state.theme = "light"  # light, dark, ocean, forest


# ==================== 主题配置 ====================
THEMES = {
    "light": {
        "name": "☀️ 浅色 / Light",
        "bg": "#ffffff",
        "secondary_bg": "#f8f9fa",
        "text": "#1a1a2e",
        "accent": "#ff6b6b",
        "card_bg": "#f0f2f6",
    },
    "dark": {
        "name": "🌙 深色 / Dark",
        "bg": "#0e1117",
        "secondary_bg": "#1a1a2e",
        "text": "#fafafa",
        "accent": "#ff6b6b",
        "card_bg": "#262730",
    },
    "ocean": {
        "name": "🌊 海洋 / Ocean",
        "bg": "#0a192f",
        "secondary_bg": "#112240",
        "text": "#ccd6f6",
        "accent": "#64ffda",
        "card_bg": "#1d3557",
    },
    "forest": {
        "name": "🌲 森林 / Forest",
        "bg": "#1a1c16",
        "secondary_bg": "#2d321c",
        "text": "#e8e6e3",
        "accent": "#a3be8c",
        "card_bg": "#3b4025",
    },
}

# 获取当前主题
current_theme = THEMES.get(st.session_state.theme, THEMES["light"])
th = current_theme  # 简写

# ==================== 动态样式（真正的主题切换）====================
st.markdown(f"""
<style>
    /* 隐藏 Streamlit 元素 */
    .stDeployButton, #MainMenu, footer {{ display: none !important; }}
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    
    /* ==================== 主题颜色覆盖 ==================== */
    /* 主背景 */
    .stApp, .main {{
        background-color: {th['bg']} !important;
    }}
    
    /* 侧边栏背景 */
    section[data-testid="stSidebar"] {{
        background-color: {th['secondary_bg']} !important;
    }}
    section[data-testid="stSidebar"] > div {{
        background-color: {th['secondary_bg']} !important;
    }}
    
    /* 所有文字颜色 */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label,
    .stMarkdown, .stMarkdown p, h1, h2, h3, h4, h5, h6,
    .stCaption, .stTextInput label, .stSelectbox label {{
        color: {th['text']} !important;
    }}
    
    /* 输入框 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
        border-color: {th['accent']}44 !important;
    }}
    
    /* 按钮 */
    .stButton > button {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
        border: 1px solid {th['accent']}66 !important;
    }}
    .stButton > button:hover {{
        background-color: {th['accent']}33 !important;
        border-color: {th['accent']} !important;
    }}
    .stButton > button[kind="primary"] {{
        background-color: {th['accent']} !important;
        color: white !important;
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
    }}
    .streamlit-expanderContent {{
        background-color: {th['secondary_bg']} !important;
    }}
    
    /* 信息框 */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {{
        background-color: {th['card_bg']} !important;
        color: {th['text']} !important;
    }}
    
    /* 分隔线 */
    hr {{
        border-color: {th['text']}22 !important;
    }}
    
    /* ==================== 超紧凑布局 ==================== */
    .main .block-container {{
        padding: 0.5rem 1rem !important;
        max-width: 900px;
    }}
    
    .main h3 {{
        font-size: 0.95rem !important;
        margin: 0.2rem 0 !important;
        line-height: 1.2 !important;
    }}
    
    .stCaption {{ font-size: 0.7rem !important; }}
    p {{ font-size: 0.85rem !important; margin: 0.2rem 0 !important; }}
    
    .stButton > button {{
        font-size: 0.75rem !important;
        padding: 0.2rem 0.6rem !important;
        border-radius: 12px;
        min-height: 0 !important;
    }}
    
    hr {{ margin: 0.3rem 0 !important; border-width: 1px !important; }}
    
    .stImage > img {{
        max-height: 150px !important;
        max-width: 350px !important;
        object-fit: contain;
    }}
    
    .element-container:has(.stImage) {{
        display: flex;
        justify-content: center;
    }}
    
    .streamlit-expanderContent {{ padding: 0.3rem !important; }}
    .streamlit-expanderHeader {{ font-size: 0.85rem !important; }}
    
    .stTextInput > div > div > input {{
        padding: 0.3rem 0.5rem !important;
        font-size: 0.8rem !important;
    }}
    
    .stSelectbox > div > div {{ font-size: 0.8rem !important; }}
    
    /* ==================== 应用样式 ==================== */
    .main-title {{
        background: linear-gradient(90deg, {th['accent']}, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.6rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.2rem;
    }}
    
    .sub-title {{
        text-align: center;
        color: {th['text']}88 !important;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
    }}
    
    .code-badge {{
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1px 6px;
        border-radius: 8px;
        font-size: 0.65rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 4px;
        text-decoration: none;
    }}
    
    /* 侧边栏紧凑 */
    section[data-testid="stSidebar"] .block-container {{
        padding: 0.5rem !important;
    }}
    
    section[data-testid="stSidebar"] .stButton > button {{
        font-size: 0.7rem !important;
        padding: 0.15rem 0.4rem !important;
    }}
</style>
""", unsafe_allow_html=True)


# ==================== 辅助函数 ====================
def t(key: str, **kwargs) -> str:
    """获取当前语言的翻译文本"""
    return get_text(key, st.session_state.lang, **kwargs)


def render_paper_card(paper, show_favorite_btn=True, is_favorite_view=False, fav_category=None):
    """渲染单个论文卡片"""
    # 统一提取论文字段，支持 dict 和 dataclass 两种格式
    if isinstance(paper, dict):
        title = paper.get('title', '')
        url = paper.get('url', '')
        arxiv_id = paper.get('arxiv_id', '')
        authors = paper.get('authors', [])
        abstract = paper.get('abstract', '')
        published = paper.get('published', '')
        code_urls = paper.get('code_urls', [])
        favorited_at = paper.get('favorited_at', '')
    else:
        title = paper.title
        url = paper.url
        arxiv_id = paper.arxiv_id
        authors = paper.authors
        abstract = paper.abstract
        published = paper.published
        code_urls = paper.code_urls if hasattr(paper, 'code_urls') else []
        favorited_at = ''
    
    with st.container():
        st.markdown("---")
        
        # 标题行：标题 + 收藏按钮
        col_title, col_fav = st.columns([6, 1])
        
        with col_title:
            st.markdown(f"### [{title}]({url})")
        
        with col_fav:
            if show_favorite_btn:
                is_fav, fav_cat = is_favorited(arxiv_id)
                
                if is_fav:
                    if st.button("💛", key=f"unfav_{arxiv_id}", help=t("remove_from_favorites")):
                        remove_favorite(arxiv_id, fav_cat)
                        st.toast(t("unfavorite_success"))
                        st.rerun()
                else:
                    if st.button("⭐", key=f"fav_{arxiv_id}", help=t("add_to_favorites")):
                        # 获取当前领域作为默认分类
                        category = st.session_state.selected_topic or "未分类"
                        add_favorite(
                            arxiv_id=arxiv_id,
                            title=title,
                            authors=authors,
                            abstract=abstract,
                            url=url,
                            published=published,
                            category=category,
                            code_urls=code_urls
                        )
                        st.toast(t("favorite_success"))
                        st.rerun()
        
        # CODE AVAILABLE 按钮
        if code_urls:
            code_links_html = " ".join([
                f'<a href="{u}" target="_blank" class="code-badge">🟢 CODE AVAILABLE</a>'
                for u in code_urls[:3]
            ])
            st.markdown(code_links_html, unsafe_allow_html=True)
        
        # 元信息
        col1, col2 = st.columns([2, 1])
        
        with col1:
            authors_display = ", ".join(authors[:3]) if authors else ""
            if len(authors) > 3:
                authors_display += " " + t("authors_et_al", count=len(authors))
            st.caption(f"👤 {authors_display}")
        with col2:
            if is_favorite_view and favorited_at:
                st.caption(f"📅 {published} | ⭐ {t('favorited_at', time=favorited_at)}")
            else:
                st.caption(f"📅 {published} | 🔖 {arxiv_id}")
        
        # 摘要
        with st.expander(t("view_abstract")):
            st.write(abstract)
        
        # Teaser 图片（仅浏览模式）
        if not is_favorite_view:
            teaser_key = arxiv_id
            
            if teaser_key in st.session_state.teasers:
                teaser_data = st.session_state.teasers[teaser_key]
                if teaser_data:
                    st.markdown(f"**{t('teaser_title')}**")
                    st.image(teaser_data, use_container_width=True)
                else:
                    st.caption(t("teaser_not_found"))
            else:
                if st.button(t("load_teaser"), key=f"teaser_{arxiv_id}"):
                    with st.spinner(t("loading_teaser")):
                        try:
                            teaser_bytes = get_teaser_image(url, arxiv_id)
                            st.session_state.teasers[teaser_key] = teaser_bytes if teaser_bytes else None
                            st.rerun()
                        except Exception:
                            st.session_state.teasers[teaser_key] = None
                            st.warning(t("teaser_not_found"))
        
        # ==================== Hyperparam Spy (参数显微镜) ====================
        # 显示超参数提取按钮（需要 API Key）
        hyperparam_key = arxiv_id
        
        if hyperparam_key in st.session_state.hyperparams:
            # 已有缓存结果
            hyperparam_result = st.session_state.hyperparams[hyperparam_key]
            if hyperparam_result:
                st.markdown(t("hyperparam_title"))
                st.info(hyperparam_result)
            else:
                st.caption(t("hyperparam_failed"))


# ==================== 侧边栏 ====================
with st.sidebar:
    # ==================== 语言和主题设置（始终可见）====================
    col_lang, col_theme = st.columns(2)
    
    with col_lang:
        st.caption(t("language_settings"))
        lang_options = list(SUPPORTED_LANGUAGES.keys())
        lang_labels = list(SUPPORTED_LANGUAGES.values())
        current_lang_idx = lang_options.index(st.session_state.lang) if st.session_state.lang in lang_options else 0
        
        selected_lang_label = st.selectbox(
            "Language",
            lang_labels,
            index=current_lang_idx,
            label_visibility="collapsed",
            key="lang_select"
        )
        
        new_lang = lang_options[lang_labels.index(selected_lang_label)]
        if new_lang != st.session_state.lang:
            st.session_state.lang = new_lang
            st.session_state.summaries = {}
            st.rerun()
    
    with col_theme:
        st.caption("🎨 Theme")
        theme_keys = list(THEMES.keys())
        theme_names = [THEMES[k]["name"] for k in theme_keys]
        current_theme_idx = theme_keys.index(st.session_state.theme) if st.session_state.theme in theme_keys else 0
        
        selected_theme_name = st.selectbox(
            "Theme",
            theme_names,
            index=current_theme_idx,
            label_visibility="collapsed",
            key="theme_select"
        )
        
        new_theme = theme_keys[theme_names.index(selected_theme_name)]
        if new_theme != st.session_state.theme:
            st.session_state.theme = new_theme
            st.rerun()
    
    st.divider()
    
    # ==================== 查看模式切换（始终可见）====================
    view_col1, view_col2 = st.columns(2)
    with view_col1:
        if st.button(t("browse_papers"), use_container_width=True, 
                     type="primary" if st.session_state.view_mode == "browse" else "secondary"):
            st.session_state.view_mode = "browse"
            st.rerun()
    with view_col2:
        fav_count = get_favorites_count()
        btn_label = f"{t('my_favorites')} ({fav_count})"
        if st.button(btn_label, use_container_width=True,
                     type="primary" if st.session_state.view_mode == "favorites" else "secondary"):
            st.session_state.view_mode = "favorites"
            st.rerun()
    
    st.divider()
    
    # ==================== 会议日历（可折叠）====================
    with st.expander(t("conference_tracker"), expanded=False):
        # CCF 等级筛选
        ccf_cols = st.columns(4)
        ccf_filter = None
        with ccf_cols[0]:
            if st.button(t("all_ranks"), key="ccf_all", use_container_width=True):
                ccf_filter = None
        with ccf_cols[1]:
            if st.button("🅰️ A", key="ccf_a", use_container_width=True):
                ccf_filter = "A"
        with ccf_cols[2]:
            if st.button("🅱️ B", key="ccf_b", use_container_width=True):
                ccf_filter = "B"
        with ccf_cols[3]:
            if st.button("©️ C", key="ccf_c", use_container_width=True):
                ccf_filter = "C"
        
        # 获取会议列表
        # 获取会议列表 - 显示更多
        upcoming = get_upcoming_deadlines(limit=15, ccf_filter=ccf_filter)
        
        if not upcoming:
            st.caption("No upcoming deadlines")
        
        for deadline in upcoming:
            days = deadline.days_left
            if days < 0:
                color = "gray"
                countdown = t("days_ago", days=abs(days))
            elif days == 0:
                color = "red"
                countdown = t("today")
            elif days <= 7:
                color = "red"
                countdown = t("days_left", days=days)
            elif days <= 30:
                color = "orange"
                countdown = t("days_left", days=days)
            else:
                color = "green"
                countdown = t("days_left", days=days)
            
            # 显示带 CCF 徽章
            st.markdown(
                f"{deadline.rank_badge} **{deadline.conference}**  \n"
                f":{color}[{countdown}] {deadline.event} · {deadline.deadline.strftime('%m-%d')}"
            )
    
    # ==================== API 设置（可折叠）====================
    with st.expander(t("api_settings"), expanded=False):
        # API 预设选项
        api_presets = {
            "OpenAI": ("https://api.openai.com/v1", "gpt-4o-mini"),
            "DeepSeek": ("https://api.deepseek.com/v1", "deepseek-chat"),
            "Moonshot (Kimi)": ("https://api.moonshot.cn/v1", "moonshot-v1-8k"),
            "GLM (ZhipuAI)": ("https://open.bigmodel.cn/api/paas/v4", "glm-4-flash"),
            "SiliconFlow": ("https://api.siliconflow.cn/v1", "Qwen/Qwen2.5-7B-Instruct"),
        }
        
        preset_names = ["自定义 / Custom"] + list(api_presets.keys())
        selected_preset = st.selectbox(
            "🔧 API 预设 / Preset",
            preset_names,
            index=0,
            help="选择预设自动填充 Base URL 和 Model"
        )
        
        # 根据预设设置默认值
        if selected_preset in api_presets:
            default_url, default_model = api_presets[selected_preset]
        else:
            default_url = "https://api.openai.com/v1"
            default_model = "gpt-3.5-turbo"
        
        base_url = st.text_input(
            t("base_url"),
            value=default_url,
            help="API 地址。如果使用预设，会自动填充。",
            key="sidebar_base_url"
        )
        
        api_key = st.text_input(
            t("api_key"),
            type="password",
            placeholder="sk-... 或 你的 API Key",
            help="从 API 提供商获取的密钥",
            key="sidebar_api_key"
        )
        
        model_name = st.text_input(
            t("model"),
            value=default_model,
            help="模型名称。如果使用预设，会自动填充。",
            key="sidebar_model"
        )
        
        st.caption("💡 提示: 选择预设后只需填写 API Key 即可使用")
    
    # ==================== 领域订阅管理（可折叠，仅浏览模式）====================
    if st.session_state.view_mode == "browse":
        with st.expander(t("subscribe_topics"), expanded=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                new_topic = st.text_input(
                    "添加领域",
                    placeholder=t("add_topic_placeholder"),
                    label_visibility="collapsed"
                )
            with col2:
                add_btn = st.button("➕", help="添加领域")
            
            if add_btn and new_topic:
                success, msg = add_topic(new_topic)
                if success:
                    st.success(t("topic_added", topic=new_topic))
                    st.rerun()
                else:
                    if "已存在" in msg or "exists" in msg.lower():
                        st.warning(t("topic_exists", topic=new_topic))
                    else:
                        st.warning(t("topic_empty"))
            
            topics = load_topics()
            
            if topics:
                st.caption(t("subscribed_count", count=len(topics)))
                
                for topic in topics:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        if st.button(f"🏷️ {topic}", key=f"topic_{topic}", use_container_width=True):
                            st.session_state.selected_topic = topic
                            st.session_state.papers = []
                            st.session_state.summaries = {}
                    with col2:
                        if st.button("🗑️", key=f"del_{topic}", help=f"删除 {topic}"):
                            success, msg = delete_topic(topic)
                            if success:
                                if st.session_state.selected_topic == topic:
                                    st.session_state.selected_topic = None
                                st.rerun()
            else:
                st.info(t("no_topics_hint"))
    
    # ==================== 收藏夹分类（可折叠，仅收藏模式）====================
    else:
        with st.expander(t("favorites"), expanded=True):
            categories = get_categories()
            
            # 全部收藏按钮
            if st.button(f"📁 {t('all_favorites')}", key="all_fav", use_container_width=True):
                st.session_state.selected_fav_category = None
                st.rerun()
            
            # 分类列表
            if categories:
                st.caption(t("favorites_count", count=get_favorites_count()))
                for cat in categories:
                    cat_papers = get_favorites_by_category(cat)
                    if st.button(f"📂 {cat} ({len(cat_papers)})", key=f"fav_cat_{cat}", use_container_width=True):
                        st.session_state.selected_fav_category = cat
                        st.rerun()
    
    st.divider()
    st.caption(t("made_with_love"))


# ==================== 主界面 ====================
st.markdown(f'<p class="main-title">{t("app_title")}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">{t("app_subtitle")}</p>', unsafe_allow_html=True)


# ==================== 收藏夹模式 ====================
if st.session_state.view_mode == "favorites":
    if st.session_state.selected_fav_category:
        st.subheader(f"📂 {st.session_state.selected_fav_category}")
        fav_papers = get_favorites_by_category(st.session_state.selected_fav_category)
    else:
        st.subheader(t("all_favorites"))
        fav_papers = get_all_favorites()
    
    if fav_papers:
        st.success(t("favorites_count", count=len(fav_papers)))
        for paper in fav_papers:
            render_paper_card(paper, show_favorite_btn=True, is_favorite_view=True)
    else:
        st.info(t("favorites_empty"))


# ==================== 浏览论文模式 ====================
else:
    if not st.session_state.selected_topic:
        st.info(t("welcome_hint"))
        
        with st.expander(t("quick_start"), expanded=True):
            st.markdown(t("quick_start_content"))
    else:
        st.subheader(t("topic_label", topic=st.session_state.selected_topic))
        
        # 论文数量选择（包含自定义选项）
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            fetch_btn = st.button(t("refresh_papers"), type="primary")
        with col2:
            count_option = st.selectbox(
                t("paper_count_label"),
                ["5", "10", "15", "20", t("paper_count_custom")],
                index=0,
                label_visibility="collapsed"
            )
        with col3:
            if count_option == t("paper_count_custom"):
                paper_count = st.number_input(
                    t("paper_count_input"),
                    min_value=1,
                    max_value=50,
                    value=10,
                    label_visibility="collapsed"
                )
            else:
                paper_count = int(count_option)
        
        # 拉取论文
        if fetch_btn or not st.session_state.papers:
            with st.spinner(t("fetching_papers", topic=st.session_state.selected_topic)):
                try:
                    papers = fetch_papers(st.session_state.selected_topic, max_results=paper_count)
                    st.session_state.papers = papers
                    st.session_state.summaries = {}
                    if not papers:
                        st.warning(t("no_papers_found", topic=st.session_state.selected_topic))
                except ArxivFetchError as e:
                    st.error(f"⚠️ {str(e)}")
                    st.session_state.papers = []
        
        # 显示论文列表
        if st.session_state.papers:
            st.success(t("papers_found", count=len(st.session_state.papers)))
            
            # ==================== Trend Radar 词云 ====================
            with st.expander(t("trend_radar"), expanded=True):
                st.caption(t("trend_radar_desc"))
                
                if WORDCLOUD_AVAILABLE:
                    # 收集所有摘要
                    abstracts = [paper.abstract for paper in st.session_state.papers]
                    
                    # 生成词云
                    wordcloud_bytes = generate_trend_radar(abstracts, colormap='viridis')
                    
                    if wordcloud_bytes:
                        st.image(wordcloud_bytes, use_container_width=True)
                        
                        # 显示热门关键词列表
                        top_kw = get_top_keywords(abstracts, top_n=8)
                        if top_kw:
                            kw_text = " | ".join([f"**{word}** ({count})" for word, count in top_kw])
                            st.markdown(f"{t('top_keywords')}: {kw_text}")
                    else:
                        st.info("No keywords extracted from papers")
                else:
                    st.warning(t("wordcloud_not_available"))
            
            st.markdown("---")
            
            for paper in st.session_state.papers:
                render_paper_card(paper, show_favorite_btn=True, is_favorite_view=False)
                
                # LLM 摘要区域
                summary_key = f"{paper.arxiv_id}_{st.session_state.lang}"
                
                if summary_key in st.session_state.summaries:
                    st.markdown(t("ai_summary_title"))
                    st.info(st.session_state.summaries[summary_key])
                else:
                    # 摘要和超参数提取按钮并排
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button(t("generate_summary"), key=f"sum_{paper.arxiv_id}"):
                            if not api_key:
                                st.warning(t("error_no_api_key"))
                            else:
                                with st.spinner(t("generating_summary")):
                                    try:
                                        summary = summarize_abstract(
                                            abstract=paper.abstract,
                                            api_key=api_key,
                                            base_url=base_url,
                                            model=model_name,
                                            lang=st.session_state.lang
                                        )
                                        st.session_state.summaries[summary_key] = summary
                                        st.rerun()
                                    except LLMSummarizeError as e:
                                        st.error(f"⚠️ {str(e)}")
                    
                    with btn_col2:
                        hyperparam_key = paper.arxiv_id
                        if hyperparam_key not in st.session_state.hyperparams:
                            if st.button(t("hyperparam_spy"), key=f"hp_{paper.arxiv_id}"):
                                if not api_key:
                                    st.warning(t("error_no_api_key"))
                                else:
                                    with st.spinner(t("extracting_hyperparams")):
                                        try:
                                            result = extract_hyperparams_from_pdf(
                                                arxiv_url=paper.url,
                                                arxiv_id=paper.arxiv_id,
                                                api_key=api_key,
                                                base_url=base_url,
                                                model=model_name,
                                                lang=st.session_state.lang
                                            )
                                            st.session_state.hyperparams[hyperparam_key] = result
                                            st.rerun()
                                        except Exception as e:
                                            st.session_state.hyperparams[hyperparam_key] = None
                                            st.error(t("hyperparam_failed"))
            
            # 批量生成摘要
            st.markdown("---")
            if st.button(t("generate_all_summaries"), type="secondary"):
                if not api_key:
                    st.warning(t("error_no_api_key"))
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, paper in enumerate(st.session_state.papers):
                        summary_key = f"{paper.arxiv_id}_{st.session_state.lang}"
                        if summary_key not in st.session_state.summaries:
                            status_text.text(t("processing_paper", title=paper.title[:50]))
                            try:
                                summary = summarize_abstract(
                                    abstract=paper.abstract,
                                    api_key=api_key,
                                    base_url=base_url,
                                    model=model_name,
                                    lang=st.session_state.lang
                                )
                                st.session_state.summaries[summary_key] = summary
                            except LLMSummarizeError as e:
                                st.session_state.summaries[summary_key] = t("summary_failed", error=str(e))
                        
                        progress_bar.progress((i + 1) / len(st.session_state.papers))
                    
                    status_text.text(t("all_summaries_done"))
                    st.rerun()
