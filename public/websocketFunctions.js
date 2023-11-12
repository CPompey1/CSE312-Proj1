// var ws = new WebSocket("ws://" + location.host + "/getAllAuctions");
function getAllAuctions(){
    var ws = new WebSocket("ws://" + location.host + "/getAllAuctions/");
}

function getCatAuctions(category){
    var ws = new WebSocket("ws://" + location.host + "/getAllAuctions/" + category);
}

function getUserAuctions(){
    const request = new XMLHttpRequest();
    request.setRequestHeader('Content-Type','application/json');
    userJson = authenticate()
    //Call get user auctions endpoint (gets created and won auctionn)
    request.open('POST', '/getUserAuctions');
    request.onload = () => {
    if (request.status === 200) {
        //store in json
        const userAuctions = JSON.parse(request.responseText);

        //add html to page
        
        console.log(userAuctions);
    } else {
        console.error('Request failed.  Returned status of ' + request.status);
    }
    };
    request.send(JSON.stringify(userJson));
    
    
}
ws.onmessage = function (evt) {
    var received_msg = evt.data;
    //Parse data
    //add to won auctions and created auctions
    alert(received_msg);
};
ws.onopen = function () {
    ws.send("Init");
};

