// On window load/document ready, wait for user input to select room
window.addEventListener('load', () => {
  // Focus on room name input when page loads
  document.querySelector('#room-name-input').focus();

  document.querySelector('#room-name-input').onkeyup = (e) => {
    // Hitting enter is same as clicking submit button
    if (e.keyCode === 13)
      document.querySelector('#room-name-submit').click();
  };

  document.querySelector('#room-name-submit').onclick = (e) => {
    // Get room name from input field and send to URL
    const roomName = document.querySelector('#room-name-input').value;
    window.location.pathname = `/chat/${roomName}/`;
  };
});
