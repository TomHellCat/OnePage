
let chatSocket
let roomId = ""
let userName = ""
function scrollToBottom(){
	let chatDiv = document.getElementById("chat");
    chatDiv.scrollTop = chatDiv.scrollHeight;
}

chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url
    
    let param = 'http://127.0.0.1:8000/chats/' + url

    var roomId = ""
    var userName = ""
    //fetch('http://127.0.0.1:8000/chats/https://protonmail.com/')
    fetch(param)
    .then((response) => {
        return response.json()
    }).then((data) =>{
    	if(data.length > 2){
    		roomId = data[3]['id']
		    userName = data[1]['user']
		    
		    let chatDiv = document.getElementById('chat')
		    for(let i = 0; i<data[0]['message'].length; i++){
		    	
		    	let rowDiv = document.createElement('div')
		    	rowDiv.className = "row"
		    	let cardDiv = document.createElement('div')
		    	cardDiv.class = "card blue me"
		    	let senderDiv = document.createElement('div')
		    	senderDiv.class = "right sender"
		    	let contentDiv = document.createElement('div')
		    	let timeDiv = document.createElement('div') 
		    	timeDiv.className = "time"
		    	if(userName == data[4]['users'][i]){
		    		cardDiv.className = "card blue me"
		    		senderDiv.className = "right sender"
		    		senderDiv.innerHTML = "You"
		    	}else{
		    		cardDiv.className = "card green her"
		    		senderDiv.className = "left sender"
		    		senderDiv.innerHTML = data[4]['users'][i]
		    	}
		    	contentDiv.innerHTML = data[0]['message'][i]
		    	timeDiv.innerHTML = data[2]['time'][i].slice(11,16)
		    	cardDiv.append(senderDiv)
		    	cardDiv.append(contentDiv)
		    	cardDiv.append(timeDiv)
		    	rowDiv.append(cardDiv)
		    	chatDiv.append(rowDiv)
		    	scrollToBottom()
		    }
		    chatSocket = new WebSocket('ws://127.0.0.1:8000/ws/'+roomId+'/')
		    chatSocket.onmessage = function(e) {
                    const data = JSON.parse(e.data);
                    if (data.message) {
                        let chatDiv = document.getElementById('chat')
                        let rowDiv = document.createElement('div')
						rowDiv.className = "row"
						let cardDiv = document.createElement('div')
						cardDiv.class = "card blue me"
						let senderDiv = document.createElement('div')
						senderDiv.class = "right sender"
						let contentDiv = document.createElement('div')
						let timeDiv = document.createElement('div') 
						timeDiv.className = "time"
						if(userName == data.user){
							cardDiv.className = "card blue me"
							senderDiv.className = "right sender"
							senderDiv.innerHTML = "You"
						}else{
							cardDiv.className = "card green her"
							senderDiv.className = "left sender"
							senderDiv.innerHTML = data.user
						}
						contentDiv.innerHTML = data.message
						timeDiv.innerHTML = data.time.slice(11,16)
						cardDiv.append(senderDiv)
						cardDiv.append(contentDiv)
						cardDiv.append(timeDiv)
						rowDiv.append(cardDiv)
						chatDiv.append(rowDiv)
                    } else {
                        alert('The message is empty!');
                    }
                    scrollToBottom() 
                };
                document.querySelector('#chat-message-input').focus();
                document.querySelector('#chat-message-input').onkeyup = function(e) {
                    if (e.keyCode === 13) {  // enter, return
                        document.querySelector('#chat-message-submit').click();
                    }
                };
                chatSocket.onclose = function(e) {
                    console.log('The socket close unexpectadly');
                };
        		document.querySelector('#chat-message-submit').onclick = function(e) {
				const messageInputDom = document.querySelector('#chat-message-input')
				const message = messageInputDom.value
				chatSocket.send(JSON.stringify({
					'message': message,
					'username': userName,                   
					'room': roomId                                    
				}));
				messageInputDom.value = ''                    
			};
    	}else{
			var newURL = "http://127.0.0.1:8000/";
       		chrome.tabs.create({ url: newURL });
    	} 
    })    
});






