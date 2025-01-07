import time
from py_lightweight_charts.chart import Chart

if __name__ == '__main__':
    # Instantiate the Chart class
    chart = Chart()
    chart.start()

    while True:
        # Simulate new candlestick data being pushed to the chart
        new_data = {
            "time": time.time() / 1000,
            "open": 120 + (time.time() % 5),
            "high": 125 + (time.time() % 5),
            "low": 115 + (time.time() % 5),
            "close": 122 + (time.time() % 5),
        }
        
        series = {
            "id": "AAA",
            "type": "candlestick",
            "data": new_data
        }
        
        new_line = {
            "id": "BBB",
            "type": "line",
            "data": {
                "time": time.time() / 1000,
                "value": 122 + (time.time() % 5)
            },
            "options": {
                "color": "#0e69fb"
            }
        }
        
        chart.update_data(series)
        chart.update_data(new_line)
        time.sleep(5)