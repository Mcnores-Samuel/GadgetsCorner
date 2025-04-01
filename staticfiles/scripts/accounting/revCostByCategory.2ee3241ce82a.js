$(document).ready(function () {
    const loader = $('#loader');

    const fetchData = () => {
        $.ajax({
            url: '/gadgetsCorner/revenue_by_category/',
            method: 'GET',
            contentType: 'application/json',
            beforeSend() {
                $('#loader').show();
            },
            success(data) {
                $('#loader').hide();
                console.log(data);
                revCostByCategory(data);
            },
        });
    }

    fetchData();
});

function revCostByCategory(data) {
    let revCostByCategoryChart = null;
    let revCostByCategoryctx = null;

    if (revCostByCategoryChart === null) {
        revCostByCategoryctx = $('.revCostByCategoryChart').get(0).getContext('2d');
    }

    function fetchAndUpdateDailyData() {
        const modelList = [];
        const revenue = [];
        const cost = [];

        data.forEach((item) => {
            modelList.push(item.category);
            revenue.push(item.total_revenue);
            cost.push(item.total_cost);
        });

        revCostByCategoryChart = new Chart(revCostByCategoryctx, {
            type: 'bar',
            data: {
                labels: modelList,
                datasets: [
                    {
                        label: 'Revenue',
                        data: revenue,
                        backgroundColor: "rgba(75, 192, 192, 0.8)",
                    },
                    {
                        label: 'Cost',
                        data: cost,
                        backgroundColor: "rgba(255, 159, 64, 0.8)",
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Revenue and Cost by Category',
                    },
                },
            },
        });
    }

    fetchAndUpdateDailyData();
}