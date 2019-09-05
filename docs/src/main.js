let palette = {
    increase: '#adff2f',
    decrease: '#e93d27',
    font: '#000000'
}

Chart.defaults.global.defaultFontColor = palette.font;

// Details trend chart
let line_trend_increase = document.getElementById("line_trend_increase");
let predictions = JSON.parse(line_trend_increase.getAttribute("data"));

let labels = predictions.map(summary => summary.date.split(' ')[0]);
let data = predictions.map(summary => summary.prediction.increase);
let line_chart_data = {
    labels: [""].concat(labels),
    datasets: [{
        data: [0].concat(data),
        label: "Passed",
        fill: true,
        backgroundColor: 'transparent',
        borderColor: palette.increase,
        borderWidth: 2,
        pointBackgroundColor: palette.increase
    }]
}

let line_chart_increase = new Chart(line_trend_increase, {
    type: 'line',
    data: line_chart_data,
    options: {
        responsive: true,
        title: {
            fontSize: 20,
            display: false,
            text: "Increase predict"
        },
        legend: {
            display: false,
            position: 'bottom',
            fontColor: '#000000'
        },
        scales: {
            xAxes: [{}],
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                scaleLabel: {
                    fontSize: 20,
                    display: true,
                    labelString: "increase prediction"
                }
            }]
        }
    }
});

// Details trend chart
let line_trend_decrease = document.getElementById("line_trend_decrease");

data = predictions.map(summary => summary.prediction.decrease);
line_chart_data = {
    labels: [""].concat(labels),
    datasets: [{
        data: [0].concat(data),
        label: "Passed",
        fill: true,
        backgroundColor: 'transparent',
        borderColor: palette.decrease,
        borderWidth: 2,
        pointBackgroundColor: palette.decrease,
    }]
}

let line_chart_decrease = new Chart(line_trend_decrease, {
    type: 'line',
    data: line_chart_data,
    options: {
        responsive: true,
        title: {
            fontSize: 20,
            display: false,
            text: "Decrease predict"
        },
        legend: {
            display: false,
            position: 'bottom'
        },
        scales: {
            xAxes: [{}],
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                scaleLabel: {
                    fontSize: 20,
                    display: true,
                    labelString: "decrease prediction"
                }
            }]
        }
    }
});
