const algorithmSelect = document.querySelector('#algorithmSelect');
const keyGroups = document.querySelectorAll('.key-group');
const themeToggle = document.querySelector('#themeToggle');
const html = document.documentElement;

function showKeyGroup() {
  const selected = algorithmSelect.value;
  keyGroups.forEach(group => {
    group.classList.toggle('active', group.dataset.key === selected);
  });
}

function applyTheme(theme) {
  html.setAttribute('data-bs-theme', theme);
  localStorage.setItem('theme', theme);
  themeToggle.textContent = theme === 'dark' ? '☾' : '☀';
}

algorithmSelect?.addEventListener('change', showKeyGroup);
showKeyGroup();

const savedTheme = localStorage.getItem('theme') || 'dark';
applyTheme(savedTheme);

themeToggle?.addEventListener('click', () => {
  const nextTheme = html.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark';
  applyTheme(nextTheme);
});

document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    await navigator.clipboard.writeText(button.dataset.copy || '');
    const oldText = button.textContent;
    button.textContent = 'Tersalin';
    setTimeout(() => button.textContent = oldText, 1200);
  });
});

const clearHistoryBtn = document.querySelector('#clearHistory');
clearHistoryBtn?.addEventListener('click', async () => {
  await fetch('/clear-history', { method: 'POST' });
  window.location.reload();
});

(() => {
  'use strict';
  const forms = document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });
})();
