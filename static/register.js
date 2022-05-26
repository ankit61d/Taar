const fullNameInput = document.getElementById('full-name');
const phoneNumberInput = document.getElementById('phone-number');
const passwordInput = document.getElementById('password');
const registerBtn = document.getElementById('register-btn');


window.onload = (event) => {
  console.log('page is fully loaded');
  checkCookie();
};


function getCookie(cname) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


// trying 3rd thing 
function checkCookie() {
  let user = getCookie("UserToken");
  if (user != "") {
    alert("Welcome again you are already logged in!");
    window.location.href='http://127.0.0.1:5000/chat';
  } 
  else {
    registerBtnClickEvent();
  }
}
// trying 3rd thing ends here


function registerBtnClickEvent() {
  registerBtn.addEventListener('click', function() {
    let fullName = fullNameInput.value;
    let phoneNumber = phoneNumberInput.value;
    let password = passwordInput.value;
  
  
    if (fullName != '' && phoneNumber != '' && password != '') {
      
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
        console.log(responseText);
        if (response.status == 200) {
          alert("You are registered please login");
          window.location.href='http://127.0.0.1:5000/login';
        } else {
          alert("Some error occured please try again");
        }
      }
      postRegisterData();
    } 
    else {
      alert("Please Check the input fields.");
    }
  })
}
























































// tyring 2nd things
// registerBtn.addEventListener('click', function() {
//   let fullName = fullNameInput.value;
//   let phoneNumber = phoneNumberInput.value;
//   let password = passwordInput.value;


//   if (fullName != '' && phoneNumber != '' && password != '') {
    
//     const inputObject = {
//       full_name: fullName,
//       phone_number: phoneNumber,
//       password: password,
//     }

//     async function postRegisterData() {
//       const response = await fetch('http://127.0.0.1:5000/api/register', {
//         method: 'POST',
//         body: JSON.stringify(inputObject),
//         headers: {
//           'Content-Type' : 'application/json'
//         }
//       });
  
//       const responseText = await response.text();
//       const toRedirect = confirm(responseText);
//       if (toRedirect) {
//         window.location.href='http://127.0.0.1:5000/login';
//       }
//     }
//     postRegisterData();
//   } 
//   else {
//     alert("Please Check the input fields.");
//   }
// })
// trying 2nd thing ends here

// .
// .

// 1st try starts

// registerBtn.addEventListener('click', function() {
//   let fullName = fullNameInput.value;
//   let phoneNumber = phoneNumberInput.value;
//   let password = passwordInput.value;

//   const inputObject = {
//     full_name: fullName,
//     phone_number: phoneNumber,
//     password: password,
//   }

//   async function postRegisterData() {
//     const response = await fetch('http://127.0.0.1:5000/api/register', {
//       method: 'POST',
//       body: JSON.stringify(inputObject),
//       headers: {
//         'Content-Type' : 'application/json'
//       }
//     });

//     const responseText = await response.text();
//     alert(responseText);
//   }
//   postRegisterData();
// })

// $(registerBtn).click(function() {
//   window.location.href='http://127.0.0.1:5000/login';
// })

// 1st try ends