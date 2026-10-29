// =====================================================================
//  CS-1-23 SMART PARKING — STANDALONE EMBEDDED WEB DASHBOARD
// =====================================================================
#pragma once
#include <Arduino.h>

const char INDEX_HTML[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Parkly.uz — IoT Hub Controller</title>
  <style>
    :root {
      --bg: #0b1120;
      --card: #1e293b;
      --border: #334155;
      --accent: #10b981;
      --cyan: #06b6d4;
      --red: #ef4444;
      --yellow: #f59e0b;
      --text: #f8fafc;
      --text-dim: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    body { background: var(--bg); color: var(--text); padding: 16px; min-height: 100vh; }
    .container { max-width: 900px; margin: 0 auto; display: flex; flex-direction: column; gap: 16px; }
    header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
    h1 { font-size: 20px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px; }
    .badge { padding: 4px 10px; border-radius: 999px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .badge-online { background: rgba(16, 185, 129, 0.2); color: var(--accent); border: 1px solid var(--accent); }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    @media(max-width: 600px) { .grid-2 { grid-template-columns: 1fr; } }
    .card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 16px; }
    .card-title { font-size: 13px; font-weight: 600; color: var(--text-dim); text-transform: uppercase; margin-bottom: 12px; }
    .stat-val { font-size: 28px; font-weight: 800; color: #fff; }
    .spots-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
    .spot { padding: 14px 8px; text-align: center; border-radius: 12px; font-weight: 700; font-size: 15px; border: 1px solid transparent; transition: all 0.2s; }
    .spot-free { background: rgba(16, 185, 129, 0.15); color: var(--accent); border-color: rgba(16, 185, 129, 0.4); }
    .spot-busy { background: rgba(239, 68, 68, 0.15); color: var(--red); border-color: rgba(239, 68, 68, 0.4); }
    .spot-unknown { background: rgba(148, 163, 184, 0.1); color: var(--text-dim); border-color: var(--border); }
    .btn { display: inline-flex; align-items: center; justify-content: center; padding: 10px 16px; border-radius: 12px; border: none; font-weight: 600; font-size: 13px; cursor: pointer; transition: all 0.2s; gap: 6px; }
    .btn-emerald { background: var(--accent); color: #022c22; }
    .btn-emerald:hover { opacity: 0.9; }
    .btn-red { background: var(--red); color: #fff; }
    .btn-red:hover { opacity: 0.9; }
    .log-box { background: #070d19; border: 1px solid var(--border); border-radius: 12px; padding: 12px; font-family: monospace; font-size: 12px; max-height: 180px; overflow-y: auto; color: var(--cyan); }
    .log-entry { margin-bottom: 4px; border-bottom: 1px dashed rgba(255,255,255,0.05); padding-bottom: 3px; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>🚗 Parkly.uz Hub Controller</h1>
      <span class="badge badge-online" id="statusBadge">WebSocket Ulangan</span>
    </header>

    <div class="grid-2">
      <div class="card">
        <div class="card-title">Avtoturargoh Holati</div>
        <div style="display:flex; justify-content:space-between; align-items:flex-end;">
          <div>
            <div class="stat-val" id="freeCount">--</div>
            <div style="color:var(--text-dim); font-size:12px;">Bo'sh joylar / Jami: <span id="totalCount">8</span></div>
          </div>
          <div style="text-align:right;">
            <div class="stat-val" style="color:var(--red);" id="busyCount">--</div>
            <div style="color:var(--text-dim); font-size:12px;">Band joylar</div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-title">Shlagbaumlarni Boshqarish</div>
        <div style="display:flex; gap:10px; margin-top:8px;">
          <button class="btn btn-emerald" style="flex:1;" onclick="openGate('entry')">🟢 Kirishni Ochish</button>
          <button class="btn btn-red" style="flex:1;" onclick="openGate('exit')">🔴 Chiqishni Ochish</button>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-title">Joylar Xaritasi (Sensorlar Oqimi)</div>
      <div class="spots-grid" id="spotsGrid">
        <!-- JavaScript orqali to'ldiriladi -->
      </div>
    </div>

    <div class="card">
      <div class="card-title">Hodisalar Jurnali (Live Log)</div>
      <div class="log-box" id="logBox">
        <div class="log-entry">[Tizim] WebSocket ulanishi kutilmoqda...</div>
      </div>
    </div>
  </div>

  <script>
    let ws;
    function connectWs() {
      ws = new WebSocket('ws://' + window.location.host + '/ws');
      ws.onopen = () => {
        document.getElementById('statusBadge').innerText = 'Online';
        document.getElementById('statusBadge').className = 'badge badge-online';
      };
      ws.onclose = () => {
        document.getElementById('statusBadge').innerText = 'Qayta ulanmoqda...';
        setTimeout(connectWs, 2000);
      };
      ws.onmessage = (e) => {
        try {
          const d = JSON.parse(e.data);
          updateUI(d);
        } catch(err) { console.error(err); }
      };
    }

    function updateUI(d) {
      document.getElementById('freeCount').innerText = d.free;
      document.getElementById('busyCount').innerText = d.busy;
      document.getElementById('totalCount').innerText = d.total;

      const grid = document.getElementById('spotsGrid');
      grid.innerHTML = '';
      if(d.spots) {
        d.spots.forEach(s => {
          const div = document.createElement('div');
          let cls = 'spot-unknown';
          let txt = s.id;
          if(s.s === 0) { cls = 'spot-free'; txt += ' (BO\'SH)'; }
          else if(s.s === 1) { cls = 'spot-busy'; txt += ' (BAND)'; }
          div.className = 'spot ' + cls;
          div.innerText = txt;
          grid.appendChild(div);
        });
      }

      if(d.ev) {
        const lb = document.getElementById('logBox');
        lb.innerHTML = '';
        d.ev.forEach(ev => {
          const row = document.createElement('div');
          row.className = 'log-entry';
          row.innerText = `[${ev.t}s oldin] ${ev.m}`;
          lb.appendChild(row);
        });
      }
    }

    function openGate(type) {
      fetch('/api/open?gate=' + type, { method: 'POST' })
        .then(r => r.json())
        .then(res => console.log('Gate opened:', res));
    }

    connectWs();
  </script>
</body>
</html>
)rawliteral";
