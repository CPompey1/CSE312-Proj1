let welcomeUserInterval;

function welcome_user() {
    updateAuctions("");
    welcomeUserInterval = setInterval(function () {
        updateAuctions("");
    }, 2000);
}

function welcome_to_profile(){

}

function stopGetHistoryInterval() {
    clearInterval(welcomeUserInterval);
}

function updateAuctions(category) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearAuctions();
            const auctions = JSON.parse(this.response);
            console.log(this.response)
            for (const auction of auctions) {
                addAuctiontoPage(auction);
            }
        }
    };
    if (category !== "") {
        request.open("GET", "/post-history/" + category);
    } else {
        request.open("GET", "/post-history");
    }
    request.send();
}

function chatAuctionHTML(auctionJSON) {
    const itemTitle = auctionJSON.item_title
    const itemDescription = auctionJSON.item_description;
    const highestBid = auctionJSON.highest_bid;
    const auctionEnd = auctionJSON.auction_end;
    const auction_id = String(auctionJSON._id);
    const image_name = auction_id + ".jpg"

    let auctionHTML = "<div class='auction' id='auction_" + auction_id + "'>" +
    "<div><img src='public/image/auction_images/" + image_name + "' alt='item image' class='my_image'/></div>" +
    "<div class='post-header'>" +
        "<b class='item-name'>" + itemTitle + "</b>" +
    "</div>" +
//need image
    "<div class='post-content'>" +
         "<div class='post-category'><b>Description: " + itemDescription + "</b></div>" +
        "<div class='post-cur-bid'><b>Highest Bid: " + highestBid + "</b></div>" +
         "<div class='post-end-time'><b>Auction End: " + auctionEnd + "</b></div>" +

    "</div>" +
    "<div class='post-actions'>" +
        "<button class='place-bid' id ='place_bid_" + auction_id + "'>Place Bid</button>" +
        "</div>" +
    "</div>";


    return auctionHTML;
}

function addAuctiontoPage(auctionJSON) {
    const chatMessages = document.getElementById("post-auctions");
    chatMessages.innerHTML += chatAuctionHTML(auctionJSON);
}

function clearAuctions() {
    const chatMessages = document.getElementById("post-auctions");
    chatMessages.innerHTML = "";
}
function redirectProfile() {
stopGetHistoryInterval(); // Stop the interval before navigating
window.location.href = 'http://localhost:8080/profile';
}
function redirectHome() {
window.location.href = 'http://localhost:8080/';
}