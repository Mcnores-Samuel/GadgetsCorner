const months = [
  'January', 'February',
  'March', 'April', 'May',
  'June', 'July', 'August',
  'September', 'October',
  'November', 'December',
];

function updateSalesByAgentChart(url, dest, chartType, loader) {
  let salesByAgentChart = null;
  let salesByAgentCtx = null;

  if (salesByAgentChart === null) {
    salesByAgentCtx = $(dest).get(0).getContext('2d');
  }
  const date = new Date();

  function fetchAndUpdateAgentMonthly() {
    let labelsList = [];
    let nums = [];

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

        const total = data.Total;
        $.each(data, (date, value) => {
          if (date !== 'Total') {
            labelsList.push(date);
            nums.push(value);
          }
        });

        if (salesByAgentChart === null) {
          salesByAgentChart = new Chart(salesByAgentCtx, {
            type: chartType, // Assuming chartType is still 'bar'
            data: {
              labels: labelsList,
              datasets: [{
                data: nums,
                backgroundColor: '#2980B9', // Blue color
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
                  text: `${months[date.getMonth()]} Sales Analysis: total ${total}`,
                  color: '#fe9a43', // Darker blue color
                  position: 'bottom',
                  align: 'center',
                  font: {
                    weight: 'bold',
                    size: 10, // Adjust font size
                  },
                  padding: 10, // Adjust padding for spacing
                  fullSize: true,
                },
                legend: {
                  display: false,
                },
              },
              indexAxis: 'x', // Explicitly set y-axis as the index axis
              barPercentage: 0.7, // Adjust bar width
              categoryPercentage: 0.7, // Adjust spacing between bars
              scales: {
                x: {
                  grid: {
                    display: false, // Hide grid lines
                  },

                  ticks: {
                    beginAtZero: true, // Start axis at 0
                    stepSize: 1, // Show values for each agent
                    color: '#fe9a43', // Darker blue color
                    font: {
                      weight: 'normal', // Regular font weight
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
                      weight: 'normal', // Regular font weight
                    },
                  },
                },
              },
            },
          });
        } else {
          salesByAgentChart.data.labels = labelsList;
          salesByAgentChart.data.datasets[0].data = nums;
          salesByAgentChart.data.datasets[0].label = `${months[date.getMonth()]} Total Loan Sales: ${total}`;
          salesByAgentChart.update();
        }
        setTimeout(fetchAndUpdateAgentMonthly, 5 * 60 * 1000);
      },
      error(err) {
        console.error(err);
      },
    });
  }
  fetchAndUpdateAgentMonthly();
}

const dest_monthly = '.monthly_sales_chart';
const url_monthly = '/gadgetsCorner/get_monthly_sales/';
const loader_monthly = '.monthly_sales_loader';

updateSalesByAgentChart(url_monthly, dest_monthly, 'bar', loader_monthly);
