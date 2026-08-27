#!/usr/bin/env python3
"""
organize_downloads.py
Tự động sắp xếp thư mục Downloads theo loại file (ảnh, video, doc, nén, code, ...)

Cách dùng:
    python organize_downloads.py                # dry-run, chỉ in ra sẽ làm gì
    python organize_downloads.py --run           # thực sự di chuyển file
    python organize_downloads.py --path /duong/dan/khac --run
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime

# Map đuôi file -> tên thư mục đích
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".heic"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv"],
    "Music": [".mp3", ".wav", ".flac", ".aac", ".m4a"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".pptx", ".csv", ".odt"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".deb", ".apk"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".ipynb", ".java", ".cpp", ".c", ".sh"],
}

def get_category(suffix: str) -> str:
    suffix = suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"

def unique_destination(dest_dir: Path, filename: str) -> Path:
    """Nếu trùng tên file, tự thêm số đằng sau để không ghi đè."""
    dest = dest_dir / filename
    if not dest.exists():
        return dest
    stem, suffix = Path(filename).stem, Path(filename).suffix
    counter = 1
    while dest.exists():
        dest = dest_dir / f"{stem} ({counter}){suffix}"
        counter += 1
    return dest

def organize(folder: Path, dry_run: bool = True):
    if not folder.exists():
        print(f"❌ Không tìm thấy thư mục: {folder}")
        return

    log_lines = []
    moved_count = 0

    for item in folder.iterdir():
        if item.is_dir():
            continue  # bỏ qua thư mục con, kể cả thư mục do script này tạo ra trước đó

        category = get_category(item.suffix)
        dest_dir = folder / category
        dest_path = unique_destination(dest_dir, item.name)

        log_lines.append(f"{item.name}  ->  {category}/{dest_path.name}")

        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_path))
            moved_count += 1

    if not log_lines:
        print("✅ Thư mục đã gọn rồi, không có gì để sắp xếp.")
        return

    print(f"\n{'[DRY-RUN] Sẽ di chuyển' if dry_run else '✅ Đã di chuyển'} {len(log_lines)} file:\n")
    for line in log_lines:
        print("  " + line)

    if dry_run:
        print("\n👉 Không có gì bị thay đổi. Chạy lại với --run để thực sự di chuyển file.")
    else:
        # Ghi log ra file để lỡ cần tra lại đã move file nào đi đâu
        log_path = folder / f"organize_log_{datetime.now():%Y%m%d_%H%M%S}.txt"
        log_path.write_text("\n".join(log_lines), encoding="utf-8")
        print(f"\n📝 Đã lưu log tại: {log_path}")

def main():
    parser = argparse.ArgumentParser(description="Tự động sắp xếp thư mục Downloads theo loại file")
    parser.add_argument("--path", type=str, default=str(Path.home() / "Downloads"),
                         help="Đường dẫn thư mục cần sắp xếp (mặc định: ~/Downloads)")
    parser.add_argument("--run", action="store_true",
                         help="Thực sự di chuyển file. Không có cờ này = chỉ dry-run")
    args = parser.parse_args()

    organize(Path(args.path), dry_run=not args.run)

if __name__ == "__main__":
    main()
