const get_pending_sales = () => {
  $('document').ready(() => {
    const note = $('.pending-sales-notice');
    function getPendingSales() {
      $.ajax({
        url: '/gadgetsCorner/total_pending_sales/',
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
