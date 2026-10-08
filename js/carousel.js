// トップページ：事例の横スライド（矢印ボタン／横スクロール／スワイプ）
(function () {
  var track = document.getElementById('track');
  if (!track) return;
  function step() { var s = track.querySelector('.slide'); return s ? s.getBoundingClientRect().width + 16 : 320; }
  document.querySelector('.carousel-btn.prev').addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
  document.querySelector('.carousel-btn.next').addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
})();
