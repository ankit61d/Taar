const fullNameInput = document.getElementById('full-name');
const phoneNumberInput = document.getElementById('phone-number');
const passwordInput = document.getElementById('password');
const registerBtn = document.getElementById('register-btn');


// Checking Cookie

// window.onload = (event) => {
//   console.log('page is fully loaded');

//   function getCookie(cookiename) {
//     let phoneNumber = cookiename + "=";
//     let cookiearray = document.cookie.split(';');
//     for (let i=0; i<cookiearray.length; i++) {
//       let cookies = cookiearray[i];
//       while (cookies.charAt(0) == ' ') {
//         cookies = cookies.substring(1);
//       }
//       if (cookies.indexOf(phoneNumber) == 0) {
//         return cookies.substring(phoneNumber.length, cookies.length);
//       }
//     }
//   }
// };

























registerBtn.addEventListener('click', function() {
  let fullName = fullNameInput.value;
  let phoneNumber = phoneNumberInput.value;
  let password = passwordInput.value;

  const inputObject = {
    full_name: fullName,
    phone_number: phoneNumber,
    password: password,
  }

  async function postRegisterData() {
    const response = await fetch('http://127.0.0.1:5000/api/register', {
      method: 'POST',
      body: JSON.stringify(inputObject),
      headers: {
        'Content-Type' : 'application/json'
      }
    });

    const responseText = await response.text();
    alert(responseText);
  }
  postRegisterData();
})

$(registerBtn).click(function() {
  window.location.href='http://127.0.0.1:5000/login';
})