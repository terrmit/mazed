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
var WIDTH = 600;
var HEIGHT = 600;
var viewportParams = { maxWidth: 1200, maxHeight: 1200, aspect: WIDTH/HEIGHT };
var cellSize;
var dateStart = Date.now();


function timestamp() {
    return Date.now() - dateStart;
}

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
    canvas = $('#canvas')[0];
    ctx = canvas.getContext('2d');
    initMaze();
}

var maze = [];
var mazeSize = 0;

function initMaze() {
    $.get('//'+loc.host+'/maze', function(data) {
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

function getKeyCode(evt) {
    var code = null;
    switch (evt.keyCode) {
        case 38:  /* Up arrow was pressed */
            code = 'up';
            break;
        case 40:  /* Down arrow was pressed */
            code = 'down';
            break;
        case 37:  /* Left arrow was pressed */
            code = 'left';
            break;
        case 39:  /* Right arrow was pressed */
            code = 'right';
            break;
    }

    return code;
}

var keys = {
        up: {
            isDown: false,
            timeout: null,
            interval: null
        },
        down: {
            isDown: false,
            timeout: null,
            interval: null
        },
        left: {
            isDown: false,
            timeout: null,
            interval: null
        },
        right: {
            isDown: false,
            timeout: null,
            interval: null
        }
    },
    keyTimeout = 30,
    keyInterval = 30;

function sendKeyCode( code ) {
    if ( !code ) return;

    // console.log(timestamp(), 'SEND CODE:', code);
    socket.send( code );
}

function handleKeyDown(evt) {
    // evt.preventDefault();

    var code = getKeyCode(evt);

    if( !code || keys[code].isDown ) return;

    sendKeyCode( code );

    keys[code].isDown = true;

    keys[code].timeout = setTimeout(
        function () {
            sendKeyCode( code );
            keys[code].interval = setInterval( sendKeyCode.bind(null, code), keyInterval );
        }, keyTimeout );
}

function handleKeyUp(evt) {
    var code = getKeyCode(evt);

    if( !code ) return;

    keys[code].isDown = false;

    if ( keys[code].timeout )
        clearTimeout( keys[code].timeout );

    if ( keys[code].interval )
        clearInterval( keys[code].interval );
}

function handleWindowBlur() {
    console.log('window blur');

    for ( code in keys ) {
        keys[code].isDown = false;

        if ( keys[code].timeout )
            clearTimeout( keys[code].timeout );

        if ( keys[code].interval )
            clearInterval( keys[code].interval );
    }
}

function handleWindowResize() {
    var c = $('#canvas'),
        w = $(window);

    var w_asp = w.width() / w.height();

    if ( w_asp > viewportParams.aspect && w.height() < viewportParams.maxHeight ) {
        WIDTH = w.height() * viewportParams.aspect;
        HEIGHT = w.height();
    }
    else if ( w_asp <= viewportParams.aspect && w.width() < viewportParams.maxWidth ) {
        WIDTH = w.width();
        HEIGHT = w.width() / viewportParams.aspect;
    }
    else {
        WIDTH = viewportParams.maxWidth;
        HEIGHT = viewportParams.maxHeight;
    }

    cellSize = WIDTH / mazeSize;
    c.attr({ height: WIDTH, width: HEIGHT });
    draw();
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
            var pos = {
                x: clients[property].x * cellSize,
                y: clients[property].y * cellSize   
            }
            circle(pos.x, pos.y, cellSize / 2 - 2);
        }
    }
}

init();
handleWindowResize();

socket = new WebSocket(new_uri);

socket.onmessage = function(event) {
    var player = JSON.parse(event.data);
    clients[player.id] = {
        x: player.x,
        y: player.y
    };
    draw();
};

$(window).keydown( handleKeyDown );
$(window).keyup( handleKeyUp );
$(window).blur( handleWindowBlur );
$(window).resize( handleWindowResize );