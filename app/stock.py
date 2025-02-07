import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression

def get_stock_data(stock_code, days):
    """ 爬取指定天數的股票資料 """
    period = f"{days}d"  # 設定查詢天數
    stock = yf.Ticker(stock_code)
    data = stock.history(period=period)  # 爬取資料
    return data

def perform_regression(data):
    """ 執行線性回歸分析 """
    data['Date'] = pd.to_datetime(data.index)
    data['Date_ordinal'] = data['Date'].map(lambda x: x.toordinal())  # 轉換日期為數字
    
    # 準備自變數與因變數
    X = data[['Date_ordinal']]
    y = data['Close']
    
    # 訓練線性回歸模型
    model = LinearRegression()
    model.fit(X, y)
    
    # 預測回歸直線
    data['Regression_Line'] = model.predict(X)
    return data, model

def predict_stock_price(model, last_date, periods=5):
    """ 預測未來股價 """
    future_dates = pd.date_range(start=last_date, periods=periods+1, freq='B')[1:]  # 預測未來交易日
    future_dates_ordinal = future_dates.map(lambda x: x.toordinal()).values.reshape(-1, 1)
    
    predicted_prices = model.predict(future_dates_ordinal)
    
    predicted_data = pd.DataFrame({
        'Date': future_dates,
        'Predicted Close': predicted_prices
    })
    return predicted_data

def plot_stock_data(data, predicted_data, periods=5):
    """ 繪製股價、回歸線與未來預測股價，X 軸根據時間長度動態調整 """
    plt.figure(figsize=(12, 6))
    
    # 繪製歷史股價
    plt.plot(data.index, data['Close'], label='Historical Close Price', color='blue', linestyle='-', marker='o')
    
    # 繪製回歸線
    plt.plot(data.index, data['Regression_Line'], label='Regression Line', color='blue', linestyle='--', linewidth=1)

    # 繪製未來預測股價
    plt.plot(predicted_data['Date'], predicted_data['Predicted Close'], label=f'Predicted Close Price for Next {periods} Days', color='red', linestyle='--', marker='x')

    # 設定標題與標籤
    plt.title(f"Stock Price Prediction for the Next {periods} Days")
    plt.xlabel("Date")
    plt.ylabel("Price (TWD)")

    # 設定 X 軸間隔（根據數據範圍自動調整）
    date_range = (data.index[-1] - data.index[0]).days

    if date_range <= 30:  # 少於 1 個月，每 3 天顯示一次
        interval = 3
    elif date_range <= 90:  # 1~3 個月，每 7 天顯示一次
        interval = 7
    elif date_range <= 180:  # 3~6 個月，每 14 天顯示一次
        interval = 14
    else:  # 6 個月以上，每 30 天顯示一次
        interval = 30

    plt.xticks(rotation=45)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=interval))

    # 顯示網格與圖例
    plt.grid(True)
    plt.legend()

    # 保存圖像
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()

    return img_base64

