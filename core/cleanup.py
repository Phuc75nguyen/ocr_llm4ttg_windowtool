# core/cleanup.py
import regex as re
import unicodedata as ud

def clean_text(text: str) -> str:
    """Làm sạch text OCR: chuẩn hoá Unicode, sửa lỗi ký tự phổ biến, dọn khoảng trắng"""
    if not text:
        return ""

    # --- Chuẩn hoá Unicode (NFC) ---
    text = ud.normalize("NFC", text)

    # --- Dọn khoảng trắng ---
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    # --- Sửa lỗi ký tự dễ nhầm ---
    text = fix_common_confusions(text)

    # --- Sửa dấu tiếng Việt bị tách (ô, ơ, ư, ă, â) ---
    text = fix_vietnamese_diacritics(text)

    return text


def fix_common_confusions(text: str) -> str:
    """Sửa lỗi phổ biến: 0↔o, 1↔l↔I theo ngữ cảnh"""
    # 0 trong chữ → o
    text = re.sub(r"(?<=[A-Za-zÀ-ỹ])0(?=[A-Za-zÀ-ỹ])", "o", text)
    # o trong số → 0
    text = re.sub(r"(?<=[0-9])o(?=[0-9])", "0", text)
    # l/I trong số → 1
    text = re.sub(r"(?<=[0-9])[lI](?=[0-9])", "1", text)
    # 1 trong chữ → l
    text = re.sub(r"(?<=[A-Za-zÀ-ỹ])1(?=[A-Za-zÀ-ỹ])", "l", text)
    return text


def fix_vietnamese_diacritics(text: str) -> str:
    """Ghép lại các ký tự dấu tiếng Việt bị tách rời"""
    s = ud.normalize("NFD", text)
    s = s.replace("o\u0302", "ô").replace("O\u0302", "Ô")
    s = s.replace("a\u0306", "ă").replace("A\u0306", "Ă")
    s = s.replace("a\u0302", "â").replace("A\u0302", "Â")
    s = s.replace("u\u031B", "ư").replace("U\u031B", "Ư")
    s = s.replace("o\u031B", "ơ").replace("O\u031B", "Ơ")
    s = ud.normalize("NFC", s)
    return s
