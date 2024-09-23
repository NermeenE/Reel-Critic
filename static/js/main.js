// nav link active
function updateNav() {
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  const sections = document.querySelectorAll('section');

  let current = '';
  sections.forEach(section => {
    const sectionOffset = parseInt(section.dataset.offset) || 0;
    const sectionTop = section.offsetTop - sectionOffset;
    const sectionHeight = section.clientHeight;
    if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
      current = section.getAttribute('id');
    }
  });

  navLinks.forEach(link => {
    link.classList.remove('active');
    if (link.getAttribute('href') === '#' + current) {
      link.classList.add('active');
    }
  });
}

function setupAutoplayVideo() {
  const video = document.querySelector("video");
  if (video) {
    // Ensure autoplay starts after the page loads
    video.play().catch(error => {
      console.error("Autoplay failed:", error);
    });
  }
}

// Smooth scrolling nav link
function setupNavLinks() {
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link, .offcanvas .nav-link');

  navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const href = this.getAttribute('href');

      if (href.startsWith('#')) {
        e.preventDefault();
        const targetElement = document.querySelector(href);

        if (targetElement) {
          const targetOffset = parseInt(targetElement.dataset.offset) || 0;
          const targetPosition = targetElement.offsetTop - targetOffset;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      }
    });
  });
}

// Change button text based on user authentication status:
function setupSubscribeButton() {
  const subscribeBtn = document.querySelector('#subscribe-btn');
  if (subscribeBtn) {
    const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
    if (isAuthenticated) {
      subscribeBtn.textContent = 'Subscribe';
      subscribeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        const targetElement = document.querySelector('#subscribe-jumbotron');
        if (targetElement) {
          const additionalOffset = 100;
          const targetPosition = targetElement.offsetTop - additionalOffset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    } else {
      subscribeBtn.textContent = 'Sign Up';
    }
  }
}

// jumbotron subscribe submission
function setupSubscriptionForm() {
  const jumbotronSubscribeForm = document.querySelector('#subscribe-form');
  const flashMessage = document.querySelector('#flash-message');
  const emailInput = jumbotronSubscribeForm.querySelector('input[type="email"]');

  if (jumbotronSubscribeForm) {
    jumbotronSubscribeForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      flashMessage.textContent = 'Newsletter is on its way! Thank you for Subscribing!';
      flashMessage.classList.remove('d-none');
      flashMessage.classList.add('show');

      emailInput.value = '';

      setTimeout(function() {
        flashMessage.classList.remove('show');
        flashMessage.classList.add('d-none');
      }, 2000);
    });
  }
}

// Main Navbar Search
function setupSearchInput() {
  const container = document.getElementById('search-container');
  const input = document.getElementById('search-input');
  const icon = document.getElementById('search-icon');

  icon.addEventListener('click', function() {
    container.classList.toggle('expanded');
    if (container.classList.contains('expanded')) {
      input.focus();
    } else {
      input.blur();
    }
  });

  document.addEventListener('click', function(event) {
    if (!container.contains(event.target) && !icon.contains(event.target)) {
      container.classList.remove('expanded');
      input.blur();
    }
  });

  container.addEventListener('mouseleave', function() {
    container.classList.remove('expanded');
    input.blur();
  });

  input.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      console.log('Search term:', input.value);
      input.value = '';
    }
  });

  container.addEventListener('mouseenter', function() {
    container.classList.add('expanded');
    input.focus();
  });
}

// hide alerts
function setupAlerts() {
  function autoHideAlert(alertElement, delay) {
    setTimeout(function() {
      alertElement.classList.add('fade');
      setTimeout(function() {
        alertElement.style.display = 'none';
      }, 500);
    }, delay);
  }

  const successAlerts = document.querySelectorAll('.alert-success');
  successAlerts.forEach(alert => autoHideAlert(alert, 2000));

  const warningAlerts = document.querySelectorAll('.alert-warning');
  warningAlerts.forEach(alert => autoHideAlert(alert, 2000));

  const dangerAlerts = document.querySelectorAll('.alert-danger');
  dangerAlerts.forEach(alert => autoHideAlert(alert, 2000));
}

// Error display
function setupErrorAlerts() {
  const urlParams = new URLSearchParams(window.location.search);
  const errors = urlParams.getAll('errors');

  if (errors.length > 0) {
    const passwordAlert = document.getElementById('passwordAlert');
    const confirmPasswordAlert = document.getElementById('confirmPasswordAlert');

    errors.forEach(error => {
      if (error.includes('Password must be')) {
        passwordAlert.innerHTML = error;
        passwordAlert.style.display = 'block';
      } else if (error.includes('Passwords do not match')) {
        confirmPasswordAlert.innerHTML = error;
        confirmPasswordAlert.style.display = 'block';
      } else if (error.includes('Email already exists')) {
        const emailAlert = document.createElement('div');
        emailAlert.className = 'alert alert-danger';
        emailAlert.innerHTML = error;
        document.querySelector('form').insertBefore(emailAlert, document.querySelector('form').firstChild);
      }
    });
  }
}

//password visibility
function setupPasswordToggle() {
  const toggleButtons = document.querySelectorAll('.fa-eye, .fa-eye-slash');
  
  toggleButtons.forEach(button => {
    button.addEventListener('click', function() {
      const passwordField = this.closest('.form-floating').querySelector('input[type="password"], input[type="text"]');
      
      if (passwordField) {
        if (passwordField.type === 'password') {
          passwordField.type = 'text';
          this.classList.remove('fa-eye');
          this.classList.add('fa-eye-slash');
        } else {
          passwordField.type = 'password';
          this.classList.remove('fa-eye-slash');
          this.classList.add('fa-eye');
        }
      }
    });
  });
}

// Countdown cardwrapper animation
function setupCardWrapperAnimation() {
  const cardWrappers = document.querySelectorAll('.card-wrapper');

  const observerOptions = {
    root: null,
    rootMargin: '0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-bottom');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  cardWrappers.forEach(cardWrapper => {
    observer.observe(cardWrapper);
  });
}

// Main initialization function
document.addEventListener('DOMContentLoaded', function() {
  setupPasswordToggle();
  updateNav();
  setupNavLinks();
  window.addEventListener('scroll', updateNav);
  setupCardWrapperAnimation();
  setupAlerts();
  setupErrorAlerts();
  setupSearchInput();
  setupSubscriptionForm();
  setupSubscribeButton();
  setupAutoplayVideo();
  
  
});
