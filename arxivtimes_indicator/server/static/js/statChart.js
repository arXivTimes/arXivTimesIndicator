Chart.pluginService.register(HorizonalLinePlugin);


function monthlyBars(elementID, chartData, legend){
    var labels = Object.keys(chartData).sort();
    var datasets = Object.keys(GENRE_NAMES).map(function(g){
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

    var yX = {
        stacked: true
    }
    var monthMax = 0
    Object.keys(chartData).forEach(function(ym){
        var values = Object.keys(chartData[ym]).map(function(g){return chartData[ym][g]});
        var total = values.reduce(function(prev, current){return prev + current});
        if(total > monthMax){
            monthMax = total;
        }
    })
    if(monthMax < CHART_BORDER){
        yX["ticks"] = {
            beginAtZero:true,
            min: 0,
            max: 25
        }
    }

    var ctx = document.getElementById(elementID).getContext("2d");
    var monthlyBars = new Chart(ctx, {
        type: "bar",
        data: barChartData,
        options: {
            tooltips: {
                mode: "index",
                intersect: false
            },
            legend: {
                display: (legend !== undefined && !legend) ? false : true
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [yX]
            },
            horizontalLine: [{
                y: CHART_BORDER,
                style: "#b0c4de",
                text: "200/year line"
            }]
        }
    });

    return monthlyBars;
}


function kindsPie(elementID, chartData, legend){
    var genres = Object.keys(chartData);
    var total = genres.reduce(function(prev, current, index){
        return prev + chartData[current]; 
    }, 0)

    var dataset = {
        data: genres.map(function(g){ return Math.round((chartData[g] / total) * 10000) / 100}),
        backgroundColor: genres.map(function(g){ return GENRE_COLOR[g]})
    }

    var pieChartData = {
        labels: genres.map(function(g){ return GENRE_NAMES[g] }),
        datasets: [dataset]
    }

    var ctx = document.getElementById(elementID).getContext("2d");
    var kindsPie = new Chart(ctx, {
        type: "pie",
        data: pieChartData,
        options: {
            tooltips: {
                mode: "index",
                intersect: false,
                callbacks: {
                    label: function(tooltipItem, data) {
                        var n = data["labels"][tooltipItem.index];
                        var d = data["datasets"][tooltipItem.datasetIndex]["data"][tooltipItem.index];
                        return n + ":" + d + "%";
                    }
                }
            },
            cutoutPercentage: 50,
            legend: {
                display: (legend !== undefined && !legend) ? false : true
            },
            responsive: true,
            maintainAspectRatio: false
        }
    });

    return kindsPie
}