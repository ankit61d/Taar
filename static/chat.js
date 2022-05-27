const friends = document.getElementById('friends');
const msgContainer = document.getElementById('msg-container');

let token = document.cookie.split('=')[1];

async function sendMsg(userId, userName) {

  const message = document.getElementById('msg').value;
  console.log(message);

  const response = await fetch('http://127.0.0.1:5000/api/messages/' + userId, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'UserToken': token,
    },
    body: JSON.stringify({content: message}),
  });
  const responseJson = await response.text();
  console.log(responseJson);
  loadFriendMessage(userId, userName); 
} 

async function loadFriendMessage(userId, userName) {
  const response = await fetch('http://127.0.0.1:5000/api/messages/' + userId, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'UserToken': token,
    }
  });
  const responseJson = await response.json();
  console.log(responseJson);
  let htmlStr = "<h3>msg from " + userName + "</h3>";
  let messages = responseJson.messages
  for (let i=0; i<messages.length; i++) {
    htmlStr += "<p>"+ messages[i].sender +" : " + messages[i].content + "</p>"
  }
  htmlStr += ('<h3>Enter msg below</h3><p><input id="msg" type="text"><button onclick="sendMsg(' + userId + ",'" + userName + '\')">Send</button></p>')
  console.log(htmlStr);
  msgContainer.innerHTML = htmlStr;
}

window.addEventListener('load', function() {
  async function getMyFriends() {
    const response = await fetch('http://127.0.0.1:5000/api/friends', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'UserToken': token,
      }
    });
    const responseJson = await response.json();
    console.log(responseJson);
    let htmlStr = "";
    for (let i=0; i<responseJson.length; i++) {
      htmlStr += "<button onclick=\"loadFriendMessage(" + responseJson[i].userId + ",'" + responseJson[i].name + "')\">"+ responseJson[i].name +"</button> "
    }
    friends.insertAdjacentHTML('beforeend', htmlStr);
  };
  getMyFriends();
});

