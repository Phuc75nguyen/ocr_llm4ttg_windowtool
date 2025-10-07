# core/pipeline.py
import os
from pathlib import Path
from datetime import datetime
from core.doctr_ocr import extract_text_doctr
from core.cleanup import clean_text
from core.llm_ollama import normalize_text_llm
from core.io_utils import write_output_files

def process_file(input_path: str, out_dir: Path) -> tuple[str, str]:
    """Xử lý 1 file PDF/Ảnh → OCR → cleanup → LLM normalize"""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    basename = Path(input_path).stem
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    work_dir = out_dir / f"{basename}_{run_id}"
    work_dir.mkdir(parents=True, exist_ok=True)

    # --- Step 1. OCR bằng docTR ---
    print("[1/4] Đang OCR với docTR...")
    raw_text = extract_text_doctr(input_path)

    # --- Step 2. Cleanup text ---
    print("[2/4] Đang làm sạch text...")
    cleaned = clean_text(raw_text)

    # --- Step 3. Gọi Ollama (nếu có) ---
    print("[3/4] Gọi LLM (Ollama)...")
    normalized = normalize_text_llm(cleaned)

    # --- Step 4. Ghi kết quả ra file ---
    print("[4/4] Ghi file kết quả...")
    raw_path, norm_path, meta_path = write_output_files(
        work_dir, raw_text, normalized, model="phi3", engine="docTR"
    )

    print("Hoàn tất.")
    return str(raw_path), str(norm_path)
