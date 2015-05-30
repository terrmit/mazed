var loc = window.location, new_uri;
if (loc.protocol === 'https:') {
    new_uri = 'wss:';
} else {
    new_uri = 'ws:';
}
new_uri += '//' + loc.host;
new_uri += loc.pathname + 'websocket';

var socket;

var canvas;
var ctx;
var dx = 5;
var dy = 5;
var WIDTH = 600;
var HEIGHT = 600;
var cellSize;


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


function line(x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}

function clear() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
}


function init() {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    initMaze();
}

var maze = [];
var mazeSize = 0;

function initMaze() {
    $.get('/maze', function(data) {
        var parsedData = JSON.parse(data);
        maze = parsedData.maze;
        mazeSize = parsedData.size;
        cellSize = WIDTH / mazeSize;
        drawMaze();
    });
}

function drawMaze() {
    for (var j = 0; j < maze.length; j++) {
        for (var i = 0; i < maze[j].length; i++) {
            if (maze[j][i].up) {
                line(i * cellSize, j * cellSize, (i + 1) * cellSize, j * cellSize);
            }
            if (maze[j][i].down) {
                line(i * cellSize, (j + 1) * cellSize, (i + 1) * cellSize, (j + 1) * cellSize);
            }
            if (maze[j][i].left) {
                line(i * cellSize, j * cellSize, i * cellSize, (j + 1) * cellSize);
            }
            if (maze[j][i].right) {
                line((i + 1) * cellSize, j * cellSize, (i + 1) * cellSize, (j + 1) * cellSize);
            }
        }
    }
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

    drawMaze();

    for (var property in clients) {
        if (clients.hasOwnProperty(property)) {
            circle(clients[property].x, clients[property].y, cellSize / 2 - 2);
        }
    }
}

init();

socket = new WebSocket(new_uri);

socket.onmessage = function(event) {
    var player = JSON.parse(event.data);
    clients[player.id] = {
        x: player.x,
        y: player.y
    };
    draw();
};


window.addEventListener('keydown', doKeyDown, true);