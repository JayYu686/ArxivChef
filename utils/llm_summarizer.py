"""
LLM 摘要生成模块
调用 OpenAI 兼容的 API 对论文摘要进行多语言总结
"""

from openai import OpenAI
from typing import Optional
from utils.i18n import get_llm_system_prompt


class LLMSummarizeError(Exception):
    """LLM 调用异常"""
    pass


def summarize_abstract(
    abstract: str,
    api_key: str,
    base_url: str = "https://api.openai.com/v1",
    model: str = "gpt-3.5-turbo",
    lang: str = "zh-CN"
) -> str:
    """
    使用 LLM 对论文摘要进行总结
    
    Args:
        abstract: 论文的英文摘要
        api_key: OpenAI 兼容 API 的密钥
        base_url: API 基础 URL（支持 DeepSeek、Moonshot 等兼容接口）
        model: 使用的模型名称
        lang: 输出语言 (zh-CN, zh-TW, ja, ko)
    
    Returns:
        str: LLM 生成的摘要
    
    Raises:
        LLMSummarizeError: 当 API 调用失败时抛出
    """
    # 参数验证
    if not api_key or not api_key.strip():
        raise LLMSummarizeError("请先配置 API Key")
    
    if not abstract or not abstract.strip():
        raise LLMSummarizeError("论文摘要为空")
    
    try:
        # 创建 OpenAI 客户端（兼容其他 API）
        client = OpenAI(
            api_key=api_key.strip(),
            base_url=base_url.strip() if base_url else "https://api.openai.com/v1",
            timeout=60.0  # 设置超时时间
        )
        
        # 根据语言获取对应的系统提示词
        system_prompt = get_llm_system_prompt(lang)
        
        # 调用 Chat Completion API
        response = client.chat.completions.create(
            model=model.strip() if model else "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请分析以下论文摘要：\n\n{abstract}"}
            ],
            temperature=0.7,  # 适中的创造性
            max_tokens=800    # 限制输出长度
        )
        
        # 提取生成的内容
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            raise LLMSummarizeError("LLM 返回结果为空")
    
    except LLMSummarizeError:
        # 重新抛出已知异常
        raise
    
    except Exception as e:
        # 处理 API 调用中的各种错误
        error_msg = str(e)
        
        if "401" in error_msg or "Unauthorized" in error_msg:
            raise LLMSummarizeError("API Key 无效，请检查配置")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            raise LLMSummarizeError("API 调用频率过高，请稍后重试")
        elif "timeout" in error_msg.lower():
            raise LLMSummarizeError("API 请求超时，请检查网络连接")
        elif "connection" in error_msg.lower():
            raise LLMSummarizeError("无法连接到 API 服务器，请检查 Base URL 配置")
        else:
            raise LLMSummarizeError(f"LLM 调用失败: {error_msg}")
