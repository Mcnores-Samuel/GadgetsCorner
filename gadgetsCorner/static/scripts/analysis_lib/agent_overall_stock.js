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
                  color: 'navy',
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                  },
                  padding: 8,
                  fullSize: true,
                },
                legend: {
                  display: true,
                  position: 'right',
                  align: 'center',
                  labels: {
                    color: 'black',
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

const url_agents_stock = '/system_core_1/get_agents_stock_json/';
const dest_all_stock = '.all_agents_stock_chart';
const chartType = 'doughnut';
const loader_all_stock = '.loading-message-stock';

const url_main_stock = '/system_core_1/get_main_stock_analysis/';
const dest_main_stock = '.main_stock_chart';
const loader_main_stock = '.loading-message-shop';
const chartType_main_stock = 'doughnut';

agentsStockChartDetails(
  url_agents_stock, dest_all_stock,
  chartType, loader_all_stock,
);

agentsStockChartDetails(
  url_main_stock, dest_main_stock,
  chartType_main_stock, loader_main_stock,
);
