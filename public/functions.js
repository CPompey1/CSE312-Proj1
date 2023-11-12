// let welcomeUserInterval;

function welcome_user() {
    updateAuctions("");
    welcomeUserInterval = setInterval(function () {
        updateAuctions("");
    }, 2000);

}

function refresh_auctions(){

}
function updateAuctions(category) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearAuctions();
            const auctions = JSON.parse(this.response);
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

function updateThisAuctions(category) {
    clearInterval(welcomeUserInterval);
    updateAuctions(category);
    welcomeUserInterval = setInterval(function () {
        updateAuctions(category);
    }, 2000);
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
    // chatMessages.scrollIntoView(false);
    // chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function clearAuctions() {
    const chatMessages = document.getElementById("post-auctions");
    chatMessages.innerHTML = "";
}

function toggleSidebar() {
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.getElementById('mainContent');

    if (sidebar.style.width === '250px') {
      sidebar.style.width = '0';
      mainContent.style.marginLeft = '0';
    } else {
      sidebar.style.width = '250px';
      mainContent.style.marginLeft = '250px';
    }
  }

  function redirect() {
    window.location.href = 'http://localhost:8080/new_page';
  }

    function redirectHome() {
    window.location.href = 'http://localhost:8080/';
    }

  function authenticate(){  
    const request = new XMLHttpRequest();
    console.log('Entering authenicate')
    request.open('GET', '/authenticate');
    request.onload = () => {
    if (request.status === 200) {
        const data = JSON.parse(request.responseText);
        console.log(data);
        return data;
    } else {
        console.error('Request failed.  Returned status of ' + request.status);
    }
    };
    request.send();
    
    
    }
