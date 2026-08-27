# Organize Downloads

Script Python tự động sắp xếp thư mục Downloads theo loại file (ảnh, video, tài liệu, file nén, code, ...).

## Cách dùng

```bash
# Xem thử (dry-run, không thay đổi gì)
python organize_downloads.py

# Chạy thật, di chuyển file
python organize_downloads.py --run

# Sắp xếp thư mục khác thay vì Downloads mặc định
python organize_downloads.py --path "D:\SomeFolder" --run
```

## Chạy tự động hàng tuần (Windows)

Dùng `run_organize.bat` kết hợp Task Scheduler để tự động chạy mỗi tuần. Chi tiết xem trong code.

## Lưu ý

Mỗi lần chạy `--run` sẽ sinh ra file log (`organize_log_*.txt`) ghi lại đã di chuyển file nào — file này không nên đưa lên GitHub vì chứa tên file cá nhân (đã thêm vào `.gitignore`).
