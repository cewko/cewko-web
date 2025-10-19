function initRecentTooltips() {
  const recentWidgets = document.querySelectorAll(".recent-widget");

  recentWidgets.forEach((widget) => {
    const content = widget.querySelector(".recent-content");
    const author = widget.querySelector(".recent-author");
    const description = widget.querySelector(".recent-description");
    const link = widget.querySelector(".recent-link");

    // Create tooltip
    const tooltip = document.createElement("div");
    tooltip.className = "recent-tooltip";
    content.appendChild(tooltip);

    // Check if element overflows
    function isOverflowing(element) {
      return (
        element.scrollHeight > element.clientHeight ||
        element.scrollWidth > element.clientWidth
      );
    }

    // Author tooltip - only if it's a link or overflows
    if (link && isOverflowing(author)) {
      author.style.cursor = "pointer";

      author.addEventListener("mouseenter", (e) => {
        tooltip.textContent = author.textContent;
        tooltip.classList.add("show");

        const rect = author.getBoundingClientRect();
        const containerRect = content.getBoundingClientRect();
        tooltip.style.left =
          rect.left - containerRect.left + rect.width / 2 + "px";
        tooltip.style.bottom = containerRect.bottom - rect.top + 8 + "px";
        tooltip.style.transform = "translateX(-50%)";
      });

      author.addEventListener("mouseleave", () => {
        tooltip.classList.remove("show");
      });
    }

    // Description tooltip - only if overflows
    if (isOverflowing(description)) {
      description.style.cursor = "pointer";

      description.addEventListener("mouseenter", (e) => {
        const fullText = description.textContent;
        tooltip.textContent = fullText;
        tooltip.classList.add("show");

        const rect = description.getBoundingClientRect();
        const containerRect = content.getBoundingClientRect();
        tooltip.style.left =
          rect.left - containerRect.left + rect.width / 2 + "px";
        tooltip.style.bottom = containerRect.bottom - rect.top + 8 + "px";
        tooltip.style.transform = "translateX(-50%)";
      });

      description.addEventListener("mouseleave", () => {
        tooltip.classList.remove("show");
      });
    }
  });
}

function updateTime() {
  const now = new Date();

  const polandTime = new Intl.DateTimeFormat("en-US", {
    timeZone: "Europe/Warsaw",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(now);

  const timeElement = document.querySelector(".weather-stats div:first-child");
  if (timeElement) {
    timeElement.textContent = `: Time: ${polandTime}`;
  }
}

updateTime();
setInterval(updateTime, 60000);
initRecentTooltips();
