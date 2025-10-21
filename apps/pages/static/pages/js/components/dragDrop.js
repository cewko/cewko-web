export function initDragAndDrop() {
  const widgets = document.querySelectorAll(
    ".left-bottom-column > .widget, .right-bottom-column > .widget, .right-bottom-column > .stats-row"
  );

  let draggedWidget = null;

  widgets.forEach((widget) => {
    const dragHandle = widget.querySelector(".widget-drag-handle");

    if (!dragHandle) return;

    const dragHandles = widget.classList.contains("stats-row")
      ? widget.querySelectorAll(".widget-drag-handle")
      : [dragHandle];

    dragHandles.forEach((handle) => {
      handle.addEventListener("mousedown", function (e) {
        widget.setAttribute("draggable", "true");
      });
    });

    widget.addEventListener("dragstart", function (e) {
      draggedWidget = this;
      this.classList.add("dragging");
      e.dataTransfer.effectAllowed = "move";
    });

    widget.addEventListener("dragend", function (e) {
      this.classList.remove("dragging");
      this.setAttribute("draggable", "false");
      
      widgets.forEach((w) => w.classList.remove("drag-over"));
    });

    widget.addEventListener("dragover", function (e) {
      e.preventDefault();
      if (draggedWidget !== this) {
        this.classList.add("drag-over");
      }
      return false;
    });

    widget.addEventListener("dragleave", function (e) {
      this.classList.remove("drag-over");
    });

    widget.addEventListener("drop", function (e) {
      e.stopPropagation();
      this.classList.remove("drag-over");

      if (draggedWidget !== this) {
        const parent1 = draggedWidget.parentNode;
        const parent2 = this.parentNode;
        const next1 = draggedWidget.nextSibling;
        const next2 = this.nextSibling;

        parent2.insertBefore(draggedWidget, next2);
        parent1.insertBefore(this, next1);
      }

      return false;
    });
  });
}