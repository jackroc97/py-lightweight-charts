import time
from py_lightweight_charts.chart import Chart
from py_lightweight_charts import PyLightweightCharts

if __name__ == '__main__':
    
    plwc = PyLightweightCharts()
    plwc.start()
    time.sleep(5)
    
    chart_options = {
        'height': 500,
        'width': 1440,
        'layout': {
            'background': { 'color': '#222' },
            'textColor': '#DDD',
        },
        'grid': {
            'vertLines': { 'color': '#444' },
            'horzLines': { 'color': '#444' },
         },
    }
    chart = Chart('main_chart', chart_options)
    plwc.add_chart(chart)
    time.sleep(1)
    
    chart2_options = chart_options
    chart2_options['height'] = 815.5 - 500
    chart2 = Chart('sub_chart', chart2_options)
    plwc.add_chart(chart2)
    time.sleep(1)

    while True:
        # Simulate new candlestick data being pushed to the chart
        candle_data = {
            "time": time.time(),
            "open": 120 + (time.time() % 5),
            "high": 125 + (time.time() % 5),
            "low": 115 + (time.time() % 5),
            "close": 122 + (time.time() % 5),
        }
        
        candle_series = {
            "id": "AAA",
            "type": "candlestick",
            "data": candle_data
        }
        
        line_series = {
            "id": "BBB",
            "type": "line",
            "data": {
                "time": time.time(),
                "value": 122 + (time.time() % 5)
            },
            "options": {
                "color": "#0e69fb"
            }
        }
        
        chart.update_data(candle_series)
        chart.update_data(line_series)
        
        other_line = {
            "id": "CCC",
            "type": "line",
            "data": {
                "time": time.time(),
                "value": 125 + (time.time() % 5)
            },
            "options": {
                "color": "#0e69fb"
            }
        }
        chart2.update_data(other_line)
        
        time.sleep(5)