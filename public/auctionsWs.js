
var auctionWs = new WebSocket("ws://" + location.host + "/getAllAuctions");

auctionWs.onopen = function(){
    auctionWs.send("None");
    //Call get user auctions endpoint (gets created and won auctionn)
    
}
auctionWs.onmessage = function (evt) {
    var received_msg = evt.data;
    //Parse data
    console.log(received_msg);
    var json_obj = JSON.parse(received_msg);
    var html2Add = '';
    //Update Created Auctions
    var doc = document.getElementById('created_auctions');
    doc.innerHTML = "<h1>Live Auctions</h1>";
    for (const auction of json_obj["Created Auctions"])
        html2Add += chat2AuctionHTML(auction, "created");
        doc.innerHTML += html2Add;
    

    //add to won auctions and created auctions
    var doc = document.getElementById('won_auctions');
    var html2Add = '';
    doc.innerHTML = "<h1>Closed Auctions</h1>";
    for (const auction of json_obj["Won Auctions"])
        html2Add += chat2AuctionHTML(auction, "won");
        doc.innerHTML += html2Add;
    
    
};

function chat2AuctionHTML(auctionJSON, calling_funct) {
    const itemName = auctionJSON.title
    const category = auctionJSON.category;
    const highestBid = auctionJSON.highestBid;
    const imageName = auctionJSON.imageUrl;
    const auction_id = String(auctionJSON._id);
    let hoursRemaing = auctionJSON.timeLeft;
    const startingPrice = auctionJSON.startingPrice;
    if(calling_funct === "won") {
        hoursRemaing = "  Auction Ended";
    }
    const description = auctionJSON.description;
    const username = auctionJSON.username;
    let auctionHTML =
    "<div class='auction' id='auction_" + auction_id + "'>" +
    "<p class='auction-id'>id: <span>" + auction_id + "</span></p>" +
    "<img class='image' src='../image/auction_images/" + imageName + "' alt='item image'>" +
    "<h2>" + itemName + "</h2>" +
    "<p>" + description + "</p>" +
    "<p>Starting Price: $" + startingPrice + "</p>" +
    "<p>Highest Bid: $" + highestBid + "</p>" +
    "<p>Time Left: " + hoursRemaing + "</p>" +
    "</div>";

    return auctionHTML;
}


