"""
modern_library.py
圖書管理系統 v2.0 (Refactored)

重構重點：
- 改用 JSON 格式儲存（books.json）
- 加入完整例外處理
- 使用 with 語法處理檔案操作
- 消除全域變數，改用參數傳遞
- 遵循單一職責原則，拆分函式
- 加入型別提示，提升可讀性
- 支援 return（還書）功能
"""

import os
import json
from typing import TypedDict

# ── 常數 ────────────────────────────────────────────────
F_NAME = "books.json"

# ── 型別定義 ─────────────────────────────────────────────
class Book(TypedDict):
    title:  str
    isbn:   str
    status: str

# ── 檔案 I/O ─────────────────────────────────────────────
def load_records(filepath: str = F_NAME) -> list[Book]:
    """從 JSON 檔案讀取書籍清單。"""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[錯誤] 無法讀取檔案：{e}")
        return []


def save_records(records: list[Book], filepath: str = F_NAME) -> bool:
    """將書籍清單寫回 JSON 檔案。"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        return True
    except OSError as e:
        print(f"[錯誤] 無法儲存檔案：{e}")
        return False

# ── 商業邏輯 ─────────────────────────────────────────────
def is_isbn_exists(records: list[Book], isbn: str) -> bool:
    return any(book["isbn"] == isbn for book in records)


def add_book(records: list[Book], title: str, isbn: str, status: str) -> bool:
    if is_isbn_exists(records, isbn):
        return False
    records.append({"title": title, "isbn": isbn, "status": status})
    return True


def borrow_book(records: list[Book], isbn: str) -> bool:
    for book in records:
        if book["isbn"] == isbn:
            if book["status"] == "borrowed":
                print("此書已被借出")
                return False
            book["status"] = "borrowed"
            return True
    return False


def return_book(records: list[Book], isbn: str) -> bool:
    for book in records:
        if book["isbn"] == isbn:
            if book["status"] == "available":
                print("此書尚未被借出")
                return False
            book["status"] = "available"
            return True
    return False


def show_books(records: list[Book]) -> None:
    if not records:
        print("目前沒有任何書籍。")
        return
    print(f"\n{'書名':<20} {'ISBN':<20} {'狀態'}")
    print("-" * 55)
    for book in records:
        print(f"{book['title']:<20} {book['isbn']:<20} {book['status']}")
    print()

# ── 指令解析 ─────────────────────────────────────────────
def handle_add(records: list[Book], raw: str) -> None:
    parts = raw.split("/")
    if len(parts) != 3:
        print("Format Error（正確格式：add 書名/ISBN/狀態）")
        return
    title, isbn, status = (p.strip() for p in parts)
    if not all([title, isbn, status]):
        print("Format Error（欄位不得為空）")
        return
    print("Success" if add_book(records, title, isbn, status) else "ISBN Exist")


def handle_borrow(records: list[Book], isbn: str) -> None:
    if not isbn:
        print("Format Error（請提供 ISBN）")
        return
    print("Updated" if borrow_book(records, isbn) else "ISBN Not Found")


def handle_return(records: list[Book], isbn: str) -> None:
    if not isbn:
        print("Format Error（請提供 ISBN）")
        return
    print("Returned" if return_book(records, isbn) else "ISBN Not Found")


def print_help() -> None:
    print("""
可用指令：
  add 書名/ISBN/狀態  新增書籍
  show                顯示所有書籍
  borrow <ISBN>       借出書籍
  return <ISBN>       歸還書籍
  help                顯示此說明
  exit                儲存並離開
""")

# ── 主程式 ───────────────────────────────────────────────
def main() -> None:
    records = load_records()
    print("=== 圖書管理系統 v2.0 (Refactored) ===")
    print("輸入 help 查看可用指令")

    while True:
        try:
            op = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n偵測到中斷，正在儲存資料...")
            save_records(records)
            break

        if not op:
            continue

        if op == "exit":
            print("資料已儲存，系統關閉。" if save_records(records) else "儲存失敗，請確認檔案權限。")
            break
        elif op == "show":
            show_books(records)
        elif op == "help":
            print_help()
        elif op.startswith("add "):
            handle_add(records, op[4:].strip())
        elif op.startswith("borrow "):
            handle_borrow(records, op[7:].strip())
        elif op.startswith("return "):
            handle_return(records, op[7:].strip())
        else:
            print(f"Unknown Command：'{op}'（輸入 help 查看可用指令）")


if __name__ == "__main__":
    main()