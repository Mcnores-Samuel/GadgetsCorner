const mboPending = () => {
  $('document').ready(() => {
    const note = $('.pending-sales-notice');
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

mboPending();

const mboApproved = () => {
  $('document').ready(() => {
    const note = $('.unverified-stock-notice');
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
}

mboApproved();


const mboRejected = () => {
  $('document').ready(() => {
    const note = $('.rejected-sales-notice');
    function getRejectedSales() {
      $.ajax({
        url: '/system_core_1/total_rejected_sales/',
        method: 'GET',
        contentTpe: 'application/json',
        success(data) {
          if (data) {
            note.text(`${data.total}`);
          }
        },
      });
    }
    getRejectedSales();
    setInterval(getRejectedSales, 5 * 60 * 1000);
  });
}

mboRejected();