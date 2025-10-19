function checkCreditsCollision() {
  const credits = document.querySelector(".credits");
  const mainContainer = document.querySelector(".main-container");

  if (!credits || !mainContainer) return;

  const creditsRect = credits.getBoundingClientRect();
  const containerRect = mainContainer.getBoundingClientRect();

  // Check if credits overlap with main container
  const isColliding = !(
    creditsRect.right < containerRect.left ||
    creditsRect.left > containerRect.right ||
    creditsRect.bottom < containerRect.top ||
    creditsRect.top > containerRect.bottom
  );

  if (isColliding) {
    credits.style.opacity = "0";
    credits.style.pointerEvents = "none";
  } else {
    credits.style.opacity = "1";
    credits.style.pointerEvents = "auto";
  }
}

checkCreditsCollision();
window.addEventListener("resize", checkCreditsCollision);
window.addEventListener("scroll", checkCreditsCollision);
