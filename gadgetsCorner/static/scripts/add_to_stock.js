let container = [];
const form = $('form');
const imei_1 = $('#id_device_imei');
const imei_2 = $('#id_device_imei_2');
const name = $('#id_name');
const cost_price = $('#id_cost_price');
const supplier = $('#id_supplier');
const waitRoom = $('#waiting-room');
const send = $('#submit');
const total = $('#total').text(container.length);

imei_2.on('change', (e) => {
  e.preventDefault();

  if (imei_1.val().length !== 15 || imei_2.val().length !== 15) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">IMEI numbers must be 15 digits long\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
    return;
  }

  if (imei_1.val() === imei_2.val()) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">IMEI numbers must be different\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
    return;
  }

  if (container.length === 30) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">Maximum number of items scanned\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
    return;
  }

  // Check if either IMEI already exists in the container
  const alreadyExists = container.some((item) => item.includes(imei_1.val()) || item.includes(imei_2.val()));

  if (!alreadyExists) {
    // Create a new item with the IMEI numbers and add it to the container
    const newItem = [imei_1.val(), imei_2.val()];
    container.push(newItem);
    total.text(container.length);
    form.trigger('reset');
    imei_1.focus();
    waitRoom.find('.list-group').append(
      `<li class="list-group-item text-success fw-bold">IMEI 1: ${newItem.join(' <===> IMEI 2: ')}</li>`,
    );
  } else {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">IMEI numbers already scanned or added in the list\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    form.trigger('reset');
    imei_1.focus();
  }
});

send.on('click', () => {
  if (container.length === 0) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">No Items Scanned!!! Please scan IMEI numbers\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    imei_1.focus();
    return;
  }

  if (name.val().length === 0 || cost_price.val().length === 0 || supplier.val().length === 0) {
    const note = '<div class="alert alert-warning alert-dismissible fade show" role="alert">Please enter the phone name, cost price and Suppllier\
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>';
    $(note).insertBefore(form);
    setTimeout(() => {
      $('.alert').alert('close');
    }, 5000);
    cost_price.focus();
    return;
  }

  const load = $('.loading-target');
  load.addClass('loading-message');

  $.ajax({
    url: '/system_core_1/add_to_stock/',
    type: 'POST',
    data: {
      data: JSON.stringify(container),
      name: name.val(),
      cost_price: cost_price.val(),
      supplier: supplier.val(),
    },
    success: (response) => {
      load.removeClass('loading-message');
      if (response.status === 200) {
        container = [];
        waitRoom.find('.list-group').empty();
        form.trigger('reset');
        imei_1.focus();
        if (response.data.length > 0) {
          response.data.forEach((item) => {
            waitRoom.find('.list-group').append(
              `<li class="list-group-item text-danger fw-bold">IMEI 1: ${item[0]} <===> IMEI 2: ${item[1]}</li>`,
            );
          });
        } else {
          const note = '<div class="alert alert-success alert-dismissible fade show" role="alert">Successfully added to stock\
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                        </div>';
          $(note).insertBefore(form);
          setTimeout(() => {
            $('.alert').alert('close');
          }, 5000);
        }
      } else {
        const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Failed to add to stock\
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                    </div>';
        $(note).insertBefore(form);
        setTimeout(() => {
          $('.alert').alert('close');
        }, 5000);
      }
    },
    error: (error) => {
      const note = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Failed to add to stock\
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                </div>';
      $(note).insertBefore(form);
      setTimeout(() => {
        $('.alert').alert('close');
      }, 5000);
    },
  });
});

$(document).ready(() => {
  // Listen for input in the first IMEI field
  $('#id_device_imei').on('input', function () {
    // If the input length is equal to 15 characters
    if ($(this).val().length === 15) {
      // Focus on the second IMEI field
      $('#id_device_imei_2').focus();
    }
  });
});
