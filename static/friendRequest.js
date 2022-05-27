const container = document.getElementById('container');
const friendRequest = document.getElementById('friend-request');


let token = document.cookie.split('=')[1];

window.addEventListener('load', (event) => {
  async function getFriendRequest() {
    const response = await fetch('http://127.0.0.1:5000/api/friends/view-requests', {
      method: 'GET',
      headers: {
        'Content-Type' : 'application/json',
        'UserToken' : token,
      }
    });
    const responseJson = await response.json();
    console.log(responseJson);
    let htmlStr = "";
    for (let i=0; i<responseJson.requests.length; i++) {
      htmlStr += "<p>Request from " + responseJson.requests[i].name + " <button onclick=\"sendFriendRequestResponse(" + responseJson.requests[i].friend_request_id + "," + "status=2" + ")\">Accept</button><button onclick=\"sendFriendRequestResponse(" + responseJson.requests[i].friend_request_id + "," + "status=3" + ")\">Reject</button><p>"
    }
    friendRequest.insertAdjacentHTML('beforeend', htmlStr);
  }
  getFriendRequest();
})


function sendFriendRequestResponse(id, status) {

  const requestObject = {
    friend_request_id: id,
    status: status
  }

  async function postFriendRequestResponse() {
    const response = await fetch('http://127.0.0.1:5000/api/friends/respond-to-requests', {
      method: 'POST',
      body: JSON.stringify(requestObject),
      headers: {
        'Content-Type': 'application/json',
        'UserToken': token,
      }
    })
    const responseJson = await response.json();
    console.log(responseJson);
  };
  postFriendRequestResponse();
};