// On window load/document ready, enable image overlay
window.addEventListener("load", () => {
  enableImageOverlay();
});

function enableImageOverlay() {
// Set up image overlay when hovering over image

  // Style "edit" button
  const editText = document.getElementById("edit_text")
  editText.style.backgroundColor = "#14b8a6"
  editText.style.color = "#292524"
  editText.style.fontWeight = "bold"
  editText.style.fontSize = "1rem"
  editText.style.padding = "1rem 2rem"
  editText.style.cursor = "pointer"

  // Move edit button to correct location
  const editButton = document.getElementById("edit_button")
  editButton.style.opacity = "0"
  editButton.style.position = "absolute"
  editButton.style.top = "50%"
  editButton.style.left = "50%"
  editButton.style.transform = "translate(-50%, -350%)"

  const imageContainer = document.getElementById("image_container")
  const profileImage = document.getElementById("profile_image")

  // Make sure cancel and confirm buttons are hidden
  const cancelConfirm = document.getElementById("image_cancel_confirm")
  cancelConfirm.classList.add("hidden")

  // Add event listener when hovering over image - add opacity to image
  imageContainer.addEventListener("mouseover", () => {
    profileImage.style.opacity = "0.3"
    editButton.style.opacity = "1"
  })

  // Add event listener when stop hovering over image - remove opacity from image
  imageContainer.addEventListener("mouseout", () => {
    profileImage.style.opacity = "1"
    editButton.style.opacity = "0"
  })

  // Add event listener when hovering over edit button - change color
  editText.addEventListener("mouseover", () => {
    editText.style.backgroundColor = "#db2778"
    editText.style.transition = ".5 ease"
  });

  // Add event listener when stop hovering over edit button - change color
  editText.addEventListener("mouseout", () => {
    editText.style.backgroundColor = "#14b8a6"
    editText.style.transition = ".5 ease"
  });

  // Add event listener when clicking edit button
  editButton.addEventListener("click", () => {
    console.log("Edit...")
    document.getElementById('profile_image').click();
  });
  
//   disableImageOverlay()
  }

function disableImageOverlay() {
// Remove image overlay and add event listener to choose image

  // Remove all event listeners when hovering over image
  const imageContainer = document.getElementById("image_container")
  imageContainer.removeEventListener("mouseover", () => {})
  imageContainer.removeEventListener("mouseout", () => {})
  imageContainer.removeEventListener("click", () => {})

  // Revert to basic styling
  const profileImage = document.getElementById("profile_image")
  const editButton = document.getElementById("edit_button")
  const editText = document.getElementById("edit_text")
  profileImage.style.opacity = "1"
  editButton.style.opacity = "0"
  editText.style.cursor = "default"
  editText.style.opacity = "0"

  // Prevent image from doing anything when clicked
  profileImage.addEventListener("click", (e) => {
    e.preventDefault();
  });

  // Display cancel and confirm buttons
  const cancelConfirm = document.getElementById("image_cancel_confirm")
  cancelConfirm.classList.remove("hidden")
  cancelConfirm.classList.add("flex")
  cancelConfirm.classList.add("flex-row")
  cancelConfirm.classList.add("justify-evenly")

  // Add event listener to checkmark/confirm button
  const checkmark = document.getElementById("confirm")
  checkmark.addEventListener("click", () => {
    console.log("Confirm...")
  })

  // Add event listener to cancel button - just reload page
  const cancel = document.getElementById("cancel")
  cancel.addEventListener("click", () => {
    window.location.reload();
  })
}
