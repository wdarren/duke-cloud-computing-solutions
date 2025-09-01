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