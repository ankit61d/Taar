const registerBtn = document.getElementById('register-btn');
const loginBtn = document.getElementById('login-btn');

$(loginBtn).click(function() {
  window.location.href='http://127.0.0.1:5000/login'
})

$(registerBtn).click(function() {
  window.location.href='http://127.0.0.1:5000/register'
})