$(document).ready(function() {
    
    const chartMap = {};

    const dataMap = {};
    
    const socket = io();
    
    socket.on('add_chart', (chart) => {
        // Create a new element for the chart
        chartDiv = document.createElement("div");
        chartDiv.setAttribute("id", chart.id);
        document.getElementById("chart-container").appendChild(chartDiv);

        // Create the chart and add it to chartMap so it may be referenced 
        chartMap[chart.id] = LightweightCharts.createChart(
            document.getElementById(chart.id), chart.options);
    });

    // Expect series to have the an `id` and `type`
    // Optionally, it may have `data` and `options` properties
    socket.on('update_series', (chart, series) => {        
        if (!dataMap[series.id]) {
            switch (series.type) {
                case 'area':
                    dataMap[series.id] = chartMap[chart.id].addAreaSeries(series.options);
                    break;
                case 'bar':
                    dataMap[series.id] = chartMap[chart.id].addBarSeries(series.options);
                    break;
                case 'baseline':
                    dataMap[series.id] = chartMap[chart.id].addBaselineSeries(series.options);
                    break;
                case 'candlestick':
                    dataMap[series.id] = chartMap[chart.id].addCandlestickSeries(series.options);
                    break;
                case 'histogram':
                    dataMap[series.id] = chartMap[chart.id].addHistogramSeries(series.options);
                    break;
                case 'line':
                    dataMap[series.id] = chartMap[chart.id].addLineSeries(series.options);      
                    break;
                default:
                    break;
            }
            dataMap[series.id].setData(series.data);
        }
        else {
            dataMap[series.id].update(series.data);
        }
    });
});

// Adding a window resize event handler to resize the chart when
// the window size changes.
// Note: for more advanced examples (when the chart doesn't fill the entire window)
// you may need to use ResizeObserver -> https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver
window.addEventListener('resize', () => {
    chart.resize(window.innerWidth, window.innerHeight);
});