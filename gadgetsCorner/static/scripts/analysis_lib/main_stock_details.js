let mainStockChart = null;
let mainStockctx = null;

function mainStockChartDetails() {
  if (mainStockChart === null) {
    mainStockctx = $('.main_stock_detailed_analysis').get(0).getContext('2d');
  }

  const date = new Date();
  const chartType = 'bar';

  function fetchAndUpdateDailyData() {
    let modelList = [];
    let total = [];

    $.ajax({
      url: '/system_core_1/get_source_stock/',
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

        if (mainStockChart === null) {
          mainStockChart = new Chart(mainStockctx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: `${date.toLocaleDateString()} Stock Levels`,
                data: total,
                backgroundColor: '#2980B9', // Blue color
                borderColor: '#2980B9', // Blue color
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
                  text: 'Daily Stock Analysis',
                  color: '#34495E', // Darker blue color
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 16, // Font size
                  },
                  padding: 10, // Adjust padding for spacing
                  fullSize: true,
                },
              },
              scales: {
                x: {
                  grid: {
                    color: '#ECF0F1', // Light gray grid lines
                    lineWidth: 0.5, // Adjust grid line thickness
                    drawBorder: true, // Display chart border
                  },
                  ticks: {
                    color: '#34495E', // Darker blue color
                    font: {
                      weight: 'normal', // Regular font weight
                    },
                  },
                },
                y: {
                  grid: {
                    color: '#ECF0F1', // Light gray grid lines
                    lineWidth: 0.5, // Adjust grid line thickness
                    drawBorder: true, // Display chart border
                  },
                  ticks: {
                    color: '#34495E', // Darker blue color
                    font: {
                      weight: 'normal', // Regular font weight
                    },
                  },
                },
              },
            },
          });
        } else {
          mainStockChart.data.labels = modelList;
          mainStockChart.data.datasets[0].data = total;
          mainStockChart.data.datasets[0].label = `${date.toLocaleDateString()} Stock Levels`;
          mainStockChart.update();
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
mainStockChartDetails();

