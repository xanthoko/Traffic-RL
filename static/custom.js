class RoutePoints {
    constructor() {
        this.canvas = null;
        this.shape = -1;
        this.width = -1;
        this.height = -1;
        this.coords = [];
        this.connections = [];
    }

    setParams(shape, width, height, canvas) {
        this.shape = shape;
        this.width = width;
        this.height = height;
        this.canvas = canvas;
    }

    appendConnection(id1, id2) {
        var ind1 = parseInt(id1);
        var ind2 = parseInt(id2);
        this.connections.push([ind1, ind2]);
        // draw line
        this.connectLine(ind1, ind2)
    }

    connectLine(pnt1, pnt2) {
        var ctx = this.canvas.getContext("2d");
        var coord1 = this.coords[pnt1];
        var coord2 = this.coords[pnt2];

        ctx.beginPath();
        ctx.moveTo(...coord1);
        ctx.lineTo(...coord2);
        ctx.stroke();
    }

    formTable() {
        var ctx = this.canvas.getContext("2d");

        var padValue = 100;
        var radius = 10;

        var stepx = (this.width - 2 * padValue) / (this.shape - 1);
        var stepy = (this.height - 2 * padValue) / (this.shape - 1);

        for (let x = padValue; x <= this.width - padValue; x += stepx) {
            for (let y = padValue; y <= this.height - padValue; y += stepy) {
                ctx.beginPath();
                ctx.arc(x, y, radius, 0, 2 * Math.PI);
                ctx.stroke();
                this.coords.push([x, y]);
            }
        }
    }
}

var start = function (inptId) {
    var inpt = document.getElementById(inptId).value;
    var shape = parseInt(inpt);

    // check if given input is a number
    if (isNaN(shape)) {
        console.log('Invalid input')
    }
    else {
        // show canvas
        canvas = document.getElementById("pathCanvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        rPoints.setParams(shape, window.innerWidth, innerHeight, canvas);

        // form the points table
        rPoints.formTable();

        // show the connections input
        document.getElementById("connDiv").removeAttribute('hidden');
    }
}


var addConn = function (inptId) {
    var connectionStr = document.getElementById(inptId).value;
    var edges = connectionStr.split('-');
    var edge1 = edges[0];
    var edge2 = edges[1];

    rPoints.appendConnection(edge1, edge2)
}


const rPoints = new RoutePoints();
