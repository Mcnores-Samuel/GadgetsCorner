/**
 * @name adminStockAnalysis - Function to update the stock analysis of the admin dashboard
 * @param {None} - None
 */
function adminStockAnalysis() {
  const estimated_revenue = $('#estimated_revenue_analysis');
  const estimated_profit = $('#estimated_profit_analysis');
  const daily_expenses = $('#daily_expenses_analysis');
  const loss = $('#loss_analysis');
  const estimated_loss = $('#estimated_loss_analysis');
  const progress = $('.progress-bar');
  const target = $('.text-end');

  function formatRevenue(value) {
    if (value >= 1000000) {
      return (value / 1000000).toFixed(3) + 'M';
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
        estimated_revenue.html('<div class="spinner-border spinner-border-sm" role="status">\
          <span class="visually-hidden">Loading...</span></div>');
        estimated_profit.html('<div class="spinner-border spinner-border-sm" role="status">\
          <span class="visually-hidden">Loading...</span></div>');
        target.html('<div class="spinner-border spinner-border-sm" role="status">\
          <span class="visually-hidden">Loading...</span></div>');
        daily_expenses.html('<div class="spinner-border spinner-border-sm" role="status">\
          <span class="visually-hidden">Loading...</span></div>');
        loss.html('<div class="spinner-border spinner-border-sm" role="status">\
          <span class="visually-hidden">Loading...</span></div>');
        estimated_loss.html('<div class="spinner-border spinner-border-sm" role="status">\
          <span class="visually-hidden">Loading...</span></div>');
        progress.css('width', '100%');
        progress.html('0%');
      },
      success(data) {
        estimated_revenue.html(`${formatRevenue(data.estimated_revenue)}`);
        estimated_profit.html(`${formatRevenue(data.estimated_profit)} <span class="material-icons text-success" style="font-size: 12px">arrow_upward</span>`);
        daily_expenses.html(`${formatRevenue(data.expenses)}`);
        loss.html(`- ${formatRevenue(data.estimated_loss)} <span class="material-icons text-danger" style="font-size: 12px">arrow_downward</span>`);
        estimated_loss.html(`- ${formatRevenue(data.estimated_loss)} <span class="material-icons text-danger" style="font-size: 12px">arrow_downward</span>`);
        target.html(`${formatRevenue(data.target)}`);
        progress.css('width', `${data.progress}%`);
        progress.html(`${data.progress}%`);
      },
    });
  }

  setTimeout(updateStockAnalysis, 3000);
}

adminStockAnalysis();
