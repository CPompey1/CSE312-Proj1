// var ws = new WebSocket("ws://" + location.host + "/getAllAuctions");
var userWs = new WebSocket("ws://" + location.host + "/userAuctions");

userWs.onopen = function(){
    
    userJson = authenticate();
    userWs.send(userJson);
    //Call get user auctions endpoint (gets created and won auctionn)
    
}
userWs.onmessage = function (evt) {
    var received_msg = evt.data;
    //Parse data
    console.log(received_msg);
    json_obj = JSON.parse(received_msg);
    //add to won auctions and created auctions
    
};


