from flask import Flask, render_template, request
from stock import get_stock_data, perform_regression, predict_stock_price, plot_stock_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_image = None
    stock_code = ""
    days = 365
    future_days = 5
    target_price = None  # 新增目標價變數

    if request.method == 'POST':
        stock_code = request.form['stock_code'].strip()

        # 🔹 自動補上 .TW，確保查詢的是台股
        if not stock_code.endswith(".TW"):
            stock_code += ".TW"

        days = request.form.get('days', 365)
        future_days = request.form.get('future_days', 5)

        try:
            days = int(days)
            future_days = int(future_days)
            if days < 1:
                days = 1
            if future_days < 1:
                future_days = 1
        except ValueError:
            days = 365
            future_days = 5

        # 取得股票資料
        data = get_stock_data(stock_code, days)
        if not data.empty:
            data, model = perform_regression(data)
            predicted_data = predict_stock_price(model, data.index[-1], future_days)
            plot_image = plot_stock_data(data, predicted_data, future_days)

            # 目標價為預測的最後一天股價
            target_price = round(predicted_data.iloc[-1]['Predicted Close'], 2)

    return render_template('index.html', plot_image=plot_image, target_price=target_price,
                           stock_code=stock_code, days=days, future_days=future_days)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)