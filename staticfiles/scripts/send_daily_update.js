// Define the update function
function sendSalesUpdate() {
  let currentTime = new Date();
  let hours = currentTime.getHours();
  let minutes = currentTime.getMinutes();

  // Define the update times
  const updateTimes = [
    { hour: 6, minute: 0, endpoint: '/gadgetsCorner/system_routine_update' },
    { hour: 12, minute: 0, endpoint: '/gadgetsCorner/system_routine_update' },
    { hour: 18, minute: 0, endpoint: '/gadgetsCorner/system_routine_update' },
  ];

  // Check if the current time matches any update time
  let update = updateTimes.find((time) => time.hour === hours && time.minute === minutes);

  // If an update time matches, make the Ajax call
  if (update) {
    $.ajax({
      url: update.endpoint,
      method: 'GET',
      contentType: 'application/json',
      success(data) {
        console.log(data);
      },
      error(err) {
        console.error('Error:', err);
      },
    });
  }
}

// Set interval to check for updates every minute
setInterval(sendSalesUpdate, 60000);
