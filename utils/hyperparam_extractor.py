"""
Hyperparam Spy - 参数显微镜模块
从论文 PDF 中提取实验配置和超参数信息
"""

import fitz  # PyMuPDF
import os
import re
from typing import Optional, Dict, List
from utils.pdf_image_extractor import download_pdf, get_pdf_url_from_arxiv


# 用于 LLM 提取超参数的系统提示词（多语言）
HYPERPARAM_PROMPTS = {
    "zh-CN": """你是一个专业的论文参数提取助手。请仔细阅读以下论文片段（来自实验和实现细节章节），提取所有实验配置和超参数信息。

**请提取以下信息（如果存在）：**
- Batch Size（批次大小）
- Learning Rate（学习率）及其调度策略
- Optimizer（优化器）类型
- GPU/硬件配置
- Training Epochs/Iterations（训练轮数）
- 模型架构细节
- 数据集信息
- 其他重要超参数

**输出格式：**
🔧 **实验配置**

| 参数 | 值 |
|------|-----|
| Batch Size | [值] |
| Learning Rate | [值] |
| Optimizer | [值] |
| GPU | [值] |
| Epochs | [值] |
| ... | ... |

如果某些参数未在文中提及，请标注"未提及"。如果文本中没有任何实验细节，请回复"未找到实验配置信息"。""",

    "zh-TW": """你是一個專業的論文參數提取助手。請仔細閱讀以下論文片段（來自實驗和實現細節章節），提取所有實驗配置和超參數信息。

**請提取以下信息（如果存在）：**
- Batch Size（批次大小）
- Learning Rate（學習率）及其調度策略
- Optimizer（優化器）類型
- GPU/硬件配置
- Training Epochs/Iterations（訓練輪數）
- 模型架構細節
- 數據集信息
- 其他重要超參數

**輸出格式：**
🔧 **實驗配置**

| 參數 | 值 |
|------|-----|
| Batch Size | [值] |
| Learning Rate | [值] |
| Optimizer | [值] |
| GPU | [值] |
| Epochs | [值] |
| ... | ... |

如果某些參數未在文中提及，請標注"未提及"。""",

    "en": """You are a professional paper parameter extraction assistant. Please carefully read the following paper excerpts (from the experiments and implementation details sections) and extract all experimental configurations and hyperparameters.

**Please extract the following (if present):**
- Batch Size
- Learning Rate and scheduling strategy
- Optimizer type
- GPU/Hardware configuration
- Training Epochs/Iterations
- Model architecture details
- Dataset information
- Other important hyperparameters

**Output format:**
🔧 **Experiment Configuration**

| Parameter | Value |
|-----------|-------|
| Batch Size | [value] |
| Learning Rate | [value] |
| Optimizer | [value] |
| GPU | [value] |
| Epochs | [value] |
| ... | ... |

If some parameters are not mentioned, mark as "Not mentioned". If no experimental details found, reply "No experimental configuration found".""",

    "ja": """あなたは論文パラメータ抽出の専門アシスタントです。以下の論文テキスト（実験と実装詳細セクションから）を注意深く読み、すべての実験構成とハイパーパラメータを抽出してください。

**以下の情報を抽出してください（存在する場合）:**
- Batch Size（バッチサイズ）
- Learning Rate（学習率）とスケジューリング戦略
- Optimizer（オプティマイザ）タイプ
- GPU/ハードウェア構成
- Training Epochs/Iterations（訓練エポック数）
- モデルアーキテクチャの詳細
- データセット情報
- その他の重要なハイパーパラメータ

**出力フォーマット:**
🔧 **実験構成**

| パラメータ | 値 |
|-----------|-----|
| Batch Size | [値] |
| Learning Rate | [値] |
| Optimizer | [値] |
| GPU | [値] |
| Epochs | [値] |
| ... | ... |

文中に記載がない場合は「記載なし」と記入してください。""",

    "ko": """당신은 논문 파라미터 추출 전문 어시스턴트입니다. 다음 논문 텍스트(실험 및 구현 세부 사항 섹션)를 주의 깊게 읽고 모든 실험 구성과 하이퍼파라미터를 추출해주세요.

**다음 정보를 추출하세요 (존재하는 경우):**
- Batch Size (배치 크기)
- Learning Rate (학습률) 및 스케줄링 전략
- Optimizer (옵티마이저) 유형
- GPU/하드웨어 구성
- Training Epochs/Iterations (훈련 에폭 수)
- 모델 아키텍처 세부 사항
- 데이터셋 정보
- 기타 중요한 하이퍼파라미터

**출력 형식:**
🔧 **실험 구성**

| 파라미터 | 값 |
|----------|-----|
| Batch Size | [값] |
| Learning Rate | [값] |
| Optimizer | [값] |
| GPU | [값] |
| Epochs | [값] |
| ... | ... |

문서에 언급되지 않은 경우 "언급 없음"으로 표시하세요."""
}


def extract_pdf_text(pdf_path: str, max_pages: int = 15) -> str:
    """
    从 PDF 中提取文本内容
    
    Args:
        pdf_path: PDF 文件路径
        max_pages: 最多提取的页数
    
    Returns:
        str: 提取的文本内容
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num in range(min(max_pages, len(doc))):
            page = doc[page_num]
            text_parts.append(page.get_text())
        
        doc.close()
        return "\n".join(text_parts)
    except Exception as e:
        print(f"提取 PDF 文本失败: {e}")
        return ""


def extract_experiment_sections(full_text: str) -> str:
    """
    从论文全文中提取实验相关章节
    
    Args:
        full_text: PDF 全文
    
    Returns:
        str: 实验相关文本（最多 8000 字符）
    """
    # 关键词模式，用于定位实验章节
    section_patterns = [
        r'(?i)(experiment|实验)',
        r'(?i)(implementation|实现)',
        r'(?i)(training|训练)',
        r'(?i)(setup|设置)',
        r'(?i)(hyperparameter|超参数)',
        r'(?i)(configuration|配置)',
        r'(?i)(baseline|基准)',
        r'(?i)(ablation|消融)',
    ]
    
    lines = full_text.split('\n')
    relevant_lines = []
    in_relevant_section = False
    section_line_count = 0
    
    for i, line in enumerate(lines):
        # 检查是否是章节标题
        is_section_header = any(re.search(pattern, line) for pattern in section_patterns)
        
        if is_section_header:
            in_relevant_section = True
            section_line_count = 0
        
        if in_relevant_section:
            relevant_lines.append(line)
            section_line_count += 1
            
            # 每个相关章节最多保留 100 行
            if section_line_count > 100:
                in_relevant_section = False
    
    result = "\n".join(relevant_lines)
    
    # 如果找到的内容太少，返回论文中间部分（通常包含实验）
    if len(result) < 1000:
        mid_start = len(full_text) // 3
        mid_end = 2 * len(full_text) // 3
        result = full_text[mid_start:mid_end]
    
    # 限制长度
    return result[:8000]


def get_hyperparam_prompt(lang: str = "zh-CN") -> str:
    """获取指定语言的超参数提取提示词"""
    return HYPERPARAM_PROMPTS.get(lang, HYPERPARAM_PROMPTS["en"])


def extract_hyperparams_from_pdf(
    arxiv_url: str,
    arxiv_id: str,
    api_key: str,
    base_url: str,
    model: str,
    lang: str = "zh-CN"
) -> Optional[str]:
    """
    从论文 PDF 中提取超参数信息
    
    Args:
        arxiv_url: ArXiv 论文 URL
        arxiv_id: ArXiv ID
        api_key: LLM API Key
        base_url: LLM API Base URL
        model: 模型名称
        lang: 语言代码
    
    Returns:
        Optional[str]: LLM 生成的超参数卡片，失败返回 None
    """
    from openai import OpenAI
    
    # 下载 PDF
    pdf_url = get_pdf_url_from_arxiv(arxiv_url)
    pdf_path = download_pdf(pdf_url, arxiv_id)
    
    if not pdf_path:
        return None
    
    # 提取文本
    full_text = extract_pdf_text(pdf_path)
    if not full_text:
        return None
    
    # 提取实验章节
    experiment_text = extract_experiment_sections(full_text)
    
    try:
        # 调用 LLM 提取超参数
        client = OpenAI(
            api_key=api_key.strip(),
            base_url=base_url.strip() if base_url else "https://api.openai.com/v1",
            timeout=90.0
        )
        
        system_prompt = get_hyperparam_prompt(lang)
        
        response = client.chat.completions.create(
            model=model.strip() if model else "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请从以下论文文本中提取实验配置：\n\n{experiment_text}"}
            ],
            temperature=0.3,  # 低创造性，追求准确
            max_tokens=1000
        )
        
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        return None
    
    except Exception as e:
        print(f"提取超参数失败: {e}")
        return None
