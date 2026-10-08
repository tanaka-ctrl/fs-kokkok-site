// お問い合わせ：相談内容に応じて質問を出し分け、入力内容をメール本文にまとめる
(function () {
  var MAIL = 'info@fs-kokkok.com';
  var form = document.getElementById('cform');
  var type = document.getElementById('f-type');
  var extras = Array.prototype.slice.call(document.querySelectorAll('.extra'));
  var msg = document.getElementById('formMsg');

  var common = document.getElementById('commonFields'), rest = document.getElementById('restFields');
  function updateExtras() {
    extras.forEach(function (fs) {
      var on = fs.getAttribute('data-for').split(' ').indexOf(type.value) !== -1;
      fs.hidden = !on;
    });
    var cnc = type.value === 'CNC加工';
    common.hidden = cnc; rest.hidden = cnc;
  }
  type.addEventListener('change', updateExtras); updateExtras();

  var same = document.getElementById('f-sameaddr'), site = document.getElementById('f-site'), ship = document.getElementById('f-ship');
  function syncShip() { if (same.checked) { ship.value = site.value; ship.readOnly = true; } else { ship.readOnly = false; } }
  same.addEventListener('change', syncShip); site.addEventListener('input', syncShip);

  function val(id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; }
  function line(label, id) { var v = val(id); return label + '：' + v; }

  function validate() {
    var missing = [];
    if (!type.value) missing.push('ご相談内容');
    if (!val('f-name')) missing.push('お名前');
    if (!val('f-tel')) missing.push('電話番号');
    if (missing.length) { msg.hidden = false; msg.textContent = '次の項目をご記入ください：' + missing.join('、'); return false; }
    msg.hidden = true; return true;
  }

  function build() {
    var t = type.value;
    var L = ['【ご相談内容】' + t, '',
      line('会社名', 'f-company'), line('お名前', 'f-name'), line('電話番号', 'f-tel'), line('メール', 'f-mail'), '',
      line('現場住所', 'f-site'), line('送付先住所', 'f-ship') + (same.checked ? '（現場と同じ）' : ''), ''];
    if (t === 'オーダー家具・什器') {
      L.push('【家具・什器について】', line('使う場所', 'f-use'), line('納品・オープン予定', 'f-open'), line('設計者・施工会社', 'f-designer'), line('図面・参考画像', 'f-drawing'), line('製作したいもの', 'f-items'), '');
    } else if (t === '試作・開発' || t === 'OEM・小ロット生産') {
      L.push('【製品について】', line('概要', 'f-product'), line('数量', 'f-lot'), line('データ', 'f-data'), line('量産の予定', 'f-massprod'), line('開発完了の目安', 'f-devdue'), '');
    } else if (t === '家具のリペア・張り替え') {
      L.push('【リペア・張り替えについて】', line('品目', 'f-ritem'), line('メーカー・購入時期', 'f-rmaker'), line('状態・困っていること', 'f-rstate'), '');
    } else if (t === 'デザイン相談') {
      L.push('【ご相談について】', line('相談したいこと', 'f-dtheme'), line('現在の段階', 'f-dstage'), line('希望時期', 'f-dwhen'), '');
    }
    L.push(line('ご予算', 'f-budget'), line('ご希望納期', 'f-due'), '', '【詳細・ご質問】', val('f-detail'));
    return L.join('\n');
  }
  function subject() { return '【お問い合わせ】' + (type.value || '什器・家具') + (val('f-company') ? '／' + val('f-company') : ''); }

  document.getElementById('mailBtn').addEventListener('click', function () {
    if (!validate()) return;
    window.location.href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(subject()) + '&body=' + encodeURIComponent(build());
  });
  document.getElementById('copyBtn').addEventListener('click', function () {
    var text = '宛先: ' + MAIL + '\n件名: ' + subject() + '\n\n' + build();
    function done() { var t = document.getElementById('toast'); t.classList.add('show'); setTimeout(function () { t.classList.remove('show'); }, 1800); }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done);
    else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (e) {} document.body.removeChild(ta); done(); }
  });
})();
