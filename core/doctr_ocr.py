# core/doctr_ocr.py
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from pathlib import Path
import os

# Tải model docTR sẵn khi module được import
# Dùng mô hình lightweight để chạy tốt trên CPU (không cần GPU)
print("[docTR] Đang khởi tạo model OCR (db_resnet50 + crnn_vgg16_bn)...")
model = ocr_predictor(pretrained=True, assume_straight_pages=True)

def extract_text_doctr(input_path: str) -> str:
    """
    OCR văn bản từ PDF hoặc ảnh bằng docTR.
    Tự động nhận dạng ngôn ngữ (ưu tiên tiếng Việt).
    """
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {input_path}")

    # Đọc file vào docTR
    if path.suffix.lower() == ".pdf":
        doc = DocumentFile.from_pdf(input_path)
    else:
        doc = DocumentFile.from_images(input_path)

    # Thực thi OCR
    result = model(doc)
    text = result.render()
    print(f"[docTR] Đã OCR xong: {len(text)} ký tự")
    return text
