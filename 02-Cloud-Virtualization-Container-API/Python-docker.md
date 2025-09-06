# 流程總覽

1. `git clone` 專案骨架
2. 建立虛擬環境（必須使用 `python3 -m venv`）, 建立`requirements.txt`、`Makefile`、`app.py`等檔案。
3. 安裝 **hadolint**, 以做Lint。
4. 撰寫 **Dockerfile**
5. 本機 `docker build`、`docker run` 驗證。
6. 建立 **Docker Hub** 帳號並登入 `docker login`。
7. `docker push` 映像至 Docker Hub。
8. 他人可直接 `docker pull` 你的映像並執行。

## Python 虛擬環境（Cloud9）

```bash
python3 -m venv ~/.dockerproj
source ~/.dockerproj/bin/activate
```
### Makefile（常用目標）

```makefile
setup:
	python3 -m venv ~/.dockerproj

install:
	pip install --upgrade pip && \
	pip install -r requirements.txt

test:
	# python -m pytest -vv --cov=myrepolib tests/*.py
	# python -m pytest --nbval notebook.ipynb

lint:
	hadolint Dockerfile
	pylint --disable=R,C,W1203 app.py

all: install lint test

```
### requirements.txt（示例）

```
pylint
click
```

### app.py（使用 Click 的極簡 CLI）

```python
#!/usr/bin/env python
import click

@click.command()
def hello():
    click.echo('Hello World!')

if __name__ == '__main__':
    hello()
```
## 製作 Dockerfile
### 安裝 [[hadolint]]（可在 root 下進行）

```bash
sudo su -
curl -sSL -o hadolint \
  https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64

sudo mv hadolint /usr/local/bin/
sudo chmod +x /usr/local/bin/hadolint

# 驗證
hadolint --version
exit
```
### Dockerfile（以官方 Python 3.12-slim 為基底)

```dockerfile
FROM python:3.12-slim

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . app.py /app/

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt
```
### 本機 `docker build`、`docker run` 驗證
```bash
docker build -t hello-docker .
docker run --rm hello-docker
```	
## 上傳到 Docker Hub
### 建立 Docker Hub 帳號並登入

```bash
docker login
```
### `docker push` 映像至 Docker Hub

```bash	
docker tag hello-docker your-dockerhub-username/hello-docker:latest
docker push your-dockerhub-username/hello-docker:latest
```	
### 他人可直接 `docker pull` 你的映像並執行

```bash		
docker pull your-dockerhub-username/hello-docker:latest
docker run --rm your-dockerhub-username/hello-docker:latest
```





