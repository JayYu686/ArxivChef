"""
ArXiv 论文拉取模块
使用 arxiv 库搜索并获取指定领域的最新论文
"""

import arxiv
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


# 用于检测代码仓库和项目页面链接的正则表达式
# 匹配 github.com, gitlab.com, bitbucket.org 以及常见项目页面 URL
CODE_URL_PATTERNS = [
    # GitHub 链接 (包含 github.com 或 github.io)
    r'https?://(?:www\.)?github\.com/[\w\-\.]+/[\w\-\.]+(?:/[\w\-\./]*)?',
    r'https?://[\w\-]+\.github\.io(?:/[\w\-\./]*)?',
    # GitLab 链接
    r'https?://(?:www\.)?gitlab\.com/[\w\-\.]+/[\w\-\.]+(?:/[\w\-\./]*)?',
    # 项目页面（常见模式）
    r'https?://[\w\-]+\.(?:github\.io|gitlab\.io|pages\.dev)(?:/[\w\-\./]*)?',
    # 带有 project, code, demo 关键词的链接
    r'https?://[^\s\)\]]+(?:project[_\-]?page|code|demo|homepage)[^\s\)\]]*',
]


def extract_code_urls(text: str) -> List[str]:
    """
    从文本中提取代码仓库和项目页面链接
    
    Args:
        text: 要扫描的文本（通常是论文摘要）
    
    Returns:
        List[str]: 找到的 URL 列表（去重）
    """
    found_urls = set()
    
    for pattern in CODE_URL_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_urls.update(matches)
    
    # 清理 URL（移除尾部标点符号）
    cleaned_urls = []
    for url in found_urls:
        # 移除末尾可能误匹配的标点
        url = url.rstrip('.,;:!?)]>')
        if url:
            cleaned_urls.append(url)
    
    return list(cleaned_urls)


@dataclass
class Paper:
    """论文数据结构"""
    title: str                          # 论文标题
    authors: List[str]                  # 作者列表
    abstract: str                       # 摘要
    url: str                            # ArXiv 链接
    published: str                      # 发布日期
    arxiv_id: str                       # ArXiv ID
    code_urls: List[str] = field(default_factory=list)  # 代码/项目页面链接
    
    @property
    def has_code(self) -> bool:
        """判断论文是否有可用代码"""
        return len(self.code_urls) > 0


class ArxivFetchError(Exception):
    """ArXiv 拉取异常"""
    pass


def fetch_papers(query: str, max_results: int = 5) -> List[Paper]:
    """
    根据关键词从 ArXiv 搜索最新论文
    
    Args:
        query: 搜索关键词（如 "Point Cloud", "LLM Agents"）
        max_results: 返回的最大论文数量，默认为 5
    
    Returns:
        List[Paper]: 论文列表
    
    Raises:
        ArxivFetchError: 当网络连接失败或超时时抛出
    """
    import time
    
    try:
        # 创建 ArXiv 客户端，设置更长的延迟和更多重试
        client = arxiv.Client(
            page_size=max_results,
            delay_seconds=3.0,  # 请求间隔增加到 3 秒
            num_retries=5       # 重试次数增加到 5 次
        )
        
        # 构建搜索查询
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        
        # 执行搜索并解析结果
        for result in client.results(search):
            # 处理摘要文本
            abstract_text = result.summary.replace("\n", " ")
            
            # 从摘要中提取代码/项目链接
            code_urls = extract_code_urls(abstract_text)
            
            paper = Paper(
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=abstract_text,
                url=result.entry_id,
                published=result.published.strftime("%Y-%m-%d"),
                arxiv_id=result.get_short_id(),
                code_urls=code_urls
            )
            papers.append(paper)
        
        return papers
    
    except arxiv.UnexpectedEmptyPageError as e:
        raise ArxivFetchError(f"未找到与 '{query}' 相关的论文")
    
    except arxiv.HTTPError as e:
        error_str = str(e)
        if "429" in error_str:
            raise ArxivFetchError(
                "⏳ ArXiv 请求频率限制 (429)，请等待 30 秒后重试。\n"
                "ArXiv API 限制每 IP 每 3 秒最多 1 次请求。"
            )
        raise ArxivFetchError(f"ArXiv 服务请求失败: {error_str}")
    
    except Exception as e:
        raise ArxivFetchError(f"获取论文失败，请检查网络连接: {str(e)}")
