$(document).ready(function () {
  const loader = $('#loader');

  function fetchData() {
    $.ajax({
      url: '/gadgetsCorner/current_year_revenue/',
      method: 'GET',
      contentType: 'application/json',
      beforeSend() {
        loader.show();
      },
      success(data) {
        loader.hide();
        console.log(data);
        revParaBreakDown(data);
        costAndRevenueDist(data);
        fillTableValues(data);
      },
    });
  }
  fetchData();
});

function revParaBreakDown(data) {
  let salesAnalystChart = null;
  let yearlyAnalysisctx = null;

  if (salesAnalystChart === null) {
    yearlyAnalysisctx = $('.yearly_revenue_chart').get(0).getContext('2d');
  }

  const date = new Date();

  function fetchAndUpdateDailyData() {
    const modelList = [
      "Both Price & Cost",
      "Cost Only",
      "Price Only",
      "No Price or Cost",
    ];
    const values = [
      data.both_price_and_cost,
      data.cost_only,
      data.price_only,
      data.no_price_or_cost,
    ]

    if (salesAnalystChart === null) {
      salesAnalystChart = new Chart(yearlyAnalysisctx, {
        type: 'doughnut',
        data: {
          labels: modelList,
          datasets: [{
            label: date.toDateString(),
            data: values,
            backgroundColor: [
              "rgba(75, 192, 192, 0.8)",
              "rgba(255, 159, 64, 0.8)",
              "rgba(153, 102, 255, 0.8)",
              "rgba(201, 203, 207, 0.8)",
            ],
            borderWidth: 0.1,
          }
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            title: {
              display: true,
              text: `Breakdown of Items by Type`,
              color: '#333',
              align: 'center',
              font: {
                weight: 'bold',
                size: 12,
              },
              padding: 5,
            },
          },
        },
      });
    } else {
      salesAnalystChart.data.labels = modelList;
      salesAnalystChart.data.datasets[0].data = values;
      salesAnalystChart.update();
    }
  }
  fetchAndUpdateDailyData();
}

function costAndRevenueDist(data) {
  let revenueDistChart = null;
  let revenueDistCtx = null;

  if (revenueDistChart === null) {
    revenueDistCtx = $('.revenue_distribution_chart').get(0).getContext('2d');
  }

  if (revenueDistChart === null) {
    revenueDistChart = new Chart(revenueDistCtx, {
      type: 'bar',
      data: {
        labels: [
          "Both Price & Cost",
          "Cost Only",
          "Price Only",
          "No Price or Cost",
        ],
        datasets: [
          {
            label: 'Revenue',
            data: [data.revenue, data.revenue_for_itwco,
              data.revenue_for_itwpo, data.revenue_for_itwnps],
            backgroundColor: "rgba(75, 192, 192, 0.8)",
          },
          {
            label: 'Cost',
            data: [data.cost, data.cost_for_itwco,
              data.cost_for_itwpo, data.cost_for_itwnps],
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
            text: `Revenue and Cost Distribution`,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          }
        }
      },
    });
  }
}

function fillTableValues(data) {
  const both_price_and_cost = $('#both_price_and_cost');
  const cost_only = $('#cost_only');
  const price_only = $('#price_only');
  const no_price_or_cost = $('#no_price_or_cost');
  const revenue = $('#revenue');
  const revenue_for_itwco = $('#revenue_for_itwco');
  const revenue_for_itwpo = $('#revenue_for_itwpo');
  const revenue_for_itwnps = $('#revenue_for_itwnps');
  const cost = $('#cost');
  const cost_for_itwco = $('#cost_for_itwco');
  const cost_for_itwpo = $('#cost_for_itwpo');
  const cost_for_itwnps = $('#cost_for_itwnps');
  const year = $('#year');
  const total = $('#total');
  const revenueId = $('#revenueId');
  const costId = $('#costId');

  const formatValue = (value) => {
    if (value === null) {
      return '0';
    }
    return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  both_price_and_cost.html(data.both_price_and_cost);
  cost_only.html(data.cost_only);
  price_only.html(data.price_only);
  no_price_or_cost.html(data.no_price_or_cost);
  revenue.html(`MK ${formatValue(data.revenue)}`);
  revenue_for_itwco.html(`MK ${formatValue(data.revenue_for_itwco)}`);
  revenue_for_itwpo.html(`MK ${formatValue(data.revenue_for_itwpo)}`);
  revenue_for_itwnps.html(`MK ${formatValue(data.revenue_for_itwnps)}`);
  cost.html(`MK ${formatValue(data.cost)}`);
  cost_for_itwco.html(`MK ${formatValue(data.cost_for_itwco)}`);
  cost_for_itwpo.html(`MK ${formatValue(data.cost_for_itwpo)}`);
  cost_for_itwnps.html(`MK ${formatValue(data.cost_for_itwnps)}`);
  year.html(data.year);
  total.html(data.total_calculated);
  revenueId.html(`MK${formatValue(data.revenue)}`);
  costId.html(`MK${formatValue(data.cost)}`);
}