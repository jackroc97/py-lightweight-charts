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
        console.log("Add chart requested");
        console.log(chart);

        // Create a new element for the chart
        chartDiv = document.createElement("div");
        chartDiv.setAttribute("id", chart.id);
        document.getElementById("chart-container").appendChild(chartDiv);

        // Create the chart and add it to chartMap so it may be referenced 

        const chart = LightweightCharts.createChart(
            document.getElementById(chart.id), chart.options);
        console.log(chart);
        console.log(chart.addAreaSeries)

        chartMap[chart.id] = chart;
        console.log(chartMap[chart.id])
        console.log(chartMap[chart.id].addAreaSeries)

        callback();
    });

    // Add a series to a chart
    socket.on('add_series', (chart, series) => {
        console.log("Add series requested");
        console.log(series);
        console.log(chart.id);
        console.log(chartMap);
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
    });

    // Set data for a series
    socket.on('set_data', (series_id, data) => {
        console.log("Set data requested for ", series_id);
        dataMap[series_id].setData(data);
    });

    // Update data for a series
    socket.on('update', (series_id, data) => {
        console.log("Update data requested for ", series_id);
        dataMap[series_id].update(data);
    });

    // Set markers on a series
    socket.on('set_markers', (seriesId, markers) => {
        if (dataMap[seriesId]) {
            dataMap[seriesId].setMarkers(markers);
        }
    });
});
