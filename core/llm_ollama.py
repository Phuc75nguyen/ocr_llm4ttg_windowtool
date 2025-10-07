# core/llm_ollama.py
import os
import requests

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL", "phi3")

def normalize_text_llm(text: str) -> str:
    """
    Gửi text qua Ollama local để chuẩn hoá chính tả và ngữ cảnh tiếng Việt.
    Nếu Ollama không chạy, trả lại text gốc.
    """
    if not text.strip():
        return text

    prompt = f"""
Bạn là trình CHUẨN HOÁ văn bản tiếng Việt chạy offline.
Yêu cầu:
- Giữ nguyên NGHĨA gốc của văn bản.
- Sửa lỗi OCR: 0↔o, 1↔l, thiếu dấu, sai chính tả, ngắt câu.
- Không bịa nội dung mới, không tóm tắt.
- Không đổi số liệu, ngày tháng, mã số.
Trả lại đúng văn bản đã được sửa, không thêm lời giải thích.

Văn bản:
\"\"\"\n{text}\n\"\"\""""

    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=90
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip() or text
    except Exception as e:
        print(f"[WARN] Ollama không phản hồi ({e}), dùng text gốc.")
        return text
