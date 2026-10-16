const avatarDivElement = document.getElementById("avatar");
const avatarButtonElement = document.getElementById("avatar-button");

avatarButtonElement.addEventListener("click", () => {
  avatarDivElement.classList.toggle("hidden");
});
