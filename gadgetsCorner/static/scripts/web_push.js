$(document).ready(() => {
  const allowWebBtn = $('#webpush-subscribe-button');
  const modal = $('#web_push_request');

  // Check if the user has already subscribed
  const isSubscribed = localStorage.getItem('webpush-subscribed');

  if (!isSubscribed) {
    // Show the modal if the user hasn't subscribed
    setTimeout(() => {
      if (allowWebBtn.text().includes('Subscribe')) {
        modal.modal('show');
      }
    }, 10000);
  }

  allowWebBtn.on('click', () => {
    // Hide the modal when the user subscribes
    $('#web_push_request').modal('hide');
    // Set the subscription status in local storage
    localStorage.setItem('webpush-subscribed', 'true');
  });

  setTimeout(() => {
    if (allowWebBtn.text().includes('Subscribe')) {
      modal.modal('show');
    } else {
      modal.modal('hide');
    }
  }, 5000);
});
