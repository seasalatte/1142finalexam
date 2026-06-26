# 1142 Web 程式設計 --- 期末考
Flask-WTF + SQLite 客戶管理系統 (含登入控管)

## 檔案結構與說明
* `app.py` : 主程式
* `requirements.txt` : 執行本專案所需的 Python 套件紀錄(用 pip freeze 產生)
* `templates/` : HTML 檔案
* `static/css/style.css` : CSS 檔案

## 執行操作步驟

1. 開 cmd 切換到你想存放專案的資料夾目錄, 然後執行 git clone <br>
`git clone https://github.com/seasalatte/1142finalexam.git`
2. 切換進入該專案資料夾, 建立虛擬環境 <br>
`python -m venv env` <br>
`venv\Scripts\activate`
3. 安裝必要套件 <br>
(env) `pip install -r requirements.txt`
4. 執行 <br>
(env) `flask --debug run`
5. 到瀏覽器, 輸入 http://127.0.0.1:5000 <br>
