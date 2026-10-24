/* Centralized affiliate-link rendering. No account credentials or fabricated URLs. */
(async function () {
  const nodes = document.querySelectorAll('[data-partner-id]');
  if (!nodes.length) return;
  let data;
  try {
    const response = await fetch('./partners.json', {cache:'no-store'});
    if (!response.ok) return;
    data = await response.json();
  } catch (_) { return; }
  for (const node of nodes) {
    const id = node.getAttribute('data-partner-id');
    const entry = data.links && data.links[id];
    if (!entry || entry.enabled !== true || !entry.url) continue;
    let url;
    try { url = new URL(entry.url); } catch (_) { continue; }
    if (url.protocol !== 'https:') continue;
    node.href = url.href;
    node.target = '_blank';
    node.rel = 'sponsored nofollow noopener noreferrer';
    node.hidden = false;
    node.setAttribute('aria-label', (entry.label || 'Посмотреть предложение') + ' (партнёрская ссылка)');
    node.textContent = entry.label || 'Посмотреть предложение';
  }
})();