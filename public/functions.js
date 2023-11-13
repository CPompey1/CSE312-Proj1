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
    const itemName = auctionJSON.item_name
    const category = auctionJSON.category;
    const highestBid = auctionJSON.highest_bid;
    const imageName = auctionJSON.image_name;
    const auction_id = String(auctionJSON._id);
    let auctionHTML = "<div class='auction' id='auction_" + auction_id + "'>" +
    "<div><img src='public/image/auction_images/" + imageName + "' alt='item image' class='my_image'/></div>" +
    "<div class='post-header'>" +
        "<b class='item-name'>" + itemName + "</b>" +
    "</div>" +
//need image
    "<div class='post-content'>" +
        "<b <div class='post-category'>Category: " + category + "</div> </b>" +
        "<b <div class='post-cur-bid'>Highest Bid: " + highestBid + "</div> </b>" +
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

function openPopup() {
    document.getElementById("popupContainer").style.display = "block";
    document.getElementById("overlay").style.display = "block";
}

function closePopup() {
    document.getElementById("popupContainer").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

function sendPostRequest() {
    // Get form data
    var formData = new FormData(document.getElementById("myForm"));

    // Perform your POST request here
    fetch('your_server_endpoint', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server
        console.log(data);
        // Optionally, close the popup after a successful request
        closePopup();
    })
    .catch(error => console.error('Error:', error));
}