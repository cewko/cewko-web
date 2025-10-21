import { initRecentTooltips } from '../components/tooltips.js';
import { initClock } from '../components/clock.js';
import { initDragAndDrop } from '../components/dragDrop.js';

document.addEventListener('DOMContentLoaded', () => {
  initRecentTooltips();
  initClock();
  initDragAndDrop();
});