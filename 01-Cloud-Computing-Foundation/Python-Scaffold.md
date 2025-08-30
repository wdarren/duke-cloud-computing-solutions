### 建立 GitHub 專案
* 點選 `New repository`
* 命名為 python-scaffold
* 勾選：
  * Add a README file
  * Add .gitignore → 選擇 Python
* 點選 Create repository
### 開啟 AWS Cloud9 並執行以下指令 (要在 Cloud9 建立環境才需要)

設定 SSH 金鑰
```bash
ssh-keygen -t rsa
cat ~/.ssh/id_rsa.pub
```

複製這段文字後，到 GitHub：

* Settings → SSH and GPG keys → New SSH Key → 貼上並命名為 python-scaffold

### 複製 GitHub Repo

```bash
git clone [repo 連結]
cd python-scaffold
```
### 建立初始檔案與虛擬環境
```bash
touch Makefile hello.py test_hello.py requirements.txt
python3 -m venv .venv
source .venv/bin/activate
```
**python3**
→ 呼叫 Python 3 的直譯器。

* `m venv`
→ 使用 Python 內建的 venv 模組 來建立虛擬環境。

* `.vnev`
→ 在目前資料夾底下建立 '.venv'虛擬環境資料夾。

**source**
→ 在 shell裡執行某個腳本，並讓它修改目前的環境變數。

* `.venv/bin/activate`
→ 這就是虛擬環境建立時自動生成的「啟用腳本」。
→ 執行它之後會：

  * 改變 $PATH，讓你打 python / pip 時指向 ~/.scaffold/bin/python 而不是系統的全域 Python。

  *  在命令列提示符（prompt）前加上 (scaffold)，提醒你目前處於這個環境。
### 編寫 Makefile

在 `Makefile` 中加入以下內容

```
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

install-azure:
	pip install --upgrade pip &&\
		pip install -r requirements-azure.txt

format:
	black *.py

lint:
	pylint --disable=R,C hello.py

test:
	python -m pytest -vv --cov=hello test_hello.py

all: install lint test
```
**Makefile 是自動化指令集合, 使用方式**

假設你的檔名是 Makefile，在專案根目錄輸入：
```bash
make install        # 安裝基本需求
make install-azure  # 安裝 Azure 需求
make format         # 格式化程式碼
make lint           # 靜態檢查
make test           # 執行測試
make all            # 一次做完以上所以
```
**format**
```bash
format:
	black *.py
```
* 把當前資料夾下所有 Python 檔案，自動套用 Black 的統一程式碼風格（乾淨、統一、可讀性高）

**lint**
```
lint:
	pylint --disable=R,C hello.py
```

* 用 pylint 做靜態檢查。

  * --disable=R,C → 關掉 所有 R 類 (Refactor) 和 C 類 (Convention) 規則，通常是一些「程式風格建議」，不是 bug。

  * 換句話說，你只會看到 更嚴重的 W (Warning) 和 E (Error)。

**test**
```bash
test:
	python -m pytest -vv --cov=hello test_hello.py
```

* -vv → 顯示更詳細的測試資訊。
* --cov=hello → 計算 hello.py 的程式碼覆蓋率。
* test_hello.py → 指定測試檔案。
### 編寫 requirements.txt
```bash
pylint
pytest
click
black
pytest-cov
```
### 編寫 hello.py
```python
def add(x, y):
    return x + y

result = add(1, 2)
print(f"This is the sum of 1 and 2: {result}")
```
### 編寫 test_hello.py

```python
from hello import add

def test_add():
    assert add(1, 2) == 3
```
### 安裝並執行 Makefile 任務
```bash
make install
make lint
make format
make test
make all
```
### 提交並推送到 GitHub
```bash
git add *
git commit -m "Initial python-scaffold project setup"
git push origin main
```