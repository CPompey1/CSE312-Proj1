// let welcomeUserInterval;



function welcome_user() {
    updateAuctions("");
    welcomeUserInterval = setInterval(function () {
        updateAuctions("");
    }, 2000);
}


function stopGetHistoryInterval() {
    clearInterval(welcomeUserInterval);
}


function stopGetHistoryInterval() {
    clearInterval(welcomeUserInterval);
}

function updateAuctions(category) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            // clearAuctions();
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

function verified() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const verified = JSON.parse(this.response);
            const emailVerification = document.getElementById("email_form");
            let verified_message = ""
            if(verified === true){
                verified_message = "Email Verified"
            }
            else{
                verified_message = "Email Not Verified" +
                "<div class='login_button'><input type='submit' value='Verify Email'></div>"
            }
            emailVerification.innerHTML += verified_message
        }
    };

    request.open("GET", "/verification_status");

    request.send();
}

function chatAuctionHTML(auctionJSON) {
    const itemTitle = auctionJSON.item_title
    const itemDescription = auctionJSON.item_description;
    const highestBid = "Highest Bid: $" + auctionJSON.highest_bid;
    const auctionEnd = auctionJSON.auction_end;
    const auction_id = String(auctionJSON._id);
    const image_name = auction_id + ".jpg"
    const timeLeft = auctionJSON.auction_end;
    const isOver = auctionJSON.isOver;
    const winner = auctionJSON.winner;

    let auctionHTML = "<div class='auction' id='auction_" + auction_id + "'>" +
        "<div><img src='public/image/auction_images/" + image_name + "' alt='item image' class='image'/></div>" +
        "<div class='post-header'>" +
        "<b class='item-name'>Item: " + itemTitle + "</b>" +
        "</div>" +
        "<div class='post-content'>" +
        "<b><div class='post-category'>Description: " + itemDescription + "</div></b>" +
        "<b><div class='post-cur-bid'> " + highestBid + "</div></b>" +
        "</div>" +
        "<div class='countdown' id='countdown_" + auction_id + "'>Time left: <span id='timer_" + auction_id + "'>" + timeLeft + "</span></div>" +

        "</div>";

    return auctionHTML;
}

function showBidDropdown(auctionid) {
    stopGetHistoryInterval()
    const bidDropdown = document.getElementById('bidDropdown_' + auctionid);
    bidDropdown.style.display = 'block';
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
    window.location.href = 'http://sniffandbid.me/profile';
}
function redirectHome() {
    window.location.href = 'http://sniffandbid.me/';
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

function redirectClosedAuctions() {
    window.location.href = 'http://sniffandbid.me/closed_auctions';
}
function redirectAuctionsWon() {
    window.location.href = 'http://sniffandbid.me/';
}
function redirectCreateAuction() {
    window.location.href = 'http://sniffandbid.me/profile';
}

function redirectHome() {
    window.location.href = 'http://sniffandbid.me/';
}


function authenticate(){  
    const request = new XMLHttpRequest();
    var data;
    // console.log('Entering authenicate')
    request.open('GET', '/authenticate',false);
    request.onload = () => {
    if (request.status === 200) {
        data = JSON.parse(request.responseText);
        console.log(data);
        return data;
    } else {
        console.error('Request failed.  Returned status of ' + request.status);
    }
    };
    request.send();
    return JSON.stringify(data);
    }
