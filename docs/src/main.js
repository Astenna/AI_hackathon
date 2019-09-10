let palette = {
    increase: '#adff2f',
    decrease: '#e93d27',
    font: '#3e423e',
    blue: '#34ced9',
    gray: '#bfbfbf'
}

Chart.defaults.global.defaultFontColor = palette.font;

// Details trend chart
let line_trend_increase = document.getElementById("line_trend_increase");
let predictions = JSON.parse(line_trend_increase.getAttribute("data"));

let labels = predictions.map(summary => summary.date.split(' ')[0]);
let data = predictions.map(summary => summary.prediction.increase);
let line_chart_data = {
    labels: [""].concat(labels).slice(-15),
    datasets: [{
        data: [0].concat(data).slice(-15),
        label: "Increase",
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
        label: "Decrease",
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

let line_trend_bin = document.getElementById("line_trend_bin");

data = predictions.map(summary => (summary.prediction.increase > summary.prediction.decrease) ? 1 : 0);
line_chart_data = {
    labels: [""].concat(labels),
    datasets: [{
        data: [0].concat(data),
        label: "General",
        fill: true,
        backgroundColor: 'transparent',
        borderColor: palette.blue,
        borderWidth: 2,
        pointBackgroundColor: palette.blue,
    }]
}

let line_chart_bin = new Chart(line_trend_bin, {
    type: 'line',
    data: line_chart_data,
    options: {
        responsive: true,
        title: {
            fontSize: 20,
            display: true,
            text: "Trend of Prediction"
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
                    labelString: "general prediction"
                }
            }]
        }
    }
});

// Generate bar chart
let bar_chart = document.getElementById('bar_chart');
let bar_chart_labels = ["Prediction"];
let bar_chart_datasets = [{ data: [], backgroundColor: palette.blue, label: "Increase" }, { data: [], backgroundColor: palette.gray, label: "Decrease" }]

let trend = JSON.parse(bar_chart.getAttribute("data"));
console.log(trend)
let last_idx = trend.length - 1;
bar_chart_datasets[0].data.push(trend[last_idx].prediction.increase);
bar_chart_datasets[1].data.push(trend[last_idx].prediction.decrease);

console.log(bar_chart_datasets)
new Chart(bar_chart, {
    type: 'bar',
    data: {
        labels: bar_chart_labels,
        datasets: bar_chart_datasets
    },
    options: {
        responsive: false,
        maintainAspectRatio: true,
        title: {
            fontSize: 20,
            display: true,
            text: "Actual Prediction"
        },
        legend: {
            display: true,
            position: 'bottom'
        },
        scales: {
            xAxes: [{
                barPercentage: 0.4,
                categoryPercentage: 0.5
            }],
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                scaleLabel: {
                    fontSize: 20,
                    display: true,
                    labelString: "chances"
                }
            }]
        }
    }
});
