const phoneNumberInput = document.getElementById('phone-number');
const sendFriendRequestBtn = document.getElementById('send-friend-request-btn');

let token = document.cookie.split('=')[1];
// console.log(document.cookie.split('=')[1]);


sendFriendRequestBtn.addEventListener('click', function() {
  let phoneNumber = phoneNumberInput.value;

  const inputObject = {
    phone_number: phoneNumber 
  }

  async function postPhoneNumber() {
    const  response = await fetch('http://127.0.0.1:5000/api/friends/add', {
      method: 'POST',
      body: JSON.stringify(inputObject),
      headers: {
        'Content-Type': 'application/json',
        'UserToken': token,
      }
    });
    const responseText = await response.text();
    
    if (response.status == 200) {
      alert("Friend request sent");
    } else {
      alert("Error Please Check the phone number");
    }
  }
  postPhoneNumber();
})