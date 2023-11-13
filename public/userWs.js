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
    var json_obj = JSON.parse(received_msg);
    var html2Add = '';
    //Update Created Auctions
    var doc = document.getElementById('created_auctions');
    doc.innerHTML = "<h1>Created Auctions</h1>";
    for (const auction of json_obj["Created Auctions"])
        html2Add += chat2AuctionHTML(auction);
        doc.innerHTML += html2Add;
    

    //add to won auctions and created auctions
    var doc = document.getElementById('won_auctions');
    var html2Add = '';
    doc.innerHTML = "<h1>Won Auctions</h1>";
    for (const auction of json_obj["Won Auctions"])
        html2Add += chat2AuctionHTML(auction);
        doc.innerHTML += html2Add;
    
    
};

function chat2AuctionHTML(auctionJSON) {
    const itemName = auctionJSON.title
    const category = auctionJSON.category;
    const highestBid = auctionJSON.highest_bid;
    const imageName = auctionJSON.imageUrl;
    const auction_id = String(auctionJSON._id);
    const hoursRemaing = auctionJSON.timeLeft;
    const description = auctionJSON.description;
    const username = auctionJSON.username;
    let auctionHTML = 
    "<div class='auction' id='auction_" + auction_id + "'>" +
        "<img src='public/image/auction_images/" + imageName + "' alt='item image'>" +
        "<h2>" + itemName + "</h2>" +
        "<p>Highest Bid: " + highestBid + "</p>" +
        "<p>Time Remaining:" + hoursRemaing+ "</p>" +
        "<p>" + description + "</p>" +
        "<form action='/place_bid' method='post' enctype='application/x-www-form-urlencoded'>" +
            "<label>Place Bid:" +
            "<input id='bid' type='text' name='bid'/>"+
            "<input type='submit' value='Place Bid'>" +
            "</label>" +
        "</form>" +
    "</div>";

    // <div class="auction">
    //             <img class="auction-image" src="auction_image1.jpg" alt="Auction Image 1">
    //             <h2>Auction Item Name 1</h2>
    //             <p>Highest Bid: $100</p>
    //             <p>Time Left: 2 days 12 hours</p>
    //             <form action="/place_bid" method="post" enctype="application/x-www-form-urlencoded">
    //                 <label>Place Bid:
    //                     <input id="bid" type="text" name="bid"/>
    //                     <input type="submit" value="Place Bid">
    //                 </label>
    //             </form>
    //         </div>

    return auctionHTML;
}


