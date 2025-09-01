上傳Python/Flask 架構檔案ZIP檔來部署在Elastic Beanstalk PaaS 平台快速部署網站範例

## 一、ZIP 結構

zip 檔根目錄僅包含：application.py、requirements.txt、Procfile (無附檔名)

## 二、檔案內容
`Procfile`（無副檔名、 用 8000 埠）
```bash
web: gunicorn application:application --bind 0.0.0.0:8000
```
- Gunicorn (Green Unicorn) 是一個 Python WSGI HTTP server，用來在生產環境啟動 Flask、Django 等 WSGI 應用程式。
Elastic Beanstalk 預期用這個來跑 Flask
    - `web`:

        process type，代表這是一個 Web 服務。

        AWS Elastic Beanstalk（或 Heroku）會特別找 web 這一行來啟動主要 HTTP 應用。

        如果是背景工作（例如排程、任務隊列），可能會寫 worker:，但這裡必須是 web:。

    - gunicorn

        這是 WSGI HTTP server 的名字（Green Unicorn）。

        它會負責監聽連線、接收 HTTP 請求，並按照 WSGI 規範把請求交給 Python 的 Flask/Django app。

    - application:application

        格式是 模組名稱:變數名稱。

        第一個 application → 指檔案 application.py（不用加 .py）。

        第二個 application → 指檔案裡定義的 WSGI app 物件。

    - `--bind` 指定伺服器要監聽的 IP 與 Port。

    - `0.0.0.0` → 意味著「所有網卡、所有 IP 皆可存取」。

    - `:8000 `→ 綁定到 8000 埠。

`requirements.txt`
```ini
Flask==3.0.3
gunicorn==21.2.0
```
- 安裝指定版本 Flask

`application.py`（WSGI 入口變數要叫 application）
```python
from flask import Flask, jsonify

# EB 預設會尋找名為 `application` 的 WSGI 物件
application = Flask(__name__)

@application.route("/")
def index():
    return "Hello World"

@application.route("/echo/<name>")
def echo(name):
    return jsonify({"echo": name})

if __name__ == "__main__":
    # 本地測試用；部署到 EB 時由平台接手啟動
    application.run(host="0.0.0.0", port=8080)
```

## 三、本機快速自測（非必要）
### 建立虛擬環境（可選）
```bash
python -m venv .venv && source .venv/bin/activate  
# Windows: .venv\Scripts\activate

pip install -r requirements.txt
gunicorn application:application --bind 0.0.0.0:8000
```
- 確認 http://localhost:8000/ 出現 "Hello World"
- http://127.0.0.1:8080/echo/bob 出現 {"echo":"bob"}

## 四、正確打包 ZIP

重點：在含有三個檔案的目錄中執行打包，避免多一層資料夾。


## 五、部署步驟（UI：Application versions 先上傳）

進入 EB 主控台 → 新增 Application 

上傳 zip 做安裝檔

點說網址測試

## 補充說明
### 1. 背景問題

Flask / Django 本身不是 Web Server
它們只提供「如何處理請求 → 回應」的邏輯。
但要真正對外提供服務，需要一個能監聽 TCP/HTTP 連線的「伺服器程式」。

### 2. WSGI

WSGI (Web Server Gateway Interface) = Python 官方定義的 Web 伺服器 ↔ Web 應用程式之間的溝通協定。

它規定：Server 怎麼把 HTTP 請求交給 App，App 怎麼把回應丟回去。

Flask、Django 都實作了 WSGI，因此它們能跟任何 WSGI server 搭配。

### 3. WSGI HTTP Server 是什麼？

簡單說，它就是：

一個 真正會開 HTTP 連線、接收請求、管理 worker 的伺服器程式

依照 WSGI 規範，把請求交給 Python app，拿回回應，再傳給瀏覽器。

常見的實作：

- Gunicorn（最常用，Elastic Beanstalk 預設）

- uWSGI

- Waitress

- mod_wsgi（Apache 的 WSGI 模組）

### 4. 舉例流程（用 Gunicorn + Flask）

瀏覽器請求 → GET /

Gunicorn（WSGI server）接收 TCP/HTTP，解析成 Python 格式

依 WSGI 規範，把請求傳給 Flask 的 application

Flask 執行對應路由，回傳 "Hello World"

Gunicorn 把結果包裝成 HTTP Response，送回瀏覽器