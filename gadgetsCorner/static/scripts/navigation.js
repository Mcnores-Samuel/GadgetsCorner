const navBar = document.querySelector('header');
const menu = document.querySelector('.menu');
const navigation = document.querySelector('.heading');
const profile = document.querySelector('.profile');
const settings = document.querySelector('.mobile-set');
const body = document.querySelector('body');

let profileSettings = null;
let isProfileSettingsDisplayed = false; 

// Function to close the menu
function closeMenu () {
  navigation.classList.remove('dropmenu');
  profile.style.display = 'block';
  settings.style.display = 'none';
}

window.addEventListener('scroll', () => {
  if (window.scrollY > 10) {
    navBar.style.boxShadow = "3px 3px 7px grey"
  }
  else{
    navBar.style.boxShadow = "none"
  }
});

// Event listener to close the menu when clicking outside
window.addEventListener('click', (e) => {
  if (!menu.contains(e.target)) {
    closeMenu();
  }
});

menu.addEventListener('click', () => {
  navigation.classList.toggle('dropmenu');
  navigation.style.boxShadow = "3px 3px 7px grey"
  if (navigation.classList.contains('dropmenu')) {
    navigation.classList.add('opening');
    profile.style.display = 'none';
    settings.style.display = 'block';
  } else {
    navigation.classList.add('closing');
    setTimeout(() => {
      navigation.classList.remove('opening', 'closing');
      profile.style.display = 'block';
      settings.style.display = 'none';
    }, 500);
  }
});

// Event listener to open the menu when clicking on the menu button
// menu.addEventListener('click', () => {
//   navigation.classList.toggle('dropmenu');
//   navigation.classList.toggle('open')

//   if (navigation.classList.contains('dropmenu')) {
//     profile.style.display = 'none';
//     settings.style.display = 'block';
//   } else {
//     closeMenu();
//   }
// });

// Event listener to close the menu when scrolling
// window.addEventListener('scroll', () => {
//   closeMenu();
// });

// Event listener to close the menu when resizing the window
window.addEventListener('resize', () => {
  closeMenu();
});

try {
  const enable = document.querySelector('.category-btn');
  const category = document.querySelector('.Categories');
  const details_section = document.querySelector('.Categories-extended');

  enable.addEventListener('click', () => {
    category.classList.toggle('show-category');
    details_section.classList.toggle('resize-details');
    category.style.display = 'block';
    if (category.classList.contains('show-category')) {
      enable.innerHTML = '<i class="bx bx-x"></i>';
      enable.classList.add('close-category');
    }
    else {
      enable.innerHTML = '<i class="bx bx-category"></i>';
      enable.classList.remove('close-category');
      category.style.display = 'none';
    }
  });
}
catch(err) {
  console.log(err);
}

profile.addEventListener('click', () => {
  if (!isProfileSettingsDisplayed) {
    profileSettings = document.createElement('div');
    profileSettings.classList.add('profile-settings');
    profileSettings.innerHTML ='<ul><li><i class="bx bx-cog"></i><a href="/system_core_1/profile/">Settings</a></li>\
    <li><i class="bx bx-log-out"></i><a href="/system_core_1/sign_out/">Sign out</a></li></ul>';
    // profileSettings.innerHTML = '';
    navBar.appendChild(profileSettings);
    isProfileSettingsDisplayed = true; // Set the flag to true
  } else {
    // If it's displayed, hide it and remove it from the DOM
    profileSettings.style.display = 'none';
    navBar.removeChild(profileSettings);
    isProfileSettingsDisplayed = false; // Set the flag to false
    profileSettings = null; // Reset the profileSettings variable
  }
});
