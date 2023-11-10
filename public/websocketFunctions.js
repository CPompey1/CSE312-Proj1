var ws = new WebSocket("ws://" + location.host + "/echo");
ws.onmessage = function (evt) {
    var received_msg = evt.data;
    alert(received_msg);
};
ws.onopen = function () {
    ws.send("Init");
};