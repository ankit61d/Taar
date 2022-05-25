const phoneNumberInput = document.getElementById('phone-number');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');

loginBtn.addEventListener('click', function() {
  let phoneNumber = phoneNumberInput.value;
  let password = passwordInput.value;

  if (phoneNumber != '' && password != '') {
    const inputObject = {
      phone_number: phoneNumber,
      password: password,
    }
  
    async function postLoginData() {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        body: JSON.stringify(inputObject),
        headers: {
          'Content-Type' : 'application/json'
        }
      });
  
      const responseText = await response.text();
      const toRedirect = confirm("Successfully logged in.");
      if (toRedirect) {
        window.location.href='http://127.0.0.1:5000/chat';
      }
    }
    postLoginData();
  }
  else {
    alert("Please Check the input fields.");
  }
})























// *trying 1st thing starts*

// loginBtn.addEventListener('click', function() {
//   let phoneNumber = phoneNumberInput.value;
//   let password = passwordInput.value;

//   const inputObject = {
//     phone_number: phoneNumber,
//     password: password,
//   }

//   async function postLoginData() {
//     const response = await fetch('http://127.0.0.1:5000/api/login', {
//       method: 'POST',
//       body: JSON.stringify(inputObject),
//       headers: {
//         'Content-Type' : 'application/json'
//       }
//     });

//     const responseText = await response.text();
//     alert(responseText);
//   }
//   postLoginData();
// })

// $(loginBtn).click(function() {
//   window.location.href='http://127.0.0.1:5000/chat'
// })

// *trying 1st thing ends here*