"""
Trend Radar - 热词云模块
从论文摘要中提取高频词并生成词云图
"""

import re
from collections import Counter
from typing import List, Optional
from io import BytesIO

try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False

# ==================== 学术论文停用词表 ====================
# 包括英文常用词 + 学术论文常见废话词
STOPWORDS = {
    # 英文常用词
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'it', 'its', 'this', 'that', 'these', 'those', 'i', 'we', 'you',
    'he', 'she', 'they', 'them', 'their', 'our', 'your', 'my', 'his', 'her',
    'which', 'who', 'whom', 'what', 'where', 'when', 'why', 'how', 'all',
    'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
    'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
    's', 't', 'just', 'don', 'now', 'also', 'into', 'over', 'after', 'before',
    'between', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
    'about', 'above', 'below', 'up', 'down', 'out', 'off', 'through', 'during',
    'while', 'if', 'because', 'until', 'although', 'though', 'whether', 'however',
    
    # 学术论文常见废话词
    'proposed', 'propose', 'proposes', 'method', 'methods', 'approach', 'approaches',
    'paper', 'papers', 'work', 'works', 'study', 'studies', 'research', 'novel',
    'new', 'based', 'using', 'use', 'used', 'show', 'shows', 'shown', 'achieve',
    'achieves', 'achieved', 'result', 'results', 'experimental', 'experiments',
    'demonstrate', 'demonstrates', 'demonstrated', 'present', 'presents', 'presented',
    'introduce', 'introduces', 'introduced', 'existing', 'previous', 'state',
    'art', 'sota', 'performance', 'perform', 'performs', 'performed', 'improve',
    'improves', 'improved', 'improvement', 'improvements', 'effective', 'effectively',
    'efficient', 'efficiently', 'significant', 'significantly', 'compared', 'comparison',
    'et', 'al', 'etc', 'eg', 'ie', 'vs', 'via', 'thus', 'hence', 'therefore',
    'moreover', 'furthermore', 'additionally', 'finally', 'first', 'second', 'third',
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'several', 'many', 'various', 'different', 'similar', 'well', 'better', 'best',
    'high', 'higher', 'highest', 'low', 'lower', 'lowest', 'large', 'larger', 'largest',
    'small', 'smaller', 'smallest', 'good', 'bad', 'able', 'particular', 'particularly',
    'given', 'without', 'within', 'across', 'among', 'along', 'around', 'since', 'even',
    'still', 'yet', 'already', 'often', 'usually', 'always', 'never', 'sometimes',
    'together', 'possible', 'especially', 'recently', 'commonly', 'widely', 'easily',
    'directly', 'simply', 'mainly', 'primarily', 'example', 'examples', 'case', 'cases',
    'way', 'ways', 'order', 'general', 'specific', 'specifically', 'following', 'follows',
    'key', 'important', 'main', 'major', 'further', 'due', 'according', 'respectively',
    'corresponding', 'overall', 'total', 'average', 'standard', 'common', 'typical',
    'known', 'called', 'considered', 'applied', 'obtained', 'required', 'needed',
    'make', 'makes', 'made', 'take', 'takes', 'took', 'taken', 'get', 'gets', 'got',
    'set', 'sets', 'put', 'give', 'gives', 'gave', 'find', 'finds', 'found', 'see',
    'problem', 'problems', 'solution', 'solutions', 'task', 'tasks', 'challenge',
    'challenges', 'issue', 'issues', 'limitation', 'limitations', 'advantage', 'advantages',
    'feature', 'features', 'property', 'properties', 'framework', 'frameworks', 'system',
    'systems', 'component', 'components', 'module', 'modules', 'layer', 'layers',
    'input', 'inputs', 'output', 'outputs', 'process', 'processes', 'step', 'steps',
    'stage', 'stages', 'level', 'levels', 'type', 'types', 'form', 'forms', 'part',
    'parts', 'number', 'numbers', 'amount', 'amounts', 'size', 'sizes', 'time', 'times',
    'point', 'points', 'value', 'values', 'function', 'functions', 'parameter', 'parameters',
}


def extract_keywords(texts: List[str], min_word_length: int = 3, max_words: int = 100) -> dict:
    """
    从文本列表中提取关键词及其频率
    
    Args:
        texts: 文本列表（通常是论文摘要）
        min_word_length: 最小词长度
        max_words: 返回的最大词数
    
    Returns:
        dict: 词频字典 {word: count}
    """
    # 合并所有文本
    combined_text = " ".join(texts).lower()
    
    # 提取单词（只保留字母和连字符）
    words = re.findall(r'\b[a-zA-Z][a-zA-Z-]*[a-zA-Z]\b|\b[a-zA-Z]{2,}\b', combined_text)
    
    # 过滤：去除停用词和短词
    filtered_words = [
        word for word in words
        if word not in STOPWORDS
        and len(word) >= min_word_length
        and not word.isdigit()
    ]
    
    # 统计词频
    word_counts = Counter(filtered_words)
    
    # 返回最常见的词
    return dict(word_counts.most_common(max_words))


def generate_wordcloud(
    word_frequencies: dict,
    width: int = 800,
    height: int = 400,
    background_color: str = 'white',
    colormap: str = 'viridis',
    max_words: int = 80
) -> Optional[bytes]:
    """
    从词频字典生成词云图像
    
    Args:
        word_frequencies: 词频字典
        width: 图像宽度
        height: 图像高度
        background_color: 背景颜色
        colormap: 颜色方案 (viridis, plasma, inferno, magma, cividis, cool, hot, spring, summer, autumn, winter, rainbow)
        max_words: 最大显示词数
    
    Returns:
        bytes: PNG 图像数据，失败返回 None
    """
    if not WORDCLOUD_AVAILABLE:
        print("wordcloud 库未安装，请运行: pip install wordcloud")
        return None
    
    if not word_frequencies:
        return None
    
    try:
        # 创建词云
        wc = WordCloud(
            width=width,
            height=height,
            background_color=background_color,
            colormap=colormap,
            max_words=max_words,
            prefer_horizontal=0.7,
            min_font_size=10,
            max_font_size=120,
            relative_scaling=0.5,
            random_state=42  # 保持一致性
        )
        
        # 生成词云
        wc.generate_from_frequencies(word_frequencies)
        
        # 保存为 PNG 字节流
        buffer = BytesIO()
        wc.to_image().save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer.getvalue()
    
    except Exception as e:
        print(f"生成词云失败: {e}")
        return None


def generate_trend_radar(abstracts: List[str], colormap: str = 'viridis') -> Optional[bytes]:
    """
    从论文摘要列表生成趋势词云
    
    Args:
        abstracts: 论文摘要列表
        colormap: 颜色方案
    
    Returns:
        bytes: PNG 图像数据
    """
    if not abstracts:
        return None
    
    # 提取关键词
    keywords = extract_keywords(abstracts)
    
    if not keywords:
        return None
    
    # 生成词云
    return generate_wordcloud(keywords, colormap=colormap)


def get_top_keywords(abstracts: List[str], top_n: int = 10) -> List[tuple]:
    """
    获取排名前 N 的关键词
    
    Args:
        abstracts: 论文摘要列表
        top_n: 返回数量
    
    Returns:
        List[tuple]: [(word, count), ...]
    """
    keywords = extract_keywords(abstracts)
    return list(keywords.items())[:top_n]
