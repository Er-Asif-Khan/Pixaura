// theme.js
(() => {
  const KEY = 'theme';
  const html = document.documentElement;

  const setButtonUI = (btn, t) => {
    if (!btn) return;
    btn.setAttribute('aria-pressed', String(t === 'dark'));
    btn.textContent = t === 'light' ? '☀️' : '🌙';
    btn.title = t === 'light' ? 'Switch to dark' : 'Switch to light';
  };

  const applyTheme = (t, { save = true } = {}) => {
    html.dataset.theme = t;
    html.style.colorScheme = t;
    html.classList.toggle('light-mode', t === 'light');
    if (document.body) document.body.classList.toggle('light-mode', t === 'light');
    if (save) localStorage.setItem(KEY, t);
    setButtonUI(document.getElementById('themeToggle'), t);
  };

  document.addEventListener('DOMContentLoaded', () => {
    const current = html.dataset.theme || localStorage.getItem(KEY) || 'dark';
    applyTheme(current, { save: false });

    const btn = document.getElementById('themeToggle');
    if (btn) {
      btn.addEventListener('click', () => {
        const next = (html.dataset.theme === 'dark') ? 'light' : 'dark';
        applyTheme(next, { save: true });
      });
    }
  });

  // Sync across tabs/windows without causing loops
  window.addEventListener('storage', (e) => {
    if (e.key === KEY && e.newValue) {
      applyTheme(e.newValue, { save: false });
    }
  });
})();
