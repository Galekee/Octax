(() => {
  let theme;
  try { theme = localStorage.getItem('octax-theme'); } catch (_) {}
  if (!['light', 'dark'].includes(theme)) theme = 'light';
  document.documentElement.dataset.theme = theme;
})();
