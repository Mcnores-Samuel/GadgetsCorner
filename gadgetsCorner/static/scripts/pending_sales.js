const get_pending_sales = () => {
  $('document').ready(() => {
    const note = $('.pending-sales-notice');
    function getPendingSales() {
      $.ajax({
        url: '/system_core_1/total_pending_sales/',
        method: 'GET',
        contentTpe: 'application/json',
        success(data) {
          if (data) {
            note.text(`${data.total}`);
          }
        },
      });
    }
    getPendingSales();
    setInterval(getPendingSales, 5 * 60 * 1000);
  });
};

get_pending_sales();


const getUnverifiedStock = () => {
  $('document').ready(() => {
    const note = $('.unverified-stock-notice');
    function getUnverifiedStock() {
      $.ajax({
        url: '/system_core_1/verify_stock_recieved/',
        method: 'GET',
        contentTpe: 'application/json',
        success(data) {
          if (data) {
            note.text(`${data.total}`);
          }
        },
      });
    }
    getUnverifiedStock();
    setInterval(getUnverifiedStock, 5 * 60 * 1000);
  });
};

getUnverifiedStock();
