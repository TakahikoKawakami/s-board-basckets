window.onload = function() {
  document.getElementById('btn_submit').onclick = function() {
    post();
  };
};

function post(cmd) {
  var data = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    message: document.getElementById('message').value
  }
  xmlHttpRequest = new XMLHttpRequest();
  xmlHttpRequest.open('POST', 'contact', true);
  xmlHttpRequest.setRequestHeader( 'Content-Type', 'application/json');
  xmlHttpRequest.send( JSON.stringify(data) );
}
