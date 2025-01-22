import time
import pandas as pd

from py_lightweight_charts import *

if __name__ == '__main__':

    # Read in data
    df = pd.read_csv("demos/ES_2023.csv", index_col=0)
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['time'] = df['date'].astype('int64') // 10**9    
    
    # Construct and start the server
    plwc = PyLightweightCharts()
    plwc.start(daemon=False)
    
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
    candles = Series("candles", SeriesType.CANDLESTICK)
    volume = Series("volume", SeriesType.HISTOGRAM, { "priceScaleId": "volume" })
    
    # Select data to be displayed on the chart
    df['color'] = ['rgba(38, 166, 154, 0.5)' if c > o else 'rgba(239, 83, 80, 0.5)' for o, c in zip(df['open'], df['close'])]        
    candles_dict = df[['time', 'open', 'high', 'low', 'close']].to_dict('records')
    volume_dict = df[['time', 'volume', 'color']].rename(columns={'volume': 'value'}).to_dict('records')
    
    chart.update_series(candles, candles_dict)
    chart.update_series(volume, volume_dict)

    t1 = df.iloc[-2]["time"]
    t2 = time=df.iloc[-5]["time"]
    
    print(t1)
    print(t2)
    
    # Add some markers to the chart
    markers = [
        Marker(time=int(df.iloc[-2]["time"]), position='aboveBar', color='rgba(0, 255, 0, 0.5)', shape='arrowUp', text='Buy signal'),
        Marker(time=int(df.iloc[-5]["time"]), position='belowBar', color='rgba(255, 0, 0, 0.5)', shape='arrowDown', text='Sell signal'),
    ]

    candles.set_markers(markers)

