# OCR_LLM4TTG_WindowTool

---

## 1. System Architecture

```text
OCR-LLM-Windows/
├── README.md                         # Hướng dẫn cài đặt & chạy trên Windows
├── requirements.txt                  # python-doctr, torch(cpu), pillow, opencv-python, requests, pypdfium2
├── .env.example                      # OLLAMA_HOST=http://localhost:11434 ; MODEL=phi3
│
├── app_gui/
│   └── main.py                       # Giao diện Tkinter: chọn file, chạy OCR → LLM → xem kết quả
│
├── core/
│   ├── pipeline.py                   # Xử lý chính: load file → OCR (docTR) → cleanup → LLM (Ollama)
│   ├── doctr_ocr.py                  # OCR dùng docTR (ưu tiên tiếng Việt, hỗ trợ tiếng Anh)
│   ├── cleanup.py                    # Sửa 0↔o, 1↔l, dấu tiếng Việt, chuẩn hoá Unicode
│   ├── llm_ollama.py                 # Gọi Ollama local để chuẩn hoá ngữ nghĩa & chính tả
│   └── io_utils.py                   # Đọc/ghi file, tạo out/, meta.json
│
├── prompts/
│   └── normalize_vi.txt              # Prompt: “sửa chính tả, giữ nguyên nghĩa”
│
├── data/
│   ├── in/                           # Tài liệu đầu vào (PDF, ảnh, hoá đơn)
│   ├── out/                          # raw_ocr.txt, normalized.txt, meta.json
│   └── temp/                         # Ảnh tạm khi PDF → ảnh
│
├── config/
│   ├── config.yaml                   # engine=doctr, model=phi3, timeout, language=vi
│   └── dictionaries/
│       ├── legal_terms.txt           # Từ khoá pháp lý
│       └── finance_terms.txt         # Từ khoá tài chính / vay vốn
│
└── scripts/
    ├── install_ollama.ps1            # Cài Ollama & pull model phi3
    ├── install_deps.ps1              # Cài Python libs & docTR
    └── run_app.bat                   # Khởi động app GUI
```