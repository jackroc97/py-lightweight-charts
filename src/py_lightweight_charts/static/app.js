$(document).ready(function() {
    
    // Stores charts that are created by the user
    const chartMap = {};

    // Stores series that are created by the user
    const dataMap = {};

    // Websocket connection
    const socket = io();
    
    // Let the server know that the client is ready
    socket.emit('ready');

    // Add a chart to the page
    socket.on('add_chart', (chart, callback) => {
        // Create a new element for the chart
        chartDiv = document.createElement("div");
        chartDiv.setAttribute("id", chart.id);
        document.getElementById("chart-container").appendChild(chartDiv);

        // Create the chart and add it to chartMap so it may be referenced 
        chartMap[chart.id] = LightweightCharts.createChart(
            document.getElementById(chart.id), chart.options);

        callback();
    });

    // Update series data on a chart
    socket.on('update_series', (chart, series, data) => {        
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
            dataMap[series.id].setData(data);
        }
        else {
            dataMap[series.id].update(data);
        }
    });
});