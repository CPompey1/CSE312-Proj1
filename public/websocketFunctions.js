// var ws = new WebSocket("ws://" + location.host + "/getAllAuctions");
function getAllAuctions(){
    var ws = new WebSocket("ws://" + location.host + "/getAllAuctions/");
}

// function getCatAuctions(category){
//     var ws = new WebSocket("ws://" + location.host + "/getAllAuctions/" + category);
// }

userWs.onopen = function(){
    
    userJson = authenticate();
    userWs.send(userJson);
    //Call get user auctions endpoint (gets created and won auctionn)
    
}
userWs.onmessage = function (evt) {
    var received_msg = evt.data;
    //Parse data
    //add to won auctions and created auctions
    console.log(received_msg)
};

ws.onmessage = function (evt) {
    var received_msg = evt.data;
    //Parse data
    //add to won auctions and created auctions
    alert(received_msg);
};
ws.onopen = function () {
    ws.send("Init");
};

