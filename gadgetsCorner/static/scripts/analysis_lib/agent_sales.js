let agent_sales_stockChart = null;
let agent_sales_stockctx = null;

function agent_stock_chart_sales() {
  if (agent_sales_stockChart === null) {
    agent_sales_stockctx = $('.salesChart').get(0).getContext('2d');
  }

  const date = new Date();
  const chartType = 'bar';

  function fetchAndUpdateDailyData() {
    let modelList = [];
    let total = [];

    $.ajax({
      url: '/system_core_1/get_individual_agent_stock_out/',
      method: 'GET',
      contentType: 'application/json',
      beforeSend() {
        const load = $('.loading-message-main-stock');
        load.addClass('loading-message');
      },
      success(data) {
        const load = $('.loading-message-main-stock');
        load.removeClass('loading-message');

        modelList = data.map((item) => item[0]);
        total = data.map((item) => item[1]);

        if (agent_sales_stockChart === null) {
          agent_sales_stockChart = new Chart(agent_sales_stockctx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: date.toDateString(),
                data: total,
                backgroundColor: ['#23435c'],
                borderColor: ['#23435c'],
                borderWidth: 2,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              events: ['mousemove'],
              interaction: {
                mode: 'nearest',
              },
              plugins: {
                title: {
                  display: true,
                  text: 'Sales Analysis',
                  color: 'navy',
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                  },
                  padding: 8,
                  fullSize: true,
                },
              },
              indexAxis: 'y',
              barPercentage: 0.7,
              categoryPercentage: 0.7,
              scales: {
                x: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: 'navy',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
                y: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: 'navy',
                    font: {
                      weight: 'bold',
                    },
                  },
                },
              },
            },
          });
        } else {
          agent_sales_stockChart.data.labels = labelsList;
          agent_sales_stockChart.data.datasets[0].data = total;
          agent_sales_stockChart.update();
        }
        setTimeout(fetchAndUpdateDailyData, 5 * 60 * 1000);
      },
      error(err) {
        console.error(err);
      },
    });
  }
  fetchAndUpdateDailyData();
}
agent_stock_chart_sales();
