"""
Conference Calendar - 会议日历模块
跟踪 AI/CV/NLP/ML 会议的关键时间节点，按 CCF 分类
"""

from datetime import datetime, date
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class ConferenceDeadline:
    """会议截止日期数据结构"""
    conference: str          # 会议名称 (如 "CVPR 2026")
    event: str               # 事件类型 (如 "Paper Deadline")
    deadline: date           # 截止日期
    url: str                 # 会议官网
    ccf_rank: str            # CCF 等级: "A", "B", "C", "None"
    
    @property
    def days_left(self) -> int:
        """计算距离截止日期的天数"""
        delta = self.deadline - date.today()
        return delta.days
    
    @property
    def is_past(self) -> bool:
        """是否已过期"""
        return self.days_left < 0
    
    @property
    def is_urgent(self) -> bool:
        """是否紧急（7天内）"""
        return 0 <= self.days_left <= 7
    
    @property
    def is_soon(self) -> bool:
        """是否临近（30天内）"""
        return 0 <= self.days_left <= 30
    
    @property
    def rank_badge(self) -> str:
        """获取等级徽章"""
        badges = {
            "A": "🅰️",
            "B": "🅱️", 
            "C": "©️",
            "None": "📎"
        }
        return badges.get(self.ccf_rank, "📎")


# ==================== CCF 会议分类及日历 ====================
# 数据来源: https://www.ccf.org.cn/ + https://aideadlin.es
# 日期建议定期更新

CONFERENCE_DEADLINES: List[ConferenceDeadline] = [
    # ==================== CCF-A 类 ====================
    # 计算机视觉
    ConferenceDeadline("CVPR 2026", "Paper Deadline", date(2025, 11, 14), "https://cvpr.thecvf.com/", "A"),
    ConferenceDeadline("CVPR 2026", "Conference", date(2026, 6, 17), "https://cvpr.thecvf.com/", "A"),
    ConferenceDeadline("ICCV 2025", "Paper Deadline", date(2025, 3, 8), "https://iccv.thecvf.com/", "A"),
    ConferenceDeadline("ICCV 2025", "Conference", date(2025, 10, 19), "https://iccv.thecvf.com/", "A"),
    
    # 机器学习
    ConferenceDeadline("NeurIPS 2025", "Paper Deadline", date(2025, 5, 22), "https://neurips.cc/", "A"),
    ConferenceDeadline("NeurIPS 2025", "Conference", date(2025, 12, 9), "https://neurips.cc/", "A"),
    ConferenceDeadline("ICML 2025", "Paper Deadline", date(2025, 1, 31), "https://icml.cc/", "A"),
    ConferenceDeadline("ICML 2025", "Conference", date(2025, 7, 13), "https://icml.cc/", "A"),
    
    # 人工智能
    ConferenceDeadline("AAAI 2026", "Paper Deadline", date(2025, 8, 15), "https://aaai.org/", "A"),
    ConferenceDeadline("AAAI 2026", "Conference", date(2026, 2, 20), "https://aaai.org/", "A"),
    ConferenceDeadline("IJCAI 2025", "Paper Deadline", date(2025, 1, 16), "https://ijcai.org/", "A"),
    ConferenceDeadline("IJCAI 2025", "Conference", date(2025, 8, 16), "https://ijcai.org/", "A"),
    
    # 自然语言处理
    ConferenceDeadline("ACL 2025", "Paper Deadline", date(2025, 2, 15), "https://www.aclweb.org/", "A"),
    ConferenceDeadline("ACL 2025", "Conference", date(2025, 7, 27), "https://www.aclweb.org/", "A"),
    
    # 多媒体
    ConferenceDeadline("ACM MM 2025", "Paper Deadline", date(2025, 4, 11), "https://www.acmmm.org/", "A"),
    ConferenceDeadline("ACM MM 2025", "Conference", date(2025, 10, 27), "https://www.acmmm.org/", "A"),
    
    # ==================== CCF-B 类 ====================
    # 计算机视觉
    ConferenceDeadline("ECCV 2026", "Paper Deadline", date(2026, 3, 6), "https://eccv.ecva.net/", "B"),
    
    # 机器学习
    ConferenceDeadline("ICLR 2026", "Paper Deadline", date(2025, 10, 1), "https://iclr.cc/", "B"),
    ConferenceDeadline("ICLR 2026", "Conference", date(2026, 4, 24), "https://iclr.cc/", "B"),
    ConferenceDeadline("AISTATS 2025", "Paper Deadline", date(2024, 10, 10), "https://aistats.org/", "B"),
    ConferenceDeadline("AISTATS 2025", "Conference", date(2025, 5, 3), "https://aistats.org/", "B"),
    
    # 自然语言处理
    ConferenceDeadline("EMNLP 2025", "Paper Deadline", date(2025, 5, 15), "https://2025.emnlp.org/", "B"),
    ConferenceDeadline("EMNLP 2025", "Conference", date(2025, 11, 12), "https://2025.emnlp.org/", "B"),
    ConferenceDeadline("NAACL 2025", "Paper Deadline", date(2024, 10, 15), "https://naacl.org/", "B"),
    ConferenceDeadline("NAACL 2025", "Conference", date(2025, 4, 29), "https://naacl.org/", "B"),
    ConferenceDeadline("COLING 2025", "Paper Deadline", date(2024, 9, 16), "https://coling2025.org/", "B"),
    ConferenceDeadline("COLING 2025", "Conference", date(2025, 1, 19), "https://coling2025.org/", "B"),
    
    # 机器人
    ConferenceDeadline("ICRA 2025", "Paper Deadline", date(2024, 9, 15), "https://ieee-icra.org/", "B"),
    ConferenceDeadline("ICRA 2025", "Conference", date(2025, 5, 19), "https://ieee-icra.org/", "B"),
    ConferenceDeadline("IROS 2025", "Paper Deadline", date(2025, 3, 1), "https://ieee-iros.org/", "B"),
    ConferenceDeadline("IROS 2025", "Conference", date(2025, 10, 19), "https://ieee-iros.org/", "B"),
    
    # 图形学
    ConferenceDeadline("SIGGRAPH 2025", "Paper Deadline", date(2025, 1, 23), "https://s2025.siggraph.org/", "B"),
    ConferenceDeadline("SIGGRAPH 2025", "Conference", date(2025, 8, 10), "https://s2025.siggraph.org/", "B"),
    ConferenceDeadline("SIGGRAPH Asia 2025", "Paper Deadline", date(2025, 5, 22), "https://asia.siggraph.org/", "B"),
    
    # ==================== CCF-C 类 ====================
    ConferenceDeadline("WACV 2026", "Paper Deadline", date(2025, 7, 10), "https://wacv2026.thecvf.com/", "C"),
    ConferenceDeadline("WACV 2026", "Conference", date(2026, 2, 28), "https://wacv2026.thecvf.com/", "C"),
    ConferenceDeadline("BMVC 2025", "Paper Deadline", date(2025, 5, 2), "https://bmvc2025.org/", "C"),
    ConferenceDeadline("BMVC 2025", "Conference", date(2025, 11, 24), "https://bmvc2025.org/", "C"),
    ConferenceDeadline("ACCV 2024", "Paper Deadline", date(2024, 7, 2), "https://accv2024.org/", "C"),
    ConferenceDeadline("3DV 2025", "Paper Deadline", date(2024, 8, 12), "https://3dvconf.github.io/", "C"),
    
    # ==================== 非 CCF 但重要 ====================
    ConferenceDeadline("CVPR Workshop", "Paper Deadline", date(2026, 3, 14), "https://cvpr.thecvf.com/", "None"),
]


def get_upcoming_deadlines(limit: int = 5, include_past: bool = False, ccf_filter: str = None) -> List[ConferenceDeadline]:
    """
    获取即将到来的会议截止日期
    
    Args:
        limit: 返回数量限制
        include_past: 是否包含已过期的截止日期
        ccf_filter: CCF 等级过滤 ("A", "B", "C", None 表示全部)
    
    Returns:
        List[ConferenceDeadline]: 按日期排序的截止日期列表
    """
    deadlines = CONFERENCE_DEADLINES.copy()
    
    # CCF 等级过滤
    if ccf_filter:
        deadlines = [d for d in deadlines if d.ccf_rank == ccf_filter]
    
    # 过滤已过期的
    if not include_past:
        deadlines = [d for d in deadlines if not d.is_past]
    
    # 按日期排序
    deadlines.sort(key=lambda x: x.deadline)
    
    return deadlines[:limit]


def get_deadlines_by_ccf_rank(rank: str) -> List[ConferenceDeadline]:
    """
    按 CCF 等级获取会议
    """
    deadlines = [d for d in CONFERENCE_DEADLINES if d.ccf_rank == rank and not d.is_past]
    deadlines.sort(key=lambda x: x.deadline)
    return deadlines


def get_deadlines_by_conference(conference_name: str) -> List[ConferenceDeadline]:
    """
    获取指定会议的所有截止日期
    """
    return [d for d in CONFERENCE_DEADLINES if conference_name.upper() in d.conference.upper()]


def check_paper_conference_match(paper_published_date: str) -> Optional[str]:
    """
    检查论文发布时间是否与某个会议投稿时间吻合
    """
    try:
        pub_date = datetime.strptime(paper_published_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    
    for deadline in CONFERENCE_DEADLINES:
        if deadline.event == "Paper Deadline":
            days_diff = (pub_date - deadline.deadline).days
            if -30 <= days_diff <= 60:
                return f"Coming to {deadline.conference}?"
    
    return None


def format_countdown(days: int, lang: str = "zh-CN") -> str:
    """格式化倒计时文本"""
    if lang == "en":
        if days < 0:
            return f"{abs(days)}d ago"
        elif days == 0:
            return "Today!"
        else:
            return f"{days}d left"
    elif lang == "ja":
        if days < 0:
            return f"{abs(days)}日前"
        elif days == 0:
            return "今日！"
        else:
            return f"残り{days}日"
    elif lang == "ko":
        if days < 0:
            return f"{abs(days)}일 전"
        elif days == 0:
            return "오늘!"
        else:
            return f"{days}일 남음"
    else:  # zh-CN, zh-TW
        if days < 0:
            return f"已过{abs(days)}天"
        elif days == 0:
            return "今天！"
        else:
            return f"剩{days}天"
