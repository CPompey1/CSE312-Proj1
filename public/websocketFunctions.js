// var ws = new WebSocket("ws://" + location.host + "/getAllAuctions");
var ws = new WebSocket("ws://" + location.host + "/getAllAuctions/cat");
ws.onmessage = function (evt) {
    var received_msg = evt.data;
    alert(received_msg);
};
ws.onopen = function () {
    ws.send("Init");
};