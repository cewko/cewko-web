export function initRecentTooltips() {
  const recentWidgets = document.querySelectorAll(".recent-widget");

  recentWidgets.forEach((widget) => {
    const content = widget.querySelector(".recent-content");
    const author = widget.querySelector(".recent-author");
    const description = widget.querySelector(".recent-description");
    const link = widget.querySelector(".recent-link");

    const tooltip = document.createElement("div");
    tooltip.className = "recent-tooltip";
    content.appendChild(tooltip);

    function isOverflowing(element) {
      return (
        element.scrollHeight > element.clientHeight ||
        element.scrollWidth > element.clientWidth
      );
    }

    function showTooltip(element, text) {
      tooltip.textContent = text;
      tooltip.classList.add("show");

      const rect = element.getBoundingClientRect();
      const containerRect = content.getBoundingClientRect();
      
      tooltip.style.left = rect.left - containerRect.left + rect.width / 2 + "px";
      tooltip.style.bottom = containerRect.bottom - rect.top + 8 + "px";
      tooltip.style.transform = "translateX(-50%)";
    }

    function hideTooltip() {
      tooltip.classList.remove("show");
    }

    if (link && isOverflowing(author)) {
      author.style.cursor = "pointer";

      author.addEventListener("mouseenter", () => {
        showTooltip(author, author.textContent);
      });

      author.addEventListener("mouseleave", hideTooltip);
    }

    if (isOverflowing(description)) {
      description.style.cursor = "pointer";

      description.addEventListener("mouseenter", () => {
        showTooltip(description, description.textContent);
      });

      description.addEventListener("mouseleave", hideTooltip);
    }
  });
}