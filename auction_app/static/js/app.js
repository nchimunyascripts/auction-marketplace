  $(document).ready(function() {
    // Handle form submissions for register.html
    $('#register-form').submit(function(event) {
      event.preventDefault();
      $.post('/register', $(this).serialize(), function(data) {
        // Clear the form
        $('#register-form')[0].reset();

        // Show the success message or error message
        if (data.message) {
          $('#register-message').text(data.message).removeClass('error').addClass('message');
        } else if (data.error) {
          $('#register-message').text(data.error).removeClass('message').addClass('error');
        }
      });
    });

    // Handle form submissions for login.html
    $('#login-form').submit(function(event) {
      event.preventDefault();
      $.post('/login', $(this).serialize(), function(data) {
        // Clear the form
        $('#login-form')[0].reset();

        // Show the success message or error message
        if (data.message) {
          $('#login-message').text(data.message).removeClass('error').addClass('message');
          // Redirect to the profile page on successful login
          setTimeout(function() {
            window.location.href = '/profile?access_token=' + data.access_token;
          }, 1000);
        } else if (data.error) {
          $('#login-message').text(data.error).removeClass('message').addClass('error');
        }
      });
    });

    // Add other jQuery event handlers for other form submissions
  });

  