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
        'height': 815,
        'width': 1440,
        'layout': {
            'background': { 'color': '#222' },
            'textColor': '#DDD',
            'panes': {
                'separatorColor': '#f22c3d',
                'separatorHoverColor': 'rgba(255, 0, 0, 0.1)',
                # setting this to false will disable the resize of the panes by the user
                'enableResize': True,
            },
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
    
    chart.add_series(candles)
    chart.add_series(volume)
    
    close = Series("close", SeriesType.LINE, { "color": "#0e69fb" })
    chart.add_series(close, pane_id=1)
    
    # Select data to be displayed on the chart
    df['color'] = ['rgba(38, 166, 154, 0.5)' if c > o else 'rgba(239, 83, 80, 0.5)' for o, c in zip(df['open'], df['close'])]        
    candles_dict = df[['time', 'open', 'high', 'low', 'close']].to_dict('records')
    volume_dict = df[['time', 'volume', 'color']].rename(columns={'volume': 'value'}).to_dict('records')
    close_dict = df[['time', 'close']].rename(columns={'close': 'value'}).to_dict('records')
    
    candles.set_data(candles_dict)
    volume.set_data(volume_dict)
    close.set_data(close_dict)
