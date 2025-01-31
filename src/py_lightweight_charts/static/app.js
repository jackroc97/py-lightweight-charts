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
        const chartDiv = document.createElement("div");
        chartDiv.setAttribute("id", chart.id);
        document.getElementById("chart-container").appendChild(chartDiv);

        // Create the chart and add it to chartMap so it may be referenced 
        chartMap[chart.id] = LightweightCharts.createChart(
            document.getElementById(chart.id), chart.options);

        callback();
    });

    // Add a series to a chart
    socket.on('add_series', (chart, series) => {
        switch (series.type) {
            case 'area':
                dataMap[series.id] = chartMap[chart.id].addSeries(LightweightCharts.AreaSeries, series.options);
                break;
            case 'bar':
                dataMap[series.id] = chartMap[chart.id].addSeries(LightweightCharts.BarSeries, series.options);
                break;
            case 'baseline':
                dataMap[series.id] = chartMap[chart.id].addSeries(LightweightCharts.BaselineSeries, series.options);
                break;
            case 'candlestick':
                dataMap[series.id] = chartMap[chart.id].addSeries(LightweightCharts.CandlestickSeries, series.options);
                break;
            case 'histogram':
                dataMap[series.id] = chartMap[chart.id].addSeries(LightweightCharts.HistogramSeries, series.options);
                break;
            case 'line':
                dataMap[series.id] = chartMap[chart.id].addSeries(LightweightCharts.LineSeries, series.options);
                break;
            default:
                break;
        }
    });

    // Set data for a series
    socket.on('set_data', (series_id, data) => {
        dataMap[series_id].setData(data);
    });

    // Update data for a series
    socket.on('update', (series_id, data) => {
        dataMap[series_id].update(data);
    });

    // Set markers on a series
    socket.on('set_markers', (seriesId, markers) => {
        // TODO: Implement the new setMarkers method which allows
        // series markers to be udpated.  For now, this will do as a workaround
        // that emulates v4 behavior.
        const seriesMarkers = LightweightCharts.createSeriesMarkers(dataMap[seriesId], markers);
    });
});
