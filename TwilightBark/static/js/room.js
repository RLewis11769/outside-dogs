window.addEventListener("load", () => {
  // On load, add frontend websocket connection

  // Get room name based on URL
  const roomName = JSON.parse(document.getElementById('room-name').textContent);
  // Websocket URL starts with ws:// if unsecured or wss:// if secured through https
  const ws = window.location.protocol == "https:" ? "wss://" : "ws://";
  // Websocket endpoint pattern shown in routing.py - ws/chat/<room_name> - not in URL
  const endpoint = `${ws}${window.location.host}/ws/chat/${roomName}/`;
  const socket = new WebSocket(endpoint);

  socket.onmessage = (e) => {
    // Parse data coming back from server and direct to correct function
    const data = JSON.parse(e.data);
    // console.log(data)
    if (data.msg_type == "join") {
      // If new user joined, add welcome message to notify other users and update user count
      if (data.user)
        addMessage(data.user, "joined");
      countUsers(data.count)
    } else if (data.msg_type == "leave") {
      // If user left, notify other chat members and update user count
      if (data.user)
        addMessage(data.user, "left");
      countUsers(data.count)
    } else if (data.msg_type == "message") {
      // If new message, add to chat log DOM
      addToDOM(data, 0);
    } else if (data.msg_type == "error") {
      // If error, log error message but don't add to DOM
      console.log(data.error);
    } else if (data.type == "load_messages") {
      // Note! This only happens to one user at a time
      // When first load page, add message backload from db to DOM
      handleMessagesBacklog(data.messages);
      // Page number will never update automatically but will on first load
      setPageNumber(data.pageNum);
    }
  }

  // Focus on input field when page loads
  document.querySelector('#chat-message-input').focus();

  document.querySelector('#chat-message-input').onkeyup = (e) => {
    // Allow for "Enter" key to submit message
    if (e.keyCode === 13)
      document.querySelector('#chat-message-submit').click();
  };

  document.querySelector('#chat-message-submit').onclick = (e) => {
    // When user clicks submit button or enter, send message to server
    const inputField = document.querySelector('#chat-message-input');
    const message = inputField.value;
    socket.send(JSON.stringify({
      'message': message
    }));
    // Clear input field
    inputField.value = '';
  };

  function addMessage(username, status) {
    // When user status message comes back from server, add to DOM
    // Create div with joined/left message, and add div to chat log
    const chatLog = document.getElementById("chat_log")
    const messageDiv = document.createElement("div")
    const usernameSpan = document.createElement("p")
    usernameSpan.innerHTML = `${username} ${status}`
    messageDiv.classList.add("m-3")
    messageDiv.appendChild(usernameSpan)
    chatLog.appendChild(messageDiv)
  }

  function addToDOM(data, backlog) {
    // When message comes back from server, add to DOM
    msg = data['message']
    username = `${data.user} `
    timestamp = data['timestamp']
    pic_url = data.pic

    // Create div with message and details about message, and add to chat log
    const chatLog = document.getElementById("chat_log")
    const mainDiv = document.createElement("div")
    mainDiv.classList.add("flex", "flex-row", "items-center", "m-3")
    const picDiv = document.createElement("div")
    const pic = document.createElement("img")
    // If loading multiple images at once, set default pic, then replace later
    const defaultPic = "../../profile_images/default_pic.png"
    pic.src = backlog ? defaultPic : pic_url
    pic.classList.add("rounded-full", "border", "border-pink-500", "bg-stone-900", "h-12", "w-12", "object-cover", "object-center")
    const pic_id = `${data.id}`
    pic.setAttribute("id", pic_id)
    pic.setAttribute("alt", "User profile picture")
    picDiv.appendChild(pic)
    mainDiv.appendChild(picDiv)
    const messageDiv = document.createElement("div")
    const usernameSpan = document.createElement("span")
    usernameSpan.innerHTML = username
    messageDiv.appendChild(usernameSpan)
    const timeSpan = document.createElement("span")
    timeSpan.innerHTML = timestamp
    messageDiv.appendChild(timeSpan)
    const msg_tag = document.createElement("p")
    msg_tag.innerHTML = msg
    msg_tag.classList.add("font-normal")
    messageDiv.appendChild(msg_tag)
    messageDiv.classList.add("m-3")
    mainDiv.appendChild(messageDiv)
    chatLog.appendChild(mainDiv)

    if (backlog)
      preloadImage(pic_url, pic_id)
  }

  function countUsers(count) {
    // When user count comes back from server, update user count
    element = document.getElementById("user_count")
    element.innerHTML = count
  }

  function handleMessagesBacklog(messages) {
    // Load backlog/payload of messages from server to DOM
    if (messages) {
      messages.forEach((message) => {
        addToDOM(message, 1)
      });
    }
  }

  function setPageNumber(pageNumber) {
    // Add page number to DOM on first load
    document.getElementById("page_number").innerHTML = `Page ${pageNumber}`
  }

  
  function preloadCallback(src, elementId) {
    const img = document.getElementById(elementId)
    img.src = src
  }

  function preloadImage(imgSrc, elementId) {
    const objImagePreloader = new Image();
    objImagePreloader.src = imgSrc;
    if (objImagePreloader.complete) {
      preloadCallback(objImagePreloader.src, elementId);
      objImagePreloader.onload =  () => {};
    }
    else {
      objImagePreloader.onload = () => {
        preloadCallback(objImagePreloader.src, elementId);
        // Clear onload in case animated gifs or other weirdness
        objImagePreloader.onload=() => {};
      }
    }
  }
});