import time

from py_lightweight_charts import *


if __name__ == '__main__':
    
    # Construct and start the server
    plwc = PyLightweightCharts("Live data")
    plwc.start()
    
    # Create the main chart
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
    
    # These two series will be added to the main chart
    candles = Series("candles", SeriesType.CANDLESTICK, {})
    line1 = Series("line1", SeriesType.LINE, { "color": "#0e69fb" })
    
    chart.add_series(candles)
    chart.add_series(line1)

    
    # Create the sub-chart
    chart2_options = chart_options
    chart2_options['height'] = 815.5 - 500
    chart2 = Chart('sub_chart', chart2_options)
    plwc.add_chart(chart2)
    
    # This series will be added ot the subchart
    line2 = Series("line2", SeriesType.LINE, { "color": "#0e69fb" })

    chart2.add_series(line2)

    # Simulate new data
    while True:
        
        # Update the main chart series
        candle_data = {
            "time": time.time(),
            "open": 120 + (time.time() % 5),
            "high": 125 + (time.time() % 5),
            "low": 115 + (time.time() % 5),
            "close": 122 + (time.time() % 5),
        }
        candles.update(candle_data)
        line1.update({
                "time": time.time(),
                "value": 122 + (time.time() % 5)
            })
        
        # Update the subchart series
        line2.update({
                "time": time.time(),
                "value": 125 + (time.time() % 5)
            })
        
        time.sleep(5)
        