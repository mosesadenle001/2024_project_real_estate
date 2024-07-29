<script>
    document.addEventListener('DOMContentLoaded', function () {
        // Registration Form Validation
        var registrationForm = document.getElementById('registrationForm');
        if (registrationForm) {
            registrationForm.addEventListener('submit', function (event) {
                var username = document.getElementById('username').value;
                var email = document.getElementById('email').value;
                var password = document.getElementById('password').value;
                var confirmPassword = document.getElementById('confirmPassword').value;

                // Email validation regex
                var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;

                if (username.trim() === '' || email.trim() === '' || password.trim() === '' || confirmPassword.trim() === '') {
                    alert('All fields are required.');
                    event.preventDefault();
                } else if (!emailPattern.test(email)) {
                    alert('Please enter a valid email address.');
                    event.preventDefault();
                } else if (password.length < 6) {
                    alert('Password must be at least 6 characters long.');
                    event.preventDefault();
                } else if (password !== confirmPassword) {
                    alert('Passwords do not match.');
                    event.preventDefault();
                }
            });
        }

        // Login Form Validation
        var loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', function (event) {
                var email = document.getElementById('email').value;
                var password = document.getElementById('password').value;

                if (email.trim() === '' || password.trim() === '') {
                    alert('All fields are required.');
                    event.preventDefault();
                }
            });
        }
    });
</script>

