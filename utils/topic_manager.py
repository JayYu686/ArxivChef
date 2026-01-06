"""
领域订阅管理模块
负责用户订阅列表的增删查改以及 JSON 文件持久化
"""

import json
import os
from typing import List

# 订阅数据文件路径（与 app.py 同级目录）
TOPICS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "topics.json")


def load_topics() -> List[str]:
    """
    从 topics.json 加载用户订阅的领域列表
    如果文件不存在或格式错误，返回空列表
    """
    try:
        if os.path.exists(TOPICS_FILE):
            with open(TOPICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 确保返回的是列表类型
                if isinstance(data, list):
                    return data
        return []
    except (json.JSONDecodeError, IOError) as e:
        # 文件损坏或读取失败时返回空列表
        print(f"加载订阅列表失败: {e}")
        return []


def save_topics(topics: List[str]) -> bool:
    """
    将订阅列表保存到 topics.json 文件
    
    Args:
        topics: 订阅的领域列表
    
    Returns:
        bool: 保存成功返回 True，失败返回 False
    """
    try:
        with open(TOPICS_FILE, "w", encoding="utf-8") as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
        return True
    except IOError as e:
        print(f"保存订阅列表失败: {e}")
        return False


def add_topic(topic: str) -> tuple[bool, str]:
    """
    添加新的订阅领域
    
    Args:
        topic: 要添加的领域关键词
    
    Returns:
        tuple: (是否成功, 提示消息)
    """
    # 去除首尾空格
    topic = topic.strip()
    
    if not topic:
        return False, "领域名称不能为空"
    
    topics = load_topics()
    
    # 检查是否已存在（不区分大小写）
    if any(t.lower() == topic.lower() for t in topics):
        return False, f"领域 '{topic}' 已存在"
    
    topics.append(topic)
    
    if save_topics(topics):
        return True, f"成功添加领域: {topic}"
    else:
        return False, "保存失败，请重试"


def delete_topic(topic: str) -> tuple[bool, str]:
    """
    删除指定的订阅领域
    
    Args:
        topic: 要删除的领域关键词
    
    Returns:
        tuple: (是否成功, 提示消息)
    """
    topics = load_topics()
    
    if topic not in topics:
        return False, f"领域 '{topic}' 不存在"
    
    topics.remove(topic)
    
    if save_topics(topics):
        return True, f"成功删除领域: {topic}"
    else:
        return False, "保存失败，请重试"
