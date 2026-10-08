// 事例詳細ページ：写真をクリックで拡大表示（前へ／次へ／閉じる）
(function () {
  var tiles = Array.prototype.slice.call(document.querySelectorAll('#tiles .tile'));
  var lb = document.getElementById('lb');
  if (!tiles.length || !lb) return;
  var img = document.getElementById('lbImg'), count = document.getElementById('lbCount');
  var cur = 0;
  function show(i) {
    cur = (i + tiles.length) % tiles.length;
    img.src = tiles[cur].getAttribute('href');
    count.textContent = (cur + 1) + ' / ' + tiles.length;
    lb.hidden = false; document.body.style.overflow = 'hidden';
  }
  function close() { lb.hidden = true; img.src = ''; document.body.style.overflow = ''; }
  tiles.forEach(function (a, i) { a.addEventListener('click', function (e) { e.preventDefault(); show(i); }); });
  document.getElementById('lbClose').addEventListener('click', close);
  document.getElementById('lbPrev').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
  document.getElementById('lbNext').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  });
  var sx = null;
  lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null;
    if (dx > 50) show(cur - 1); else if (dx < -50) show(cur + 1);
  });
})();
