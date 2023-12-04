// var ws = new WebSocket("ws://" + location.host + "/getAllAuctions");
var userWs = new WebSocket("wss://" + location.host + "/userAuctions");
// var socket = new WebSocket('ws://' + window.location.host + '/ws');


userWs.onmessage = function (message) {
    const data = JSON.parse(message.data);
    if (data.messageType === 'timerUpdate') {
        data.updatedTimes.forEach(element => {
        updateTimer(element.auctionId, element.timeLeft);
            });
        }
    };

function updateTimer(auctionId, timeLeft) {
    const timerElement = document.getElementById('timer_' + auctionId);
    if (timerElement) {
        timerElement.textContent = timeLeft;
    }
}

userWs.onopen = function(){

    userJson = authenticate();
    userWs.send(userJson);
    //Call get user auctions endpoint (gets created and won auctionn)

}
userWs.onmessage = function (evt) {
    var received_msg = evt.data;
    //Parse data
    console.log(received_msg);
    var json_obj = JSON.parse(received_msg);
    var html2Add = '';
    //Update Created Auctions
    var doc = document.getElementById('created_auctions');
    doc.innerHTML = "<h1>Live Auctions</h1>";
    for (const auction of json_obj["Created Auctions"])
        html2Add += chat2AuctionHTML(auction);
        doc.innerHTML += html2Add;


    //add to won auctions and created auctions
    var doc = document.getElementById('won_auctions');
    var html2Add = '';
    doc.innerHTML = "<h1>Closed Auctions</h1>";
    for (const auction of json_obj["Won Auctions"])
        html2Add += chat2AuctionHTML(auction);
        doc.innerHTML += html2Add;

};




function chat2AuctionHTML(auctionJSON) {
    const itemName = auctionJSON.title
    const category = auctionJSON.category;
    const highestBid = auctionJSON.highestBid;
    const imageName = auctionJSON.imageUrl
    const auction_id = String(auctionJSON._id);
    const hoursRemaing = auctionJSON.timeLeft;
    const description = auctionJSON.description;
    const username = auctionJSON.username;
    let auctionHTML =
    "<div class='auction' id='auction_" + auction_id + "'>" +
        "<img class='image' src='../image/auction_images/" + imageName + "' alt='item image'>" +
        "<h2>" + itemName + "</h2>" +
        "<p>" + description + "</p>" +
        "<p>Highest Bid: " + highestBid + "</p>" +
        "<p>Auction id: " + auction_id + "</p>" +
        "<p>Time Left:" + hoursRemaing+ "</p>" +
    "</div>";

    return auctionHTML;
}


