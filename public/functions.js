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
    chatMessages.innerHTML += chatMessageHTML(messageJSON);
    chatMessages.scrollIntoView(false);
    chatMessages.scrollTop = chatMessages.scrollHeight - chatMessages.clientHeight;
}

function clearPosts() {
    const chatMessages = document.getElementById("post-messages");
    chatMessages.innerHTML = "";
}