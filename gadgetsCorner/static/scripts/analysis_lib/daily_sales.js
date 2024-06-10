function updateDailyChart(url, dest, chartType, loader) {
  let dailySalesChart = null;
  let dailyCtx = null;

  if (dailySalesChart === null) {
    dailyCtx = $(dest).get(0).getContext('2d');
  }

  const date = new Date();

  function fetchAndUpdateDailyData() {
    const modelList = [];
    const total = [];
    let overallTotal = 0;

    $.ajax({
      url,
      method: 'GET',
      contentType: 'application/json',
      beforeSend() {
        const load = $(loader);
        load.addClass('loading-message');
      },
      success(data) {
        const load = $(loader);
        load.removeClass('loading-message');

        $.each(data, (model, value) => {
          modelList.push(model);
          total.push(value);
          overallTotal += value;
        });

        if (dailySalesChart === null) {
          dailySalesChart = new Chart(dailyCtx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: `${date.toDateString()} Total ${overallTotal}`,
                data: total,
                backgroundColor: '#2980B9', // Blue color
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false, // Allows for better chart scaling
              events: ['mousemove'],
              interaction: {
                mode: 'nearest',
              },
              plugins: {
                title: {
                  display: true,
                  text: `Daily Sales: ${overallTotal}`,
                  color: '#fe9a43', // Darker blue color
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 16, // Adjust font size
                  },
                  padding: 10, // Adjust padding for spacing
                  fullSize: true,
                },
              },
              scales: {
                x: {
                  grid: {
                    display: false, // Hide grid lines
                  },
                  ticks: {
                    color: '#fe9a43', // Darker blue color
                    font: {
                      weight: 'bold', // Regular font weight
                    },
                  },
                },
                y: {
                  grid: {
                    display: false, // Hide grid lines
                  },
                  ticks: {
                    color: '#fe9a43', // Darker blue color
                    font: {
                      weight: 'bold', // Regular font weight
                    },
                  },
                },
              },
            },
          });
        } else {
          dailySalesChart.data.labels = modelList;
          dailySalesChart.data.datasets[0].data = total;
          dailySalesChart.update();
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

const dest_daily = '.daily_sales_chart_loan';
const url_daily = '/gadgetsCorner/get_daily_sales_json_loan/';
const loader_daily = '.daily_sales_loader_loan';

const dest_daily_2 = '.daily_sales_chart_cash';
const url_daily_2 = '/gadgetsCorner/get_daily_sales_json_cash/';
const loader_daily_2 = '.daily_sales_loader_cash';

updateDailyChart(url_daily, dest_daily, 'bar', loader_daily);
updateDailyChart(url_daily_2, dest_daily_2, 'bar', loader_daily_2);
