document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.comment-toggle').forEach(button => button.addEventListener('click', () => {
    const section = document.getElementById(button.dataset.target);
    if (!section) return;
    const open = section.classList.toggle('open');
    button.setAttribute('aria-expanded', String(open));
    if (open) section.querySelector('input[name="text"]')?.focus();
  }));
  document.querySelectorAll('form[data-confirm]').forEach(form => form.addEventListener('submit', event => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  }));
  document.querySelectorAll('.message').forEach(message => setTimeout(() => message.classList.add('fade'), 4500));
  document.querySelectorAll('.postimage').forEach(image => image.addEventListener('error', () => image.style.display = 'none'));
});
