# 使用官方 Python 映像檔
FROM python:3.11

# 設定工作目錄
WORKDIR /app

# 安裝必要的系統套件
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 依賴
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 將所有內容掛載
COPY . .

# 暴露 Flask 預設埠
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "app.py"]
