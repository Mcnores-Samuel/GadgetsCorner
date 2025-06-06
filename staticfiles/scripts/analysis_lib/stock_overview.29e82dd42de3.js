/**
 * agentsStockChartDetails - function to fetch data from the server and render the chart
 * @param {*} url - url to fetch data from
 * @param {*} dest - destination to render the chart
 * @param {*} chartType - type of chart to render
 * @param {*} loader - loader to show when fetching data
 */
function agentsStockChartDetails(url, dest, chartType, loader) {
  let allAgentsStocks = null;
  let allAgentCtx = null;
  const date = new Date();

  if (allAgentsStocks === null) {
    allAgentCtx = $(dest).get(0).getContext('2d');
  }

  function fetchAndUpdateDailyData() {
    const modelList = [];
    const total = [];
    const colors = [];
    let overallTotal = 0;
    let targetCapacity = 0; // Variable to store target capacity
    let filledPercentage = 0; // Variable to store the percentage of stock filled

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
          if (model !== 'Total') {
            modelList.push(model);
            total.push(value);
          }
          if (model === 'Target Capacity') {
            targetCapacity = value; // Get the target capacity from the response
          }
          overallTotal === 0 ? overallTotal = data.Total : overallTotal;
        });

        filledPercentage = (overallTotal / targetCapacity) * 100; // Calculate filled percentage

        for (let i = 0; i < modelList.length; i++) {
          const num1 = Math.round(Math.random() * 255 + 1);
          const num2 = Math.round(Math.random() * 255 + 1);
          const num3 = Math.round(Math.random() * 255 + 1);
          colors.push(`rgb(${num1}, ${num2}, ${num3})`);
        }

        if (allAgentsStocks === null) {
          allAgentsStocks = new Chart(allAgentCtx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: `Total ${overallTotal}`,
                data: total,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              animation: {
                animateScale: true,
                animateRotate: true,
              },
              events: ['mousemove'],
              interaction: {
                mode: 'nearest',
              },
              plugins: {
                title: {
                  display: true,
                  text: `Total overall stock ${overallTotal}`,
                  color: '#fe9a43',
                  position: 'bottom',
                  align: 'left',
                  font: {
                    weight: 'bold',
                    size: 10,
                  },
                  padding: 10,
                  fullSize: true,
                },
                legend: {
                  display: false,
                  position: 'top',
                  align: 'center',
                  labels: {
                    color: '#fe9a43',
                    font: {
                      size: 10,
                      weight: 'bold',
                    },
                  },
                },
              },
              annotation: { // Add annotation to show the target capacity
                annotations: [{
                  type: 'line',
                  mode: 'horizontal',
                  scaleID: 'y',
                  value: targetCapacity,
                  borderColor: 'rgba(255,0,0,0.5)',
                  borderWidth: 2,
                  label: {
                    enabled: true,
                    content: 'Target Capacity',
                  },
                }],
              },
            },
          });
        } else {
          allAgentsStocks.data.labels = labelsList;
          allAgentsStocks.data.datasets[0].data = total;
          allAgentsStocks.update();
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

const url_main_stock = '/gadgetsCorner/get_main_stock_analysis';
const dest_main_stock = '.main_stock_overview_chart';
const loader_main_stock = '.main_stock_chart_loader';
const chartType_main_stock = 'doughnut';

agentsStockChartDetails(
  url_main_stock, dest_main_stock,
  chartType_main_stock, loader_main_stock,
);
