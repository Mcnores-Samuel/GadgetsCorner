let container = [];
const scannedItem = $('#data');
const form = $('form');
const waitingRoom = $('#waiting-room ul');
const date = $('#date');
const sales_type = $('#sales_type');
const deploy = $('#deploy');
const total = $('#total');
const csrf = $('#token');
total.text(container.length);

function deployData() {
  form.on('submit', (e) => {
    e.preventDefault();
    if (scannedItem.val() === '') {
      return;
    }
    if (!container.includes(scannedItem.val())) {
      container.push(scannedItem.val());
      total.text(container.length);
      scannedItem.val('');
      waitingRoom.html(`<li class="list-group-item">${container.join('</li><li class="list-group-item">')}</li>`);
    } else {
      const note = `<div class="alert alert-danger alert-dismissible fade show" role="alert">Item ${scannedItem.val()} already scanned\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>`;
      $(note).insertBefore(scannedItem);
      setInterval(() => {
        $('.alert').alert('close');
      }, 5000);
    }
    scannedItem.val('');
  });

  deploy.on('click', () => {
    if (date.val() === '' || sales_type.val() === '') {
      const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Please select date and sales_type\
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
      $(note).insertBefore(form);
      setInterval(() => {
        $('.alert').alert('close');
      }, 5000);
      return;
    }
    if (container.length === 0) {
      const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">No items to deploy\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
      $(note).insertBefore(form);
      setInterval(() => {
        $('.alert').alert('close');
      }, 5000);
      return;
    }
    $.ajax({
      url: '/system_core_1/uploadBulkSales/',
      type: 'POST',
      data: {
        csrfmiddlewaretoken: csrf.val(),
        data: JSON.stringify(container),
        date: JSON.stringify(date.val()),
        sales_type: JSON.stringify(sales_type.val()),
      },
      beforeSend() {
        const load = $('.loading');
        load.addClass('loading-message');
      },
      success(response) {
        if (response.status === 200) {
          container = [];
          waitingRoom.html('');
          date.val('');
          sales_type.val('');
          total.text(container.length);
          if (response.not_in_stock.length > 0) {
            waitingRoom.html(`<li class="list-group-item bg-danger">${response.not_in_stock.join('</li><li class="list-group-item bg-danger">')}</li>`);
            total.text(response.not_in_stock.length);
            const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">The following items are not in stock\
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>';
            $(note).insertBefore(form);
            setInterval(() => {
              $('.alert').alert('close');
            }, 5000);
          } else {
            const note = '<div class="alert alert-success alert-dismissible fade show" role="alert">Items deployed successfully\
              <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
              </div>';
            $(note).insertBefore(form);
            setInterval(() => {
              $('.alert').alert('close');
            }, 5000);
          }
        } else {
          const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Error deploying items\
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>';
          $(note).insertBefore(form);
          setInterval(() => {
            $('.alert').alert('close');
          }, 5000);
        }
      },
      error() {
        const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Error deploying items\
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
            </div>';
        $(note).insertBefore(form);
        setInterval(() => {
          $('.alert').alert('close');
        }, 5000);
      },
    });
  });
}
deployData();
