/**
 * Yearly Sales Analysis - Fetches data from the server and renders a chart
 * @param {*} url - The url to fetch data from
 * @param {*} dest - The destination to render the chart
 * @param {*} chartType - The type of chart to render
 * @param {*} loader - The loader to show when fetching data
 */
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
                  text: `Yearly Sales Analysis: Total Sales: ${total.reduce((a, b) => a + b, 0)}`,
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

/**
 *
 * @param {*} url - The url to fetch data from
 * @param {*} dest - The destination to render the chart
 * @param {*} chartType - The type of chart to render
 * @param {*} loader - The loader to show when fetching data
 */
function yearlySalesAnalysisProduct(url, dest, chartType, loader) {
  let salesAnalystChartPro = null;
  let yearlyAnalysisctxPro = null;

  if (salesAnalystChartPro === null) {
    yearlyAnalysisctxPro = $(dest).get(0).getContext('2d');
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

        for (let i = 0; i < data.length; i++) {
          if (data[i][1] > 10 || data[i][1] === 10) {
            modelList.push(data[i][0]);
            total.push(data[i][1]);
          }
        }

        if (salesAnalystChartPro === null) {
          salesAnalystChartPro = new Chart(yearlyAnalysisctxPro, {
            type: chartType,
            data: {
              labels: modelList,
              datasets: [{
                label: date.toDateString(),
                data: total,
                backgroundColor: '#4285F4',
                borderColor: '#4285F4',
                borderWidth: 2,
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
                  text: 'Yearly Sales Analysis by Product',
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
                  },
                },
              },
            },
          });
        } else {
          salesAnalystChartPro.data.labels = modelList;
          salesAnalystChartPro.data.datasets[0].data = total;
          salesAnalystChartPro.update();
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

const urlYearly = '/system_core_1/get_yearly_sales/';
const destYearly = '.yearly_sales_chart';
const chartTypeYearly = 'bar';
const loaderYearly = '.yearly_sales_chart_loader';

const productAnalysis = '/system_core_1/get_yearly_product_sales/';
const productDest = '.yearly_product_sales_chart';
const productLoader = '.yearly_product_sales_chart_loader';
const chartTypeProduct = 'bar';

const urlYearlyOther = '/system_core_1/get_yearly_sales_total/';
const destYearlyOther = '.yearly_sales_chart_total';
const chartTypeYearlyOther = 'bar';
const loaderYearlyOther = '.yearly_sales_chart_loader_total';

yearlySalesAnalysis(
  urlYearly, destYearly,
  chartTypeYearly, loaderYearly,
);

yearlySalesAnalysis(
  urlYearlyOther, destYearlyOther,
  chartTypeYearlyOther, loaderYearlyOther,
);
yearlySalesAnalysisProduct(
  productAnalysis, productDest,
  chartTypeProduct, productLoader,
);
