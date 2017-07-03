var CHART_BORDER = 16;

var horizonalLinePlugin = {
    afterDatasetsDraw: function(chartInstance) {
        var yScale = chartInstance.scales["y-axis-0"];
        var xScale = chartInstance.scales["x-axis-0"];
        var canvas = chartInstance.chart;
        var ctx = canvas.ctx;
        console.log("x")
        if (chartInstance.options.horizontalLine) {
            for (var index = 0; index < chartInstance.options.horizontalLine.length; index++) {
                var line = chartInstance.options.horizontalLine[index];
                var yValue = 0;
                var xPadding = xScale.getPixelForValue(undefined, 0);
                var style = "rgba(169,169,169, .6)";

                if (line.y) {
                    yValue = yScale.getPixelForValue(line.y);
                }
                if (line.style) {
                    style = line.style;
                }
                
                ctx.lineWidth = 2;
                ctx.beginPath();
                console.log();
                ctx.moveTo(xPadding, yValue);
                ctx.lineTo(canvas.width - xPadding, yValue);
                ctx.strokeStyle = style;
                ctx.stroke();

                if (line.text) {
                    ctx.fillStyle = style;
                    var offset = line.text.length * 6;
                    ctx.fillText(line.text, canvas.width - xPadding - offset, yValue + ctx.lineWidth);
                }
            }
            return;
        }
  }
};
Chart.pluginService.register(horizonalLinePlugin);

var chartData = PAPERS.recent.map(function(p){
    var year_month_day = p.created_at.split("T")[0].split("-");
    var year_month = year_month_day[0] + "/" + year_month_day[1];
    var genres = [];
    for(var g in LABEL_TO_GENRE){
        LABEL_TO_GENRE[g].forEach(function(lb){
            if(p.labels.indexOf(lb) > -1){
                if(genres.indexOf(g) == -1){
                    genres.push(g);                    
                }
            }
        })
    }
    return {
        "ym": year_month, "genres": genres
    }
}).reduce(function(prev, current){
    var d = prev;
    var target = [current];
    if("ym" in d){
        d = {};
        target = [prev, current];
    }
    for(var i = 0; i < target.length; i++){
        if(!(target[i].ym in d)){
            d[target[i].ym] = {}
        }
        target[i].genres.forEach(function(g){
            if(!(g in d[current.ym])){
                d[target[i].ym][g] = 1;
            }else{
                d[target[i].ym][g] += 1;
            }
        })
    }
    return d;
})

for(var ym in chartData){
    for(var g in LABEL_TO_GENRE){
        if(!(g in chartData[ym])){
            chartData[ym][g] = 0;  // 0 filling if genre is missed in target ym
        }
    }
}

var labels = Object.keys(chartData).sort();
var datasets = Object.keys(LABEL_TO_GENRE).map(function(g){
    var data = labels.map(function(ym){
        return chartData[ym][g];
    })
    return {
        label: GENRE_NAMES[g],
        type: "bar",
        data: data,
        backgroundColor: GENRE_COLOR[g]
    }
})

var barChartData = {
    labels: labels,
    datasets: datasets
}

window.onload = function() {
    var ctx = document.getElementById("chart").getContext("2d");
    window.myBar = new Chart(ctx, {
        type: "bar",
        data: barChartData,
        options: {
            tooltips: {
                mode: "index",
                intersect: false
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            },
            "horizontalLine": [{
                "y": CHART_BORDER,
                "style": "#b0c4de",
                "text": "200/year line"
            }]
        }
    });
};
