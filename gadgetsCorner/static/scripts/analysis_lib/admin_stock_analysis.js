/**
 * @name adminStockAnalysis - Function to update the stock analysis of the admin dashboard
 * @param {None} - None
 */
function adminStockAnalysis() {
  const estimated_revenue = $('#estimated_revenue_analysis');
  const estimated_profit = $('#estimated_profit_analysis');
  const mainShopSales = $('#main_shop_sales_analysis');
  const progress = $('.progress-bar');
  const target = $('.text-end');

  function formatRevenue(value) {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
      return (value / 1000).toFixed(1) + 'K';
    } else {
      return value.toFixed(2);
    }
  }

  function updateStockAnalysis() {
    $.ajax({
      url: '/gadgetsCorner/admin_stock_analysis',
      type: 'GET',
      dataType: 'json',
      beforeSend() {
        estimated_revenue.html('Loading...');
        estimated_profit.html('Loading...');
        mainShopSales.html('Loading...');
        target.html('Loading...');
        progress.css('width', '100%');
        progress.html('0%');
      },
      success(data) {
        console.log(data);
        estimated_revenue.html(`${formatRevenue(data.estimated_revenue)}`);
        estimated_profit.html(`${formatRevenue(data.estimated_profit)}`);
        mainShopSales.html(`${formatRevenue(data.main_shop_sales)}`);
        target.html(`${formatRevenue(data.target)}`);
        progress.css('width', `${data.progress}%`);
        progress.html(`${data.progress}%`);
      },
    });
  }

  setTimeout(updateStockAnalysis, 3000);
}

adminStockAnalysis();
