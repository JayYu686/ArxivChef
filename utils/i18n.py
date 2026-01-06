"""
国际化 (i18n) 模块
支持简体中文、繁体中文、日文、韩文、英文界面
"""

from typing import Dict

# 支持的语言列表
SUPPORTED_LANGUAGES = {
    "en": "English",
    "zh-CN": "简体中文",
    "zh-TW": "繁體中文",
    "ja": "日本語",
    "ko": "한국어"
}

# 翻译字典
TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # ==================== 页面标题和描述 ====================
    "app_title": {
        "zh-CN": "🍳 ArXiv Daily Chef",
        "zh-TW": "🍳 ArXiv Daily Chef",
        "ja": "🍳 ArXiv Daily Chef",
        "ko": "🍳 ArXiv Daily Chef"
    },
    "app_subtitle": {
        "zh-CN": "你的论文私人主厨，每日精选最新研究",
        "zh-TW": "你的論文私人主廚，每日精選最新研究",
        "ja": "あなたの論文プライベートシェフ、毎日最新研究をお届け",
        "ko": "당신의 논문 프라이빗 셰프, 매일 최신 연구를 선별"
    },
    
    # ==================== 侧边栏 - API 设置 ====================
    "api_settings": {
        "zh-CN": "⚙️ API 设置",
        "zh-TW": "⚙️ API 設置",
        "ja": "⚙️ API 設定",
        "ko": "⚙️ API 설정"
    },
    "base_url": {
        "zh-CN": "Base URL",
        "zh-TW": "Base URL",
        "ja": "Base URL",
        "ko": "Base URL"
    },
    "base_url_help": {
        "zh-CN": "OpenAI 兼容 API 地址，如 DeepSeek、Moonshot 等",
        "zh-TW": "OpenAI 兼容 API 地址，如 DeepSeek、Moonshot 等",
        "ja": "OpenAI互換APIアドレス（DeepSeek、Moonshotなど）",
        "ko": "OpenAI 호환 API 주소 (DeepSeek, Moonshot 등)"
    },
    "api_key": {
        "zh-CN": "API Key",
        "zh-TW": "API Key",
        "ja": "API Key",
        "ko": "API Key"
    },
    "api_key_help": {
        "zh-CN": "你的 API 密钥",
        "zh-TW": "你的 API 密鑰",
        "ja": "あなたのAPIキー",
        "ko": "당신의 API 키"
    },
    "model": {
        "zh-CN": "Model",
        "zh-TW": "Model",
        "ja": "Model",
        "ko": "Model"
    },
    "model_help": {
        "zh-CN": "模型名称，如 gpt-4, deepseek-chat 等",
        "zh-TW": "模型名稱，如 gpt-4, deepseek-chat 等",
        "ja": "モデル名（gpt-4、deepseek-chatなど）",
        "ko": "모델 이름 (gpt-4, deepseek-chat 등)"
    },
    
    # ==================== 侧边栏 - 语言设置 ====================
    "language_settings": {
        "zh-CN": "🌐 语言设置",
        "zh-TW": "🌐 語言設置",
        "ja": "🌐 言語設定",
        "ko": "🌐 언어 설정"
    },
    
    # ==================== 侧边栏 - 订阅领域 ====================
    "subscribe_topics": {
        "zh-CN": "📚 订阅领域",
        "zh-TW": "📚 訂閱領域",
        "ja": "📚 購読分野",
        "ko": "📚 구독 분야"
    },
    "add_topic_placeholder": {
        "zh-CN": "如: Point Cloud",
        "zh-TW": "如: Point Cloud",
        "ja": "例: Point Cloud",
        "ko": "예: Point Cloud"
    },
    "subscribed_count": {
        "zh-CN": "已订阅 {count} 个领域",
        "zh-TW": "已訂閱 {count} 個領域",
        "ja": "{count} 分野を購読中",
        "ko": "{count}개 분야 구독 중"
    },
    "no_topics_hint": {
        "zh-CN": "👆 请添加你感兴趣的领域",
        "zh-TW": "👆 請添加你感興趣的領域",
        "ja": "👆 興味のある分野を追加してください",
        "ko": "👆 관심 분야를 추가해주세요"
    },
    "topic_exists": {
        "zh-CN": "领域 '{topic}' 已存在",
        "zh-TW": "領域 '{topic}' 已存在",
        "ja": "分野 '{topic}' は既に存在します",
        "ko": "분야 '{topic}'이(가) 이미 존재합니다"
    },
    "topic_added": {
        "zh-CN": "成功添加领域: {topic}",
        "zh-TW": "成功添加領域: {topic}",
        "ja": "分野を追加しました: {topic}",
        "ko": "분야 추가 완료: {topic}"
    },
    "topic_empty": {
        "zh-CN": "领域名称不能为空",
        "zh-TW": "領域名稱不能為空",
        "ja": "分野名を入力してください",
        "ko": "분야 이름을 입력해주세요"
    },
    
    # ==================== 主界面 - 欢迎信息 ====================
    "welcome_hint": {
        "zh-CN": "👈 请在左侧添加并选择一个领域，开始探索最新论文！",
        "zh-TW": "👈 請在左側添加並選擇一個領域，開始探索最新論文！",
        "ja": "👈 左側で分野を追加・選択して、最新論文を探索しましょう！",
        "ko": "👈 왼쪽에서 분야를 추가하고 선택하여 최신 논문을 탐색하세요!"
    },
    "quick_start": {
        "zh-CN": "🚀 快速入门",
        "zh-TW": "🚀 快速入門",
        "ja": "🚀 クイックスタート",
        "ko": "🚀 빠른 시작"
    },
    "quick_start_content": {
        "zh-CN": """**使用步骤：**
1. 在左侧**配置 API**（支持 OpenAI、DeepSeek、Moonshot 等兼容接口）
2. 输入感兴趣的领域关键词，点击 ➕ 添加
3. 点击领域标签，拉取最新论文
4. 点击「生成摘要」按钮，获取 AI 中文解读

**推荐关键词：**
- `Point Cloud` - 点云处理
- `3D Gaussian Splatting` - 3D 高斯泼溅
- `LLM Agents` - 大语言模型智能体
- `Neural Radiance Fields` - 神经辐射场""",
        "zh-TW": """**使用步驟：**
1. 在左側**配置 API**（支持 OpenAI、DeepSeek、Moonshot 等兼容接口）
2. 輸入感興趣的領域關鍵詞，點擊 ➕ 添加
3. 點擊領域標籤，拉取最新論文
4. 點擊「生成摘要」按鈕，獲取 AI 中文解讀

**推薦關鍵詞：**
- `Point Cloud` - 點雲處理
- `3D Gaussian Splatting` - 3D 高斯潑濺
- `LLM Agents` - 大語言模型智能體
- `Neural Radiance Fields` - 神經輻射場""",
        "ja": """**使い方：**
1. 左側で**APIを設定**（OpenAI、DeepSeek、Moonshot等の互換インターフェースに対応）
2. 興味のある分野のキーワードを入力し、➕をクリックして追加
3. 分野タグをクリックして最新論文を取得
4. 「要約を生成」ボタンをクリックしてAI解説を取得

**おすすめキーワード：**
- `Point Cloud` - 点群処理
- `3D Gaussian Splatting` - 3Dガウシアンスプラッティング
- `LLM Agents` - 大規模言語モデルエージェント
- `Neural Radiance Fields` - ニューラル放射場""",
        "ko": """**사용 방법:**
1. 왼쪽에서 **API 설정** (OpenAI, DeepSeek, Moonshot 등 호환 인터페이스 지원)
2. 관심 분야 키워드를 입력하고 ➕를 클릭하여 추가
3. 분야 태그를 클릭하여 최신 논문 가져오기
4. 「요약 생성」 버튼을 클릭하여 AI 해설 받기

**추천 키워드:**
- `Point Cloud` - 포인트 클라우드 처리
- `3D Gaussian Splatting` - 3D 가우시안 스플래팅
- `LLM Agents` - 대규모 언어 모델 에이전트
- `Neural Radiance Fields` - 신경 방사장"""
    },
    
    # ==================== 主界面 - 论文展示 ====================
    "topic_label": {
        "zh-CN": "📖 领域: {topic}",
        "zh-TW": "📖 領域: {topic}",
        "ja": "📖 分野: {topic}",
        "ko": "📖 분야: {topic}"
    },
    "refresh_papers": {
        "zh-CN": "🔄 刷新论文",
        "zh-TW": "🔄 刷新論文",
        "ja": "🔄 論文を更新",
        "ko": "🔄 논문 새로고침"
    },
    "paper_count": {
        "zh-CN": "论文数量",
        "zh-TW": "論文數量",
        "ja": "論文数",
        "ko": "논문 수"
    },
    "fetching_papers": {
        "zh-CN": "正在从 ArXiv 拉取 {topic} 相关论文...",
        "zh-TW": "正在從 ArXiv 拉取 {topic} 相關論文...",
        "ja": "ArXivから {topic} 関連論文を取得中...",
        "ko": "ArXiv에서 {topic} 관련 논문을 가져오는 중..."
    },
    "no_papers_found": {
        "zh-CN": "未找到与「{topic}」相关的论文",
        "zh-TW": "未找到與「{topic}」相關的論文",
        "ja": "「{topic}」に関連する論文が見つかりませんでした",
        "ko": "「{topic}」 관련 논문을 찾을 수 없습니다"
    },
    "papers_found": {
        "zh-CN": "✅ 找到 {count} 篇最新论文",
        "zh-TW": "✅ 找到 {count} 篇最新論文",
        "ja": "✅ 最新論文 {count} 件を取得しました",
        "ko": "✅ 최신 논문 {count}편을 찾았습니다"
    },
    "authors_et_al": {
        "zh-CN": "等 {count} 人",
        "zh-TW": "等 {count} 人",
        "ja": "他 {count} 名",
        "ko": "외 {count}명"
    },
    "view_abstract": {
        "zh-CN": "📄 查看原始摘要 (English)",
        "zh-TW": "📄 查看原始摘要 (English)",
        "ja": "📄 原文アブストラクトを表示 (English)",
        "ko": "📄 원문 초록 보기 (English)"
    },
    "code_available": {
        "zh-CN": "🟢 CODE AVAILABLE",
        "zh-TW": "🟢 CODE AVAILABLE",
        "ja": "🟢 CODE AVAILABLE",
        "ko": "🟢 CODE AVAILABLE"
    },
    
    # ==================== LLM 摘要 ====================
    "ai_summary_title": {
        "zh-CN": "**🤖 AI 中文解读：**",
        "zh-TW": "**🤖 AI 中文解讀：**",
        "ja": "**🤖 AI日本語解説：**",
        "ko": "**🤖 AI 한국어 해설:**"
    },
    "generate_summary": {
        "zh-CN": "✨ 生成 AI 摘要",
        "zh-TW": "✨ 生成 AI 摘要",
        "ja": "✨ AI要約を生成",
        "ko": "✨ AI 요약 생성"
    },
    "generating_summary": {
        "zh-CN": "AI 正在解读论文...",
        "zh-TW": "AI 正在解讀論文...",
        "ja": "AIが論文を解説中...",
        "ko": "AI가 논문을 해설하는 중..."
    },
    "generate_all_summaries": {
        "zh-CN": "🚀 一键生成所有摘要",
        "zh-TW": "🚀 一鍵生成所有摘要",
        "ja": "🚀 全ての要約を一括生成",
        "ko": "🚀 모든 요약 한 번에 생성"
    },
    "processing_paper": {
        "zh-CN": "正在处理: {title}...",
        "zh-TW": "正在處理: {title}...",
        "ja": "処理中: {title}...",
        "ko": "처리 중: {title}..."
    },
    "all_summaries_done": {
        "zh-CN": "✅ 所有摘要生成完成！",
        "zh-TW": "✅ 所有摘要生成完成！",
        "ja": "✅ 全ての要約が完了しました！",
        "ko": "✅ 모든 요약 생성 완료!"
    },
    "summary_failed": {
        "zh-CN": "❌ 生成失败: {error}",
        "zh-TW": "❌ 生成失敗: {error}",
        "ja": "❌ 生成失敗: {error}",
        "ko": "❌ 생성 실패: {error}"
    },
    
    # ==================== Visual Teaser (论文图片预览) ====================
    "load_teaser": {
        "zh-CN": "🖼️ 加载论文配图",
        "zh-TW": "🖼️ 載入論文配圖",
        "ja": "🖼️ 論文の図を読み込む",
        "ko": "🖼️ 논문 이미지 로드"
    },
    "loading_teaser": {
        "zh-CN": "正在下载 PDF 并提取配图...",
        "zh-TW": "正在下載 PDF 並提取配圖...",
        "ja": "PDFをダウンロードし図を抽出中...",
        "ko": "PDF 다운로드 및 이미지 추출 중..."
    },
    "teaser_title": {
        "zh-CN": "📸 论文配图 (Teaser/架构图)",
        "zh-TW": "📸 論文配圖 (Teaser/架構圖)",
        "ja": "📸 論文の図 (Teaser/アーキテクチャ図)",
        "ko": "📸 논문 이미지 (Teaser/아키텍처)"
    },
    "teaser_not_found": {
        "zh-CN": "未能提取到配图（PDF 可能无图或下载失败）",
        "zh-TW": "未能提取到配圖（PDF 可能無圖或下載失敗）",
        "ja": "図を抽出できませんでした（PDFに図がないか、ダウンロード失敗）",
        "ko": "이미지를 추출할 수 없습니다 (PDF에 이미지가 없거나 다운로드 실패)"
    },
    
    # ==================== 自定义论文数量 ====================
    "paper_count_label": {
        "zh-CN": "论文数量",
        "zh-TW": "論文數量",
        "ja": "論文数",
        "ko": "논문 수"
    },
    "paper_count_custom": {
        "zh-CN": "自定义",
        "zh-TW": "自定義",
        "ja": "カスタム",
        "ko": "사용자 지정"
    },
    "paper_count_input": {
        "zh-CN": "输入数量 (1-50)",
        "zh-TW": "輸入數量 (1-50)",
        "ja": "数量を入力 (1-50)",
        "ko": "수량 입력 (1-50)"
    },
    
    # ==================== 收藏夹功能 ====================
    "favorites": {
        "zh-CN": "⭐ 收藏夹",
        "zh-TW": "⭐ 收藏夾",
        "ja": "⭐ お気に入り",
        "ko": "⭐ 즐겨찾기"
    },
    "favorites_count": {
        "zh-CN": "共 {count} 篇收藏",
        "zh-TW": "共 {count} 篇收藏",
        "ja": "全 {count} 件のお気に入り",
        "ko": "총 {count}개 즐겨찾기"
    },
    "favorites_empty": {
        "zh-CN": "收藏夹为空，点击论文旁的 ⭐ 添加收藏",
        "zh-TW": "收藏夾為空，點擊論文旁的 ⭐ 添加收藏",
        "ja": "お気に入りは空です。論文の横にある ⭐ をクリックして追加",
        "ko": "즐겨찾기가 비어 있습니다. 논문 옆의 ⭐를 클릭하여 추가"
    },
    "add_to_favorites": {
        "zh-CN": "⭐ 收藏",
        "zh-TW": "⭐ 收藏",
        "ja": "⭐ お気に入り追加",
        "ko": "⭐ 즐겨찾기 추가"
    },
    "remove_from_favorites": {
        "zh-CN": "💛 已收藏",
        "zh-TW": "💛 已收藏",
        "ja": "💛 お気に入り済み",
        "ko": "💛 즐겨찾기됨"
    },
    "favorite_success": {
        "zh-CN": "已添加到收藏夹",
        "zh-TW": "已添加到收藏夾",
        "ja": "お気に入りに追加しました",
        "ko": "즐겨찾기에 추가되었습니다"
    },
    "unfavorite_success": {
        "zh-CN": "已从收藏夹移除",
        "zh-TW": "已從收藏夾移除",
        "ja": "お気に入りから削除しました",
        "ko": "즐겨찾기에서 제거되었습니다"
    },
    "favorite_category": {
        "zh-CN": "收藏到分类",
        "zh-TW": "收藏到分類",
        "ja": "カテゴリに追加",
        "ko": "카테고리에 추가"
    },
    "new_category": {
        "zh-CN": "新建分类...",
        "zh-TW": "新建分類...",
        "ja": "新しいカテゴリ...",
        "ko": "새 카테고리..."
    },
    "category_name": {
        "zh-CN": "分类名称",
        "zh-TW": "分類名稱",
        "ja": "カテゴリ名",
        "ko": "카테고리 이름"
    },
    "all_favorites": {
        "zh-CN": "全部收藏",
        "zh-TW": "全部收藏",
        "ja": "すべてのお気に入り",
        "ko": "모든 즐겨찾기"
    },
    "favorited_at": {
        "zh-CN": "收藏于 {time}",
        "zh-TW": "收藏於 {time}",
        "ja": "{time} にお気に入りに追加",
        "ko": "{time}에 즐겨찾기에 추가됨"
    },
    "delete_category": {
        "zh-CN": "删除分类",
        "zh-TW": "刪除分類",
        "ja": "カテゴリを削除",
        "ko": "카테고리 삭제"
    },
    "view_mode": {
        "zh-CN": "查看模式",
        "zh-TW": "查看模式",
        "ja": "表示モード",
        "ko": "보기 모드"
    },
    "browse_papers": {
        "zh-CN": "📚 浏览论文",
        "zh-TW": "📚 瀏覽論文",
        "ja": "📚 論文を閲覧",
        "ko": "📚 논문 탐색"
    },
    "my_favorites": {
        "zh-CN": "⭐ 我的收藏",
        "zh-TW": "⭐ 我的收藏",
        "ja": "⭐ マイお気に入り",
        "ko": "⭐ 내 즐겨찾기"
    },
    
    # ==================== 错误消息 ====================
    "error_no_api_key": {
        "en": "⚠️ Please configure API Key in the sidebar first",
        "zh-CN": "⚠️ 请先在左侧配置 API Key",
        "zh-TW": "⚠️ 請先在左側配置 API Key",
        "ja": "⚠️ まず左側でAPI Keyを設定してください",
        "ko": "⚠️ 먼저 왼쪽에서 API Key를 설정해주세요"
    },
    
    # ==================== Conference Tracker (顶会日历) ====================
    "conference_tracker": {
        "en": "📅 Conference Calendar",
        "zh-CN": "📅 会议日历",
        "zh-TW": "📅 會議日曆",
        "ja": "📅 学会カレンダー",
        "ko": "📅 학회 일정"
    },
    "ccf_a": {
        "en": "CCF-A",
        "zh-CN": "CCF-A",
        "zh-TW": "CCF-A",
        "ja": "CCF-A",
        "ko": "CCF-A"
    },
    "ccf_b": {
        "en": "CCF-B",
        "zh-CN": "CCF-B",
        "zh-TW": "CCF-B",
        "ja": "CCF-B",
        "ko": "CCF-B"
    },
    "ccf_c": {
        "en": "CCF-C",
        "zh-CN": "CCF-C",
        "zh-TW": "CCF-C",
        "ja": "CCF-C",
        "ko": "CCF-C"
    },
    "all_ranks": {
        "en": "All",
        "zh-CN": "全部",
        "zh-TW": "全部",
        "ja": "すべて",
        "ko": "전체"
    },
    "upcoming_deadlines": {
        "en": "Upcoming Deadlines",
        "zh-CN": "即将截止",
        "zh-TW": "即將截止",
        "ja": "締切間近",
        "ko": "마감 임박"
    },
    "days_left": {
        "en": "{days} days left",
        "zh-CN": "还剩 {days} 天",
        "zh-TW": "還剩 {days} 天",
        "ja": "残り {days} 日",
        "ko": "{days}일 남음"
    },
    "today": {
        "en": "Today!",
        "zh-CN": "今天！",
        "zh-TW": "今天！",
        "ja": "今日！",
        "ko": "오늘!"
    },
    "days_ago": {
        "en": "{days} days ago",
        "zh-CN": "已过 {days} 天",
        "zh-TW": "已過 {days} 天",
        "ja": "{days} 日前",
        "ko": "{days}일 전"
    },
    "coming_to_conference": {
        "en": "🎯 {conference}",
        "zh-CN": "🎯 可能投稿 {conference}",
        "zh-TW": "🎯 可能投稿 {conference}",
        "ja": "🎯 {conference} に投稿予定？",
        "ko": "🎯 {conference} 투고 예정?"
    },
    
    # ==================== Hyperparam Spy (参数显微镜) ====================
    "hyperparam_spy": {
        "en": "🔬 Extract Hyperparams",
        "zh-CN": "🔬 提取超参数",
        "zh-TW": "🔬 提取超參數",
        "ja": "🔬 ハイパラ抽出",
        "ko": "🔬 하이퍼파람 추출"
    },
    "extracting_hyperparams": {
        "en": "Extracting hyperparameters from PDF...",
        "zh-CN": "正在从 PDF 提取超参数...",
        "zh-TW": "正在從 PDF 提取超參數...",
        "ja": "PDFからハイパーパラメータを抽出中...",
        "ko": "PDF에서 하이퍼파라미터 추출 중..."
    },
    "hyperparam_title": {
        "en": "🔧 **Experiment Configuration**",
        "zh-CN": "🔧 **实验配置**",
        "zh-TW": "🔧 **實驗配置**",
        "ja": "🔧 **実験構成**",
        "ko": "🔧 **실험 구성**"
    },
    "hyperparam_failed": {
        "en": "Failed to extract hyperparameters",
        "zh-CN": "提取超参数失败",
        "zh-TW": "提取超參數失敗",
        "ja": "ハイパーパラメータの抽出に失敗",
        "ko": "하이퍼파라미터 추출 실패"
    },
    
    # ==================== Trend Radar (热词云) ====================
    "trend_radar": {
        "en": "☁️ Trend Radar",
        "zh-CN": "☁️ 热词云",
        "zh-TW": "☁️ 熱詞雲",
        "ja": "☁️ トレンドレーダー",
        "ko": "☁️ 트렌드 레이더"
    },
    "trend_radar_desc": {
        "en": "Word cloud showing trending topics in current papers",
        "zh-CN": "展示当前论文中的热门话题",
        "zh-TW": "展示當前論文中的熱門話題",
        "ja": "現在の論文のトレンドトピック",
        "ko": "현재 논문의 트렌드 토픽"
    },
    "generating_wordcloud": {
        "en": "Generating word cloud...",
        "zh-CN": "正在生成词云...",
        "zh-TW": "正在生成詞雲...",
        "ja": "ワードクラウドを生成中...",
        "ko": "워드클라우드 생성 중..."
    },
    "wordcloud_not_available": {
        "en": "Please install wordcloud: pip install wordcloud",
        "zh-CN": "请安装 wordcloud: pip install wordcloud",
        "zh-TW": "請安裝 wordcloud: pip install wordcloud",
        "ja": "wordcloud をインストールしてください: pip install wordcloud",
        "ko": "wordcloud 설치 필요: pip install wordcloud"
    },
    "top_keywords": {
        "en": "🔥 Top Keywords",
        "zh-CN": "🔥 热门关键词",
        "zh-TW": "🔥 熱門關鍵字",
        "ja": "🔥 人気キーワード",
        "ko": "🔥 인기 키워드"
    },
    
    # ==================== 底部信息 ====================
    "made_with_love": {
        "en": "Made with ❤️ by Jay Yu",
        "zh-CN": "Made with ❤️ by Jay Yu",
        "zh-TW": "Made with ❤️ by Jay Yu",
        "ja": "Made with ❤️ by Jay Yu",
        "ko": "Made with ❤️ by Jay Yu"
    }
}

# ==================== 为所有翻译添加英文版本 ====================
# 自动为缺少英文的翻译项添加英文
ENGLISH_TRANSLATIONS = {
    "app_title": "🍳 ArXiv Daily Chef",
    "app_subtitle": "Your personal paper chef, curating the latest research daily",
    "api_settings": "⚙️ API Settings",
    "base_url": "Base URL",
    "base_url_help": "OpenAI compatible API address (DeepSeek, Moonshot, etc.)",
    "api_key": "API Key",
    "api_key_help": "Your API key",
    "model": "Model",
    "model_help": "Model name (gpt-4, deepseek-chat, etc.)",
    "language_settings": "🌐 Language",
    "subscribe_topics": "📚 Subscribed Topics",
    "add_topic_placeholder": "e.g. Point Cloud",
    "subscribed_count": "{count} topics subscribed",
    "no_topics_hint": "👆 Add topics you're interested in",
    "topic_exists": "Topic '{topic}' already exists",
    "topic_added": "Successfully added: {topic}",
    "topic_empty": "Topic name cannot be empty",
    "welcome_hint": "👈 Add and select a topic from the sidebar to explore papers!",
    "quick_start": "🚀 Quick Start",
    "quick_start_content": """**Steps:**
1. Configure **API** in the sidebar (supports OpenAI, DeepSeek, Moonshot, etc.)
2. Enter topic keywords and click ➕ to add
3. Click topic tags to fetch latest papers
4. Click "Generate Summary" for AI insights

**Recommended Keywords:**
- `Point Cloud` - Point cloud processing
- `3D Gaussian Splatting` - 3D Gaussian splatting
- `LLM Agents` - Large language model agents
- `Neural Radiance Fields` - Neural radiance fields""",
    "topic_label": "📖 Topic: {topic}",
    "refresh_papers": "🔄 Refresh Papers",
    "paper_count": "Paper count",
    "fetching_papers": "Fetching {topic} papers from ArXiv...",
    "no_papers_found": "No papers found for \"{topic}\"",
    "papers_found": "✅ Found {count} latest papers",
    "authors_et_al": "et al. ({count} authors)",
    "view_abstract": "📄 View Abstract (English)",
    "code_available": "🟢 CODE AVAILABLE",
    "ai_summary_title": "**🤖 AI Summary:**",
    "generate_summary": "✨ Generate AI Summary",
    "generating_summary": "AI is analyzing the paper...",
    "generate_all_summaries": "🚀 Generate All Summaries",
    "processing_paper": "Processing: {title}...",
    "all_summaries_done": "✅ All summaries generated!",
    "summary_failed": "❌ Generation failed: {error}",
    "load_teaser": "🖼️ Load Paper Figure",
    "loading_teaser": "Downloading PDF and extracting figure...",
    "teaser_title": "📸 Paper Figure (Teaser/Architecture)",
    "teaser_not_found": "Could not extract figure (PDF may not contain images)",
    "paper_count_label": "Paper count",
    "paper_count_custom": "Custom",
    "paper_count_input": "Enter count (1-50)",
    "favorites": "⭐ Favorites",
    "favorites_count": "{count} papers saved",
    "favorites_empty": "Favorites empty. Click ⭐ next to papers to add",
    "add_to_favorites": "⭐ Favorite",
    "remove_from_favorites": "💛 Favorited",
    "favorite_success": "Added to favorites",
    "unfavorite_success": "Removed from favorites",
    "favorite_category": "Save to category",
    "new_category": "New category...",
    "category_name": "Category name",
    "all_favorites": "All Favorites",
    "favorited_at": "Saved on {time}",
    "delete_category": "Delete category",
    "view_mode": "View Mode",
    "browse_papers": "📚 Browse Papers",
    "my_favorites": "⭐ My Favorites",
}

# 自动添加英文翻译
for key, en_text in ENGLISH_TRANSLATIONS.items():
    if key in TRANSLATIONS and "en" not in TRANSLATIONS[key]:
        TRANSLATIONS[key]["en"] = en_text


def get_text(key: str, lang: str = "zh-CN", **kwargs) -> str:
    """
    获取指定语言的翻译文本
    
    Args:
        key: 翻译键名
        lang: 语言代码 (en, zh-CN, zh-TW, ja, ko)
        **kwargs: 用于格式化字符串的参数
    
    Returns:
        str: 翻译后的文本，如果找不到则返回键名
    """
    if key not in TRANSLATIONS:
        return key
    
    translations = TRANSLATIONS[key]
    # 优先返回请求的语言，其次英文，最后中文
    text = translations.get(lang, translations.get("en", translations.get("zh-CN", key)))
    
    # 支持字符串格式化
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    
    return text


def get_llm_system_prompt(lang: str = "zh-CN") -> str:
    """
    根据语言返回对应的 LLM 系统提示词
    
    Args:
        lang: 语言代码
    
    Returns:
        str: 系统提示词
    """
    prompts = {
        "en": """You are a professional research paper analysis assistant. Please analyze the following English paper abstract.

**Requirements:**
1. First, summarize the core content and research objectives in 2-3 sentences
2. Then list **3 key innovations**, each described in one sentence

**Output format:**
📝 **Paper Summary**
[Your summary]

💡 **Key Innovations**
1. [Innovation 1]
2. [Innovation 2]
3. [Innovation 3]

Be concise and professional for quick understanding.""",
        
        "zh-CN": """你是一位专业的科研论文解读助手。请根据用户提供的英文论文摘要，用简体中文进行解读。

**输出要求：**
1. 先用 2-3 句话概括论文的核心内容和研究目标
2. 然后列出 **3 个核心创新点**，每个创新点用一句话描述

**输出格式：**
📝 **论文概述**
[你的概述内容]

💡 **核心创新点**
1. [创新点1]
2. [创新点2]
3. [创新点3]

请确保语言简洁专业，便于快速理解。""",
        
        "zh-TW": """你是一位專業的科研論文解讀助手。請根據用戶提供的英文論文摘要，用繁體中文進行解讀。

**輸出要求：**
1. 先用 2-3 句話概括論文的核心內容和研究目標
2. 然後列出 **3 個核心創新點**，每個創新點用一句話描述

**輸出格式：**
📝 **論文概述**
[你的概述內容]

💡 **核心創新點**
1. [創新點1]
2. [創新點2]
3. [創新點3]

請確保語言簡潔專業，便於快速理解。""",
        
        "ja": """あなたはプロフェッショナルな科学論文解説アシスタントです。ユーザーが提供する英語の論文アブストラクトを日本語で解説してください。

**出力要件：**
1. まず2-3文で論文の核心的な内容と研究目標を要約
2. 次に**3つの核心的イノベーションポイント**を列挙し、各ポイントを1文で説明

**出力フォーマット：**
📝 **論文概要**
[概要内容]

💡 **核心的イノベーションポイント**
1. [ポイント1]
2. [ポイント2]
3. [ポイント3]

簡潔かつ専門的な表現で、素早く理解できるようにしてください。""",
        
        "ko": """당신은 전문적인 과학 논문 해설 어시스턴트입니다. 사용자가 제공하는 영어 논문 초록을 한국어로 해설해주세요.

**출력 요구사항:**
1. 먼저 2-3문장으로 논문의 핵심 내용과 연구 목표를 요약
2. 그 다음 **3가지 핵심 혁신점**을 나열하고, 각 혁신점을 한 문장으로 설명

**출력 형식:**
📝 **논문 개요**
[개요 내용]

💡 **핵심 혁신점**
1. [혁신점1]
2. [혁신점2]
3. [혁신점3]

간결하고 전문적인 표현으로 빠르게 이해할 수 있도록 해주세요."""
    }
    
    return prompts.get(lang, prompts["en"])
