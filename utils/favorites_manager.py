"""
收藏夹管理模块
支持按领域分类收藏论文，JSON 持久化存储
"""

import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


# 收藏数据文件路径
FAVORITES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "favorites.json")


@dataclass
class FavoritePaper:
    """收藏的论文数据结构"""
    arxiv_id: str           # ArXiv ID
    title: str              # 论文标题
    authors: List[str]      # 作者列表
    abstract: str           # 摘要
    url: str                # ArXiv 链接
    published: str          # 发布日期
    category: str           # 收藏分类（领域）
    favorited_at: str       # 收藏时间
    code_urls: List[str]    # 代码链接（如有）
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "FavoritePaper":
        return cls(**data)


def load_favorites() -> Dict[str, List[dict]]:
    """
    从 favorites.json 加载收藏列表
    返回格式：{分类名: [论文列表]}
    """
    try:
        if os.path.exists(FAVORITES_FILE):
            with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        return {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"加载收藏列表失败: {e}")
        return {}


def save_favorites(favorites: Dict[str, List[dict]]) -> bool:
    """
    保存收藏列表到 favorites.json
    """
    try:
        with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
            json.dump(favorites, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"保存收藏列表失败: {e}")
        return False


def get_categories() -> List[str]:
    """
    获取所有收藏分类（领域）
    """
    favorites = load_favorites()
    return list(favorites.keys())


def add_favorite(
    arxiv_id: str,
    title: str,
    authors: List[str],
    abstract: str,
    url: str,
    published: str,
    category: str,
    code_urls: List[str] = None
) -> tuple[bool, str]:
    """
    添加论文到收藏夹
    
    Args:
        arxiv_id: ArXiv ID
        title: 论文标题
        authors: 作者列表
        abstract: 摘要
        url: ArXiv 链接
        published: 发布日期
        category: 收藏分类
        code_urls: 代码链接列表
    
    Returns:
        tuple: (是否成功, 提示消息)
    """
    favorites = load_favorites()
    
    # 检查是否已收藏
    if category in favorites:
        for paper in favorites[category]:
            if paper.get("arxiv_id") == arxiv_id:
                return False, "该论文已在收藏夹中"
    
    # 创建收藏记录
    paper = FavoritePaper(
        arxiv_id=arxiv_id,
        title=title,
        authors=authors,
        abstract=abstract,
        url=url,
        published=published,
        category=category,
        favorited_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        code_urls=code_urls or []
    )
    
    # 添加到分类
    if category not in favorites:
        favorites[category] = []
    favorites[category].append(paper.to_dict())
    
    if save_favorites(favorites):
        return True, "收藏成功"
    return False, "保存失败"


def remove_favorite(arxiv_id: str, category: str) -> tuple[bool, str]:
    """
    从收藏夹移除论文
    """
    favorites = load_favorites()
    
    if category not in favorites:
        return False, "分类不存在"
    
    # 查找并删除
    for i, paper in enumerate(favorites[category]):
        if paper.get("arxiv_id") == arxiv_id:
            favorites[category].pop(i)
            # 如果分类空了，删除分类
            if not favorites[category]:
                del favorites[category]
            if save_favorites(favorites):
                return True, "已取消收藏"
            return False, "保存失败"
    
    return False, "论文不在收藏夹中"


def is_favorited(arxiv_id: str) -> tuple[bool, Optional[str]]:
    """
    检查论文是否已收藏
    
    Returns:
        tuple: (是否已收藏, 所在分类)
    """
    favorites = load_favorites()
    
    for category, papers in favorites.items():
        for paper in papers:
            if paper.get("arxiv_id") == arxiv_id:
                return True, category
    
    return False, None


def get_favorites_by_category(category: str) -> List[dict]:
    """
    获取指定分类的所有收藏
    """
    favorites = load_favorites()
    return favorites.get(category, [])


def get_all_favorites() -> List[dict]:
    """
    获取所有收藏（扁平化）
    """
    favorites = load_favorites()
    all_papers = []
    for papers in favorites.values():
        all_papers.extend(papers)
    return all_papers


def get_favorites_count() -> int:
    """
    获取收藏总数
    """
    return len(get_all_favorites())


def delete_category(category: str) -> tuple[bool, str]:
    """
    删除整个收藏分类
    """
    favorites = load_favorites()
    
    if category not in favorites:
        return False, "分类不存在"
    
    del favorites[category]
    
    if save_favorites(favorites):
        return True, f"已删除分类: {category}"
    return False, "保存失败"
