# core/io_utils.py
import json
from pathlib import Path
from datetime import datetime

def write_output_files(out_dir: Path, raw_text: str, normalized_text: str,
                       model: str = "phi3", engine: str = "docTR"):
    """
    Ghi các file đầu ra:
      - raw_ocr.txt
      - normalized.txt
      - meta.json
    Trả về tuple (raw_path, norm_path, meta_path)
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_path = out_dir / "raw_ocr.txt"
    norm_path = out_dir / "normalized.txt"
    meta_path = out_dir / "meta.json"

    # Ghi text
    raw_path.write_text(raw_text, encoding="utf-8")
    norm_path.write_text(normalized_text, encoding="utf-8")

    # Ghi metadata
    meta = {
        "timestamp": datetime.now().isoformat(),
        "engine": engine,
        "model": model,
        "files": {
            "raw_ocr": str(raw_path),
            "normalized": str(norm_path)
        },
        "lengths": {
            "raw": len(raw_text),
            "normalized": len(normalized_text)
        }
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    return raw_path, norm_path, meta_path
