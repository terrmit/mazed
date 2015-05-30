var socket = new WebSocket('wss://localhost:5000/websocket');

var canvas;
var ctx;
var dx = 5;
var dy = 5;
var WIDTH = 600;
var HEIGHT = 400;


function circle(x,y,r) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, Math.PI*2, true);
    ctx.fill();
}


function rect(x,y,w,h) {
    ctx.beginPath();
    ctx.rect(x,y,w,h);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
}


function clear() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
}


function init() {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    // return setInterval(draw, 5);
}


function doKeyDown(evt){
    switch (evt.keyCode) {
        case 38:  /* Up arrow was pressed */
            socket.send('up');
            break;
        case 40:  /* Down arrow was pressed */
            socket.send('down');
            break;
        case 37:  /* Left arrow was pressed */
            socket.send('left');
            break;
        case 39:  /* Right arrow was pressed */
            socket.send('right');
            break;
    }
}


var clients = {};


function draw() {
    clear();
    ctx.fillStyle = 'white';
    ctx.strokeStyle = 'black';
    rect(0, 0, WIDTH, HEIGHT);
    ctx.fillStyle = 'purple';

    for (var property in clients) {
        if (clients.hasOwnProperty(property)) {
            circle(clients[property].x, clients[property].y, 10);
        }
    }
}

init();


socket.onmessage = function(event) {
    var player = JSON.parse(event.data);
    clients[player.id] = {
        x: player.x,
        y: player.y
    };
    draw();
};


window.addEventListener('keydown', doKeyDown, true);