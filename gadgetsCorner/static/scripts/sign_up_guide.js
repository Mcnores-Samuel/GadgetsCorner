window.addEventListener('load', function(event) {
    let myInfo = [
      'Welcome to Hafeez Enterprise!!',
      'Please fill in the form below to create an account.',
      'If you are our agent, please contact us to get your agent code. you know how to contact us.',
      'If you are our customer, please fill in the form below and leave the agent code field empty.',
      'Thank you for choosing Hafeez Enterprise.'
    ];
  
    function typeWriter(text, character, fnCallback) {
      if (character < text.length) {
        document.querySelector(".writeInfo").innerHTML = text.substring(0, character + 1) + '<span class="introInfo" aria-hidden="true"></span>';
        setTimeout(function() {
          typeWriter(text, character + 1, fnCallback)
        }, 50);
      } else if (typeof fnCallback == 'function') {
        setTimeout(fnCallback, 3000);
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
  