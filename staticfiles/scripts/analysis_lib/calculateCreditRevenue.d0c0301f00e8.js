function yearlySalesAnalysis(url, dest, chartType, loader) {
  let salesAnalystChart = null;
  let yearlyAnalysisctx = null;

  if (salesAnalystChart === null) {
    yearlyAnalysisctx = $(dest).get(0).getContext('2d');
  }

  const date = new Date();

  function fetchAndUpdateDailyData() {
    const modelList = [];
    const total = [];

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

        $.each(data, (key, value) => {
          modelList.push(key);
          total.push(value);
        });

        if (salesAnalystChart === null) {
          salesAnalystChart = new Chart(yearlyAnalysisctx, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: date.toDateString(),
                data: total,
                backgroundColor: '#4285F4',
                borderColor: '#4285F4',
                borderWidth: 0.1,
              },
              {
                label: 'Total Sales',
                data: total,
                backgroundColor: '#0F9D58',
                borderColor: '#0F9D58',
                borderWidth: 2,
                type: 'line',
                fill: false,
                yAxisID: 'y',
                order: 1,
                tension: 0.4,
                pointRadius: 5,
                pointHoverRadius: 7,
                pointBackgroundColor: '#0F9D58',
                pointBorderColor: '#0F9D58',
                pointHoverBackgroundColor: '#0F9D58',
                pointHoverBorderColor: '#0F9D58',
                pointBorderWidth: 2,
                pointHoverBorderWidth: 3,
                hitRadius: 10,
                hoverRadius: 10,
                hoverBorderWidth: 3,
                hoverBackgroundColor: '#0F9D58',
                hoverBorderColor: '#0F9D58',
              },
              ],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                title: {
                  display: true,
                  text: `Yearly Sales Analysis: Total Sales:`,
                  color: '#333',
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 16,
                  },
                  padding: 20,
                },
                legend: {
                  display: false,
                },
              },
              scales: {
                x: {
                  grid: {
                    display: false,
                    drawBorder: false,
                  },
                  ticks: {
                    color: '#333',
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
                    color: '#333',
                    font: {
                      weight: 'bold',
                    },
                    // Format tick labels
                    callback(value, index, values) {
                      if (value >= 1000000) {
                        return `${(value / 1000000).toFixed(1)}M`;
                      } if (value >= 1000) {
                        return `${(value / 1000).toFixed(1)}K`;
                      }
                      return value;
                    },
                  },
                },
              },
            },
          });
        } else {
          salesAnalystChart.data.labels = modelList;
          salesAnalystChart.data.datasets[0].data = total;
          salesAnalystChart.update();
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

const urlyearlyRevenue = '/system_core_1/calculateCreditRevenue/';
const destYearlyRevenue = '.yearly_revenue_chart';
const chartTypeYearlyRevenue = 'bar';
const loaderYearlyRevenue = '.yearly_revenue_chart_loader';

yearlySalesAnalysis(
  urlyearlyRevenue, destYearlyRevenue,
  chartTypeYearlyRevenue, loaderYearlyRevenue,
);
