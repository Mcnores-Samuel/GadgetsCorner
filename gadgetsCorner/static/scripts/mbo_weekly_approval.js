/**
 * updateWeeklyChart - Fetches data from the server and renders a chart on the canvas element
 * @param {string} url - The url to fetch the data from
 * @param {string} dest - The canvas element to render the chart
 * @param {string} chartType - The type of chart to render
 * @param {string} loader - The loader element to show when fetching data
 */
function updateWeeklyChart(url, dest, chartType = 'line', loader) {
  let weeklySalesChart = null;
  let weeklyCtx = null;

  if (weeklySalesChart === null) {
    weeklyCtx = $(dest).get(0).getContext('2d');
  }

  const labelsList = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  function fetchAndUpdateWeeklyData() {
    const nums = [];
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

        Object.keys(data).forEach((day) => {
          const salesData = data[day];
          const total = salesData.length;
          nums.push(total);
          overallTotal += total;
        });

        if (weeklySalesChart === null) {
          weeklySalesChart = new Chart(weeklyCtx, {
            type: chartType,
            data: {
              labels: labelsList,
              datasets: [{
                data: nums,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
              }],
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                title: {
                  display: true,
                  text: `Weekly Sales Analysis: total sales: ${overallTotal}`,
                  position: 'bottom',
                  color: '#333',
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
          weeklySalesChart.data.labels = labelsList;
          weeklySalesChart.data.datasets[0].data = nums;
          weeklySalesChart.update();
        }
        setTimeout(fetchAndUpdateWeeklyData, 5 * 60 * 1000);
      },
      error(err) {
        console.error(err);
      },
    });
  }
  fetchAndUpdateWeeklyData();
}

const dest_3 = '.Weekly_approved_contracts_chart';
const url_3 = '/system_core_1/weekly_approved_contracts/';
const loader_3 = '.weekly_approved_contracts_loader';

updateWeeklyChart(url_3, dest_3, 'bar', loader_3);
