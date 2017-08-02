var GENRE_NAMES = {
    "cv": "Computer Vision",
    "nlp": "Natural Language Processing",
    "opt": "Optimization",
    "rl": "Reinforcement Learning",
    "audio": "Audio Processing"
};

var GENRE_COLOR = {
    "cv": "#fef2c0",
    "nlp": "#c2e0c6",
    "opt": "#deb887",
    "rl": "#e99695",
    "audio": "#d8bfd8"
};

var CHART_BORDER = 16;

var HorizonalLinePlugin = {
    afterDraw: function(chartInstance) {
        var yScale = chartInstance.scales["y-axis-0"];
        var xScale = chartInstance.scales["x-axis-0"];
        var canvas = chartInstance.chart;
        var ctx = canvas.ctx;
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

document.addEventListener("DOMContentLoaded", function () {
    var $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll(".navbar-burger"), 0);
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(function ($el) {
            $el.addEventListener("click", function () {
                var target = $el.dataset.target;
                var $target = document.getElementById(target);
                $el.classList.toggle("is-active");
                $target.classList.toggle("is-active");
            });
        });
    }
});