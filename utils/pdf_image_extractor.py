"""
PDF 图片提取模块
使用 PyMuPDF (fitz) 从论文 PDF 中提取 Teaser Image 或架构图
"""

import fitz  # PyMuPDF
import io
import os
import requests
import tempfile
from typing import Optional, Tuple
from PIL import Image
import base64


# 缓存目录
CACHE_DIR = os.path.join(tempfile.gettempdir(), "arxiv_daily_chef_cache")


def ensure_cache_dir():
    """确保缓存目录存在"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def get_pdf_url_from_arxiv(arxiv_url: str) -> str:
    """
    从 ArXiv 论文页面 URL 获取 PDF 下载链接
    
    Args:
        arxiv_url: ArXiv 论文页面 URL (如 https://arxiv.org/abs/2401.xxxxx)
    
    Returns:
        str: PDF 下载 URL
    """
    # 将 abs URL 转换为 pdf URL
    if "/abs/" in arxiv_url:
        return arxiv_url.replace("/abs/", "/pdf/") + ".pdf"
    elif "arxiv.org" in arxiv_url:
        # 从 entry_id 提取 arxiv_id
        arxiv_id = arxiv_url.split("/")[-1]
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return arxiv_url


def download_pdf(pdf_url: str, arxiv_id: str) -> Optional[str]:
    """
    下载 PDF 文件到缓存目录
    
    Args:
        pdf_url: PDF 下载 URL
        arxiv_id: ArXiv ID，用于缓存文件名
    
    Returns:
        Optional[str]: 下载的 PDF 文件路径，失败返回 None
    """
    ensure_cache_dir()
    
    # 生成缓存文件名
    safe_id = arxiv_id.replace("/", "_").replace(":", "_")
    cache_path = os.path.join(CACHE_DIR, f"{safe_id}.pdf")
    
    # 如果已缓存，直接返回
    if os.path.exists(cache_path):
        return cache_path
    
    try:
        # 下载 PDF
        response = requests.get(pdf_url, timeout=30, stream=True)
        response.raise_for_status()
        
        # 保存到缓存
        with open(cache_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return cache_path
    
    except Exception as e:
        print(f"下载 PDF 失败: {e}")
        return None


def extract_first_image(pdf_path: str, min_width: int = 200, min_height: int = 200) -> Optional[bytes]:
    """
    从 PDF 中提取第一张有意义的图片（通常是 Teaser 或架构图）
    
    Args:
        pdf_path: PDF 文件路径
        min_width: 最小宽度，过滤掉小图标
        min_height: 最小高度，过滤掉小图标
    
    Returns:
        Optional[bytes]: 图片的二进制数据 (PNG 格式)，失败返回 None
    """
    try:
        doc = fitz.open(pdf_path)
        
        # 只扫描前 3 页（Teaser 通常在第一页）
        max_pages = min(3, len(doc))
        
        for page_num in range(max_pages):
            page = doc[page_num]
            
            # 获取页面中的所有图片
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]
                
                try:
                    # 提取图片
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # 检查图片尺寸
                    img = Image.open(io.BytesIO(image_bytes))
                    width, height = img.size
                    
                    # 过滤掉太小的图片（如 logo、图标）
                    if width >= min_width and height >= min_height:
                        # 转换为 PNG 格式
                        output = io.BytesIO()
                        
                        # 如果是 RGBA，转为 RGB
                        if img.mode == "RGBA":
                            img = img.convert("RGB")
                        
                        img.save(output, format="PNG")
                        doc.close()
                        return output.getvalue()
                
                except Exception as e:
                    # 某些图片可能无法提取，跳过
                    continue
        
        doc.close()
        return None
    
    except Exception as e:
        print(f"提取图片失败: {e}")
        return None


def get_teaser_image(arxiv_url: str, arxiv_id: str) -> Optional[bytes]:
    """
    获取论文的 Teaser 图片
    
    Args:
        arxiv_url: ArXiv 论文 URL
        arxiv_id: ArXiv ID
    
    Returns:
        Optional[bytes]: 图片二进制数据 (PNG)，失败返回 None
    """
    # 获取 PDF URL
    pdf_url = get_pdf_url_from_arxiv(arxiv_url)
    
    # 下载 PDF
    pdf_path = download_pdf(pdf_url, arxiv_id)
    if not pdf_path:
        return None
    
    # 提取图片
    return extract_first_image(pdf_path)


def image_to_base64(image_bytes: bytes) -> str:
    """
    将图片二进制数据转换为 base64 字符串，用于在 HTML 中显示
    
    Args:
        image_bytes: 图片二进制数据
    
    Returns:
        str: base64 编码的 data URL
    """
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{base64_str}"
