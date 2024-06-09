/**
 * @name adminStockAnalysis - Function to update the stock analysis of the admin dashboard
 * @param {None} - None
 */
function adminStockAnalysis() {
  const overallStock = $('#overall_stock_analysis');
  const overallSales = $('#overall_sales_analysis');
  const mainShopSales = $('#main_shop_sales_analysis');
  const progress = $('.progress-bar');
  const target = $('.text-end');

  function updateStockAnalysis() {
    $.ajax({
      url: '/system_core_1/admin_stock_analysis',
      type: 'GET',
      dataType: 'json',
      beforeSend() {
        overallStock.html('Loading...');
        overallSales.html('Loading...');
        mainShopSales.html('Loading...');
        target.html('Loading...');
        progress.css('width', '100%');
        progress.html('0%');
      },
      success(data) {
        overallStock.html(`${data.overall_stock} Devices`);
        overallSales.html(`${data.overall_sales} Devices`);
        mainShopSales.html(`${data.sales} Devices`);
        target.html(`${data.target} Devices`);
        if (data.progress < 50) {
          progress.css('background-color', 'red');
        }
        if (data.progress >= 50 && data.progress < 75) {
          progress.css('background-color', 'blue');
        }
        if (data.progress >= 75) {
          progress.css('background-color', 'purple');
        }
        progress.css('width', `${data.progress}%`);
        progress.html(`${data.progress}%`);
      },
    });
  }
  setTimeout(updateStockAnalysis, 3000);
}
adminStockAnalysis();
