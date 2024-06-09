window.addEventListener('load', function(event) {
    let myInfo = ['Note:',
    'You must select payment method before you can sell a device.',
    'If you sell a device by cash payment, You can skip the customer data collection and hit submit.',
    'If you sell a device by loan payment, You must collect the customer information and other necessary information.',
    'That is all. Happy selling!'];
  
    function typeWriter(text, character, fnCallback) {
      if (character < text.length) {
        document.querySelector(".data_intake_guide").innerHTML = text.substring(0, character + 1) + '<span class="introInfo" aria-hidden="true"></span>';
        setTimeout(function() {
          typeWriter(text, character + 1, fnCallback)
        }, 100);
      } else if (typeof fnCallback == 'function') {
        setTimeout(fnCallback, 2000);
      }
    }
  
    function StartTextAnimation(index) {
      if (index < myInfo.length) {
        typeWriter(myInfo[index], 0, function() {
          StartTextAnimation(index + 1);
        });
      }
    }
  
    StartTextAnimation(0);
  });