import time
import pandas as pd

from py_lightweight_charts import *

if __name__ == '__main__':

    # Read in data
    df = pd.read_csv("demos/ES_2023.csv", index_col=0)
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['time'] = df['date'].astype('int64') // 10**9    
    
    # Construct and start the server
    plwc = PyLightweightCharts("ES 2023")
    plwc.start(daemon=False)
    
    # Create the main chart
    chart_options = {
        'layout': {
            'background': { 'color': '#222' },
            'textColor': '#DDD',
            'attributionLogo': False
        },
        'grid': {
            'vertLines': { 'color': '#444' },
            'horzLines': { 'color': '#444' },
         },
        'leftPriceScale': {
            'visible': False,
            'scaleMargins': {
                'top': 0.8,
                'bottom': 0
            }
        },
    }
    
    chart = Chart('main_chart', chart_options)
    plwc.add_chart(chart)
    
    # These two series will be added to the main chart
    candles = Series("candles", SeriesType.CANDLESTICK)
    volume = Series("volume", SeriesType.HISTOGRAM, { "priceScaleId": "left" })
    
    chart.add_series(candles)
    chart.add_series(volume)
    
    # Select data to be displayed on the chart
    df['color'] = ['rgba(38, 166, 154, 0.5)' if c > o else 'rgba(239, 83, 80, 0.5)' for o, c in zip(df['open'], df['close'])]        
    candles_dict = df[['time', 'open', 'high', 'low', 'close']].to_dict('records')
    volume_dict = df[['time', 'volume', 'color']].rename(columns={'volume': 'value'}).to_dict('records')
    
    candles.set_data(candles_dict)
    volume.set_data(volume_dict)
