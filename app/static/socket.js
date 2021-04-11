
var socket = io.connect('http://' + document.domain + ':' + location.port);
userId = Math.floor((Math.random() * 10) + 1);

// Handler for connect
socket.on('connect', function() {
  console.log('Websocket connected!');
});
// Handler for join room
socket.on('join_room', function(msg) {
  console.log(msg);
});

// To handle redirect request
socket.on('redirect', function (data) {
    window.location = data.url;
});

// On message handler
socket.on('message', function(msg){
  var node = document.createElement("LI");                 // Create a <li> node
  var textnode = document.createTextNode(msg.userId + ' ---- ' + msg.message);         // Create a text node
  node.appendChild(textnode);                              // Append the text to <li>
  document.getElementById("msg-list").appendChild(node); 
})

// Error handler
socket.on('error', function(msg){
    console.log(msg);
})

// Send Message function
function send(){
  var input = document.getElementById('message');
  messagetext = input.value;
  input.value = ''
  console.log(messagetext)
  socket.send({message: messagetext, roomId: '123', userId: userId});
}

// Join Room Function
function joinRoom(){
  console.log('Joining Room');
  socket.emit('join', {roomId: '123', userId: userId})
  var button = document.getElementById('room');
  button.disabled = true;
}

// Disconnect function
function disconnect(){
  console.log('Disconnect Webscoket');
  socket.disconnect()
}

// Create Room Function
function createRoom() {
  console.log('Creating Room');
  var room_name = document.getElementById('room_name').value;
  var description = document.getElementById('description').value;
  var user_name = document.getElementById('name').value;
  socket.emit('create', {
    user: { 'userId': userId, 'name': user_name },
    size: 'normal',
    room: { 'name': room_name, 'description': description }
  });
}
