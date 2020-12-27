timeSeriesChart = null 

$(document).ready(function() {
    fetch("/getOldPrices/FPT")
        .then(response => response.json())
        .then(jsonData => {
            console.log(jsonData)
            timeSeries = parseTimeFromResponse(jsonData)
            priceSeries = parsePriceFromResponse(jsonData)

            fetch("getPredict/FPT/prophet")
                .then(response => response.json())
                .then(jsonData => {
                    timeSeriesPredict = parseTimeFromResponse(jsonData)
                    priceSeriesPredict = parsePriceFromResponse(jsonData)
                    plotStockPriceLineChart("stock-price-chart", timeSeries, priceSeries, timeSeriesPredict, priceSeriesPredict)
                })
                .catch(error => console.debug(error))

        })
        .catch(error => console.debug(error))
        
    
});

function getCurrentTime(){
    return moment().format('MMMM Do YYYY, h:mm:ss a')
}

// draw stock pricing charts
function parseTimeFromResponse(jsonDates){
    return jsonDates.map((item, index) =>{
        return moment(item["time"], "DD/MM/YYYY hh:mm:ss").toDate()
    })
}

function parsePriceFromResponse(jsonPrices){
    return jsonPrices.map((item, index) =>{
        return item["price"]
    })
}


function plotStockPriceLineChart(chartId, dates, prices, datesPredict, pricesPredict){
    am4core.ready(function() {

        am4core.useTheme(am4themes_animated);
        if (!timeSeriesChart){
            timeSeriesChart = am4core.create(chartId, am4charts.XYChart);
        }
        
        let data = [];
        dates.forEach((date, index) => {
            data.push({date: new Date(date), "price_actual": prices[index], "price_predict": null})
        })
        datesPredict.forEach((date, index) =>{
            data.push({date: new Date(date), "price_actual": null, "price_predict": pricesPredict[index]})
        })

        console.log(data)

        timeSeriesChart.data = data;
        
        // Create axes
        let dateAxis = timeSeriesChart.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.minGridDistance = 60;
        dateAxis.title.text = "Thời gian"
        
        let valueAxis = timeSeriesChart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.title.text = "Giá trị (Đơn vị: Nghìn VNĐ)"
        
        // Create series
        let series1 = timeSeriesChart.series.push(new am4charts.LineSeries());
        series1.name = "True prices";
        series1.stroke = am4core.color("#332288");
        series1.strokeWidth = 1;
        series1.dataFields.valueY = "price_actual";
        series1.dataFields.dateX = "date";
        series1.tooltipText = "Giá trị thực: {price_actual}"

        let series2 = timeSeriesChart.series.push(new am4charts.LineSeries());
        series2.name = "Predict prices"
        series2.stroke = am4core.color("red");
        series2.strokeWidth = 1;
        series2.dataFields.valueY = "price_predict";
        series2.dataFields.dateX = "date";
        series2.tooltipText = "Giá dự đoán: {price_predict}"
        
        series1.tooltip.pointerOrientation = "vertical";
        series2.tooltip.pointerOrientation = "vertical";

        timeSeriesChart.cursor = new am4charts.XYCursor();
        timeSeriesChart.cursor.snapToSeries = [series1, series2];
        timeSeriesChart.cursor.xAxis = dateAxis;
        
        // chart.scrollbarY = new am4core.Scrollbar();
        timeSeriesChart.scrollbarX = new am4core.Scrollbar();
        
        });    
}

