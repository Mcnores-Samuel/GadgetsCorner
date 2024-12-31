function updateCreditPrice() {
  $.ajax({
    url: '/system_core_1/updateCreditPrices/',
    method: 'GET',
    contentType: 'application/json',
    success(data) {
      if (data) {
        const note = $('.credit-price-notice');
        note.text(`${data.price}`);
      }
    },
  });
}
updateCreditPrice();
