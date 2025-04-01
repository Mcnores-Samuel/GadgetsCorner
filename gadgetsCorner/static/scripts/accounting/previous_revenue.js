$(document).ready(function () {
    const loader = $('#loader');
    
    function fetchData() {
        $.ajax({
        url: '/gadgetsCorner/lastyearBycurrentMonth/',
        method: 'GET',
        contentType: 'application/json',
        beforeSend() {
            loader.show();
        },
        success(data) {
            loader.hide();
            console.log(data);
            lastYearByCurrentMonth(data);
        },
        });
    }
    fetchData();
});

function lastYearByCurrentMonth(data) {
    let salesAnalystChart = null;
    let yearlyAnalysisctx = null;

    if (salesAnalystChart === null) {
        yearlyAnalysisctx = $('.last_revenue_chart').get(0).getContext('2d');
    }

    const date = new Date();

    const modelist = [];
    const values = [];

    $.each(data, function (key, value) {
        modelist.push(key);
        values.push(value);
    });

    salesAnalystChart = new Chart(yearlyAnalysisctx, {
        type: 'line',
        data: {
            labels: modelist,
            datasets: [{
                label: 'Revenue',
                data: values,
                backgroundColor: "rgba(75, 192, 192, 0.8)",
                fill: true,
                tension: 0.4,
                yAxisID: 'y',
                order: 1,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    display: false,
                    drawBorder: false,
                },
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false,
                },
            },
        },
    });
}
