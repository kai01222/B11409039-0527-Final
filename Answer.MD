# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409039  
**系級：** 資管系大一  
**姓名：** 李元凱  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) |l1 是存放檔案每一行內容的暫存清單 |lines()|
| Q2 d2 (in main) |d2 是儲存所有書籍資料的全域清單| book_list()|
| Q3 c_res (in check) |這個函式用來檢查某個 ISBN 是否已存在於 d2 清單中，避免重複新增書籍。 | is_isbn_exists(isbn)|

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 缺乏例外處理，當檔案 `lib_data.txt` 不存在或格式錯誤時，程式會直接崩潰。
- **Q2：** 使用全域變數 `d2`，當程式規模擴大時，容易導致資料競態問題或意外覆蓋。
- **Q3：** 檔案操作未使用 `with` 語法，當程式中途發生錯誤時，可能導致檔案未正確關閉。
- **Q4：** 函式 `load_proc` 和 `main` 的職責過於複雜，未遵循單一職責原則，難以測試和維護。
- **Q5：** 硬編碼的檔案名稱 `F_NAME`，降低程式的靈活性，無法輕易切換檔案來源。

---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 請將 `load_proc` 函式重構，加入例外處理，並使用 `with` 語法來處理檔案操作。

Prompt B： 請將全域變數 `d2` 改為函式參數，並確保所有函式都能正確傳遞和操作該參數。

Prompt C： 請將 `main` 函式中的命令解析邏輯拆分為獨立的函式，並遵循單一職責原則。
```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？ 是，AI 在重構 load_proc 時，漏掉了檢查檔案是否為空的邏輯。

2. 發現的問題： AI 重構後的程式碼在檔案為空時，仍然嘗試解析內容，導致程式崩潰。
3. 修正的對話： 請在讀取檔案內容後，檢查是否為空，若為空則回傳空清單，避免後續解析錯誤。

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
PS C:\Users\pclab\Desktop\irs_1779844448e4ba56cf6b581cc28ce7991f8427c277c4c82b99\NTUST-0527-Final-master> python modern_library.py
=== 圖書管理系統 v2.0 (Refactored) ===
輸入 help 查看可用指令
> add 深入淺出Python/978001/available
Success
> add 資料結構理論/978002/available
Success
> add 演算法實作/978003/available
Success
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show

書名                   ISBN            狀態
---------------------------------------------
深入淺出Python           978001          available
資料結構理論               978002          borrowed
演算法實作                978003          available

> exit
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
  {
    "title": "深入淺出Python",
    "isbn": "978001",
    "status": "available"
  },
  {
    "title": "資料結構理論",
    "isbn": "978002",
    "status": "borrowed"
  },
  {
    "title": "演算法實作",
    "isbn": "978003",
    "status": "available"
  }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)
a809fe1 (HEAD -> master) v2
b411048 加入 .gitignore 排除 .venv
c2edd96 MESSAGE

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/kai01222/B11409039-0527-Final
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
