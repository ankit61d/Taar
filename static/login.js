const phoneNumberInput = document.getElementById('phone-number');
const passwordInput = document.getElementById('password');
const loginBtn = document.getElementById('login-btn');


window.onload = checkCookie();


function setCookie(name,value,days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}


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
    loginBtnClickEvent();
  }
}
// trying 3rd thing ends here


function loginBtnClickEvent() {
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
    
        const responseJson = await response.json();
        if (response.status == 200) {
          setCookie("UserToken", responseJson.token, 7)
          alert("Successfully logged in.");
          window.location.href='http://127.0.0.1:5000/chat';
        }
        else {
          alert("Error: user dosen't exit or wrong password");
        }

      }
      postLoginData();
    }
    else {
      alert("Please Check the input fields.");
    }
  })
}









































// function checkCookie() {
//   let user = getCookie("UserToken");
//   if (user != "") {
//     alert("Welcome again " + user);
//   } else {
//     user = prompt("Please enter your name:", "");
//     if (user != "" && user != null) {
//       setCookie("UserToken", responseJson.token, 7)
//     }
//   }
// }


// trying 2nd thing
// loginBtn.addEventListener('click', function() {
//   let phoneNumber = phoneNumberInput.value;
//   let password = passwordInput.value;

//   if (phoneNumber != '' && password != '') {
//     const inputObject = {
//       phone_number: phoneNumber,
//       password: password,
//     }
  
//     async function postLoginData() {
//       const response = await fetch('http://127.0.0.1:5000/api/login', {
//         method: 'POST',
//         body: JSON.stringify(inputObject),
//         headers: {
//           'Content-Type' : 'application/json'
//         }
//       });
  
//       const responseJson = await response.json();
//       console.log(responseJson.token);
//       // document.cookie = "UserToken=" + responseJson.token;
//       setCookie("UserToken", responseJson.token, 7);
//       const toRedirect = confirm("Successfully logged in.");
//       if (toRedirect) {
//         window.location.href='http://127.0.0.1:5000/chat';
//       }
//     }
//     postLoginData();
//   }
//   else {
//     alert("Please Check the input fields.");
//   }
// })
//  trying 2nd thing ends here

// .
// .


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