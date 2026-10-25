const details = document.querySelector('aside details');
if (matchMedia('(max-width:650px)').matches) details.open = false;
const sizes = [19, 21, 23];
let size = 0;
document.querySelector('#size').addEventListener('click', () => {
  size = (size + 1) % sizes.length;
  document.documentElement.style.setProperty('--reading', `${sizes[size]}px`);
});
const zoom = document.querySelector('#zoom');
document.querySelectorAll('article img').forEach(img => img.addEventListener('click', () => {
  zoom.querySelector('img').src = img.src;
  zoom.querySelector('img').alt = img.alt;
  zoom.showModal();
}));
document.querySelector('#close-zoom').addEventListener('click', () => zoom.close());
zoom.addEventListener('click', e => { if (e.target === zoom) zoom.close(); });
let searchIndex;
let generation = 0;
document.querySelector('#search').addEventListener('input', async e => {
  const current = ++generation;
  const q = e.target.value.trim().toLowerCase();
  const results = document.querySelector('#results');
  results.replaceChildren();
  document.querySelector('#chapters').hidden = !!q;
  if (!q) return;
  try {
    searchIndex ||= fetch(new URL('search.json', document.querySelector('script[src$="app.js"]').src)).then(r => {
      if (!r.ok) throw new Error('search');
      return r.json();
    });
    const entries = await searchIndex;
    if (current !== generation) return;
    const found = entries.filter(c => (c.title + c.text).toLowerCase().includes(q));
    found.forEach(c => {
      const a = document.createElement('a');
      a.href = c.url; a.textContent = c.title;
      const snippet = document.createElement('small');
      const at = Math.max(0, c.text.toLowerCase().indexOf(q) - 18);
      snippet.textContent = c.text.slice(at, at + 95) + '…';
      a.append(snippet); results.append(a);
    });
    if (!found.length) results.textContent = '没有找到相关章节';
  } catch {
    if (current === generation) results.textContent = '搜索暂不可用，请使用目录';
    searchIndex = undefined;
  }
});
