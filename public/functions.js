function welcome_user() {
    request_username();
    updatePosts();
    setInterval(updatePosts, 2000);
}

function sendPost() {
    const title = document.getElementById("title_input").value
    const description = document.getElementById("description_input").value
    
    if(title == ""){
        alert("title required")
        return
    }

    if(description == ""){
        alert("description required")
        return
    }

    message = {"title": title, "description": description}
    console.log(message)
    
    const request = new XMLHttpRequest();
    console.log(request)
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
        }
    }
    request.open("POST", "/post-message");
    request.setRequestHeader("Content-Type","application/json")
    request.send(JSON.stringify(message));

    document.getElementById("title_input").value = ""
    document.getElementById("description_input").value = ""
}


function request_username(){
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            console.log(this.response);
            payload = JSON.parse(this.response)
            console.log(payload.username)
            document.getElementById("paragraph").innerHTML = "<br/>Hello " + payload.username
            return 
        }
    }
    request.open("GET", "/username");
    request.send();
}

function updatePosts() {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            clearPosts();
            const messages = JSON.parse(this.response);
            for (const message of messages) {
                addPostToChat(message);
            }
        }
    }
    request.open("GET", "/post-history");
    request.send();
}

function addPostToChat(messageJSON) {
    const chatMessages = document.getElementById("post-messages");
    chatMessages.innerHTML += chatPostHTML(messageJSON);
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function chatPostHTML(messageJSON) {
    const username = messageJSON.username;
    const title = messageJSON.title
    const description = messageJSON.description;
    const messageId = messageJSON.id;
    let messageHTML = "<br><button onclick='likeMessage(\"" + messageId + "\")'>" +
        "<img src=\"public/image/white_heart.jpg\" width='25' height='auto' id='heart' class=\"my_image\"/></button> ";
    messageHTML += "<span id='message_" + messageId + "'><b>" + username + "</b> " + "<div>" + title + "</div>" + description + "</span>";
    return messageHTML;
}

function clearPosts() {
    const chatMessages = document.getElementById("post-messages");
    chatMessages.innerHTML = "";
}

function likeMessage(messageId){
    const request = new XMLHttpRequest();
    console.log("It's entering thr function");                                           // print was never seen, request is sent tho
    if(document.getElementById('heart').src=== "image/white_heart.jpg"){        // heart image never gets changed
        document.getElementById('heart').src = "image/red_heart.jpg";
    }else{
        document.getElementById('heart').src= "image/white_heart.jpg";
    }
    request.open("POST", "/like");
    request.setRequestHeader("Content-Type","application/json")
    request.send(JSON.stringify(messageId));
}