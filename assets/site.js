/* Akula Uday Kiran – portfolio
   1. Light / dark theme switch.
   2. Fig. 1: potential flow past a Joukowski aerofoil, computed in the browser.
      The model matches tools/flow.py in the site's build notes: circle centre mu = -0.08 + 0.07i,
      Joukowski constant c = 1, circulation from the Kutta condition. */
(function () {
  'use strict';
  var root = document.documentElement;
  var darkQuery = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;

  /* ---------------------------------------------------------------- theme */
  var themeButton = document.querySelector('.theme');

  function currentTheme() {
    var t = root.getAttribute('data-theme');
    if (t === 'dark' || t === 'light') return t;
    return darkQuery && darkQuery.matches ? 'dark' : 'light';
  }

  function syncThemeButton() {
    if (!themeButton) return;
    var dark = currentTheme() === 'dark';
    themeButton.setAttribute('data-state', dark ? 'dark' : 'light');
    themeButton.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  }

  function announceTheme() {
    syncThemeButton();
    document.dispatchEvent(new CustomEvent('themechange'));
  }

  if (themeButton) {
    themeButton.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) { /* storage unavailable: theme lasts this visit */ }
      announceTheme();
    });
  }
  if (darkQuery) {
    if (darkQuery.addEventListener) darkQuery.addEventListener('change', announceTheme);
    else if (darkQuery.addListener) darkQuery.addListener(announceTheme);
  }
  syncThemeButton();

  /* ---------------------------------------------------------------- flow */
  var canvas = document.getElementById('flow');
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext('2d');
  var slider = document.getElementById('aoa');
  var aoaOut = document.getElementById('aoa-out');
  var clOut = document.getElementById('cl-out');
  var motionQuery = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;

  // Joukowski aerofoil: zeta = z + c^2 / z, with z on a circle through z = c.
  var C2 = 1;                      // c^2, with c = 1
  var MUX = -0.08, MUY = 0.07;     // circle centre: thickness and camber
  var R = Math.sqrt((1 - MUX) * (1 - MUX) + MUY * MUY);
  var R2 = R * R;
  var BETA = Math.atan2(MUY, 1 - MUX);
  var ca = 1, sa = 0, K = 0;       // cos and sin of alpha; circulation / (2 pi)

  // Aerofoil outline in the zeta plane, and its chord.
  var OUTLINE = [];
  var xmin = Infinity, xmax = -Infinity;
  (function () {
    for (var i = 0; i <= 360; i++) {
      var t = (i / 360) * 2 * Math.PI;
      var zr = MUX + R * Math.cos(t), zi = MUY + R * Math.sin(t);
      var m = zr * zr + zi * zi;
      var x = zr + zr / m, y = zi - zi / m;          // z + 1/z
      OUTLINE.push(x, y);
      if (x < xmin) xmin = x;
      if (x > xmax) xmax = x;
    }
  })();
  var CHORD = xmax - xmin;

  function setAngle(deg) {
    var a = deg * Math.PI / 180;
    ca = Math.cos(a); sa = Math.sin(a);
    var gamma = 4 * Math.PI * R * Math.sin(a + BETA);   // Kutta condition, U = 1
    K = gamma / (2 * Math.PI);
    var sign = deg < 0 ? '−' : '';
    if (aoaOut) aoaOut.textContent = sign + Math.abs(deg).toFixed(1) + '°';
    if (clOut) {
      var cl = 2 * gamma / CHORD;
      clOut.textContent = (cl < 0 ? '−' : '') + Math.abs(cl).toFixed(2);
    }
  }

  // Velocity (u, v) at zeta = x + iy, written to out. Returns false inside the aerofoil.
  function velocity(x, y, out) {
    // z = (zeta +- sqrt(zeta^2 - 4c^2)) / 2, taking the root outside the circle
    var ar = x * x - y * y - 4 * C2, ai = 2 * x * y;
    var m = Math.sqrt(ar * ar + ai * ai);
    var sr = Math.sqrt(Math.max(0, (m + ar) / 2));
    var si = Math.sqrt(Math.max(0, (m - ar) / 2));
    if (ai < 0) si = -si;
    var z1r = (x + sr) / 2, z1i = (y + si) / 2, z2r = (x - sr) / 2, z2i = (y - si) / 2;
    var d1 = (z1r - MUX) * (z1r - MUX) + (z1i - MUY) * (z1i - MUY);
    var d2 = (z2r - MUX) * (z2r - MUX) + (z2i - MUY) * (z2i - MUY);
    var zr, zi, d;
    if (d1 >= d2) { zr = z1r; zi = z1i; d = d1; } else { zr = z2r; zi = z2i; d = d2; }
    if (d < R2) return false;
    var wr = zr - MUX, wi = zi - MUY;
    var iwr = wr / d, iwi = -wi / d;                        // 1 / (z - mu)
    var iw2r = iwr * iwr - iwi * iwi, iw2i = 2 * iwr * iwi;   // 1 / (z - mu)^2
    var er = ca * iw2r - sa * iw2i, ei = ca * iw2i + sa * iw2r;
    var Wr = ca - R2 * er - K * iwi;                        // dw/dz, conjugate velocity in the circle plane
    var Wi = -sa - R2 * ei + K * iwr;
    var zz = zr * zr + zi * zi;
    var zz2 = zz * zz;
    var Dr = 1 - C2 * (zr * zr - zi * zi) / zz2;            // dzeta/dz = 1 - c^2 / z^2
    var Di = C2 * 2 * zr * zi / zz2;
    var Dm = Dr * Dr + Di * Di;
    if (Dm < 1e-10) return false;
    out[0] = (Wr * Dr + Wi * Di) / Dm;
    out[1] = -(Wi * Dr - Wr * Di) / Dm;
    return true;
  }

  // View: zeta from X0 to X1, centred vertically on Y_MID.
  var X0 = -3.15, X1 = 3.05, Y_MID = 0.05;
  var W = 0, H = 0, dpr = 1, scale = 1, Y0 = 0, Y1 = 0;
  var colours = [], bins = 9;
  var N = 0, px, py, age, life;
  var k1 = [0, 0], k2 = [0, 0];
  var running = false, visible = true, last = 0, raf = 0;

  function hexToRgb(hex) {
    var h = hex.trim().replace('#', '');
    if (h.length === 3) h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    var n = parseInt(h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function mix(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t]; }

  var bodyFill = '#fff', bodyEdge = '#000';
  function readColours() {
    var s = getComputedStyle(root);
    var slow = hexToRgb(s.getPropertyValue('--flow-slow') || '#255C8F');
    var mid = hexToRgb(s.getPropertyValue('--flow-mid') || '#8295A7');
    var fast = hexToRgb(s.getPropertyValue('--flow-fast') || '#E5560B');
    bodyFill = (s.getPropertyValue('--flow-body') || '#fff').trim();
    bodyEdge = (s.getPropertyValue('--flow-edge') || '#000').trim();
    colours = [];
    for (var i = 0; i < bins; i++) {
      var t = i / (bins - 1);
      var c = t < 0.5 ? mix(slow, mid, t / 0.5) : mix(mid, fast, (t - 0.5) / 0.5);
      colours.push('rgb(' + Math.round(c[0]) + ',' + Math.round(c[1]) + ',' + Math.round(c[2]) + ')');
    }
  }
  // speed 0.35 and below -> slowest colour, 1 -> middle, 1.65 and above -> fastest
  function bin(speed) {
    var t = (speed - 0.35) / 1.3;
    if (t < 0) t = 0; else if (t > 1) t = 1;
    return Math.round(t * (bins - 1));
  }

  function sx(x) { return (x - X0) * scale; }
  function sy(y) { return H / 2 - (y - Y_MID) * scale; }

  function resize() {
    var rect = canvas.getBoundingClientRect();
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = Math.max(1, Math.round(rect.width * dpr));
    H = Math.max(1, Math.round(rect.height * dpr));
    canvas.width = W; canvas.height = H;
    scale = W / (X1 - X0);
    Y0 = Y_MID - H / 2 / scale; Y1 = Y_MID + H / 2 / scale;
    var n = Math.round(rect.width * rect.height / 430);
    N = Math.max(120, Math.min(1100, n));
    px = new Float32Array(N); py = new Float32Array(N); age = new Float32Array(N); life = new Float32Array(N);
    for (var i = 0; i < N; i++) spawn(i, true);
    ctx.clearRect(0, 0, W, H);
  }

  function spawn(i, anywhere) {
    for (var tries = 0; tries < 20; tries++) {
      var x = anywhere ? X0 + Math.random() * (X1 - X0) : X0 - Math.random() * 0.25;
      var y = Y0 + Math.random() * (Y1 - Y0);
      if (velocity(x, y, k1)) { px[i] = x; py[i] = y; break; }
    }
    age[i] = 0;
    life[i] = 2.5 + Math.random() * 5;   // seconds before a tracer is reborn somewhere else
  }

  function drawBody() {
    ctx.beginPath();
    for (var i = 0; i < OUTLINE.length; i += 2) {
      var X = sx(OUTLINE[i]), Y = sy(OUTLINE[i + 1]);
      if (i === 0) ctx.moveTo(X, Y); else ctx.lineTo(X, Y);
    }
    ctx.closePath();
    ctx.fillStyle = bodyFill;
    ctx.fill();
    ctx.lineWidth = 1.3 * dpr;
    ctx.strokeStyle = bodyEdge;
    ctx.stroke();
  }

  var paths = [];
  function step(dt) {
    // fade old trails towards transparent
    ctx.globalCompositeOperation = 'destination-out';
    ctx.fillStyle = 'rgba(0,0,0,' + Math.min(0.12, 2.4 * dt) + ')';
    ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'source-over';

    for (var b = 0; b < bins; b++) paths[b] = [];
    var h = dt * 1.25;   // flow speed on screen, in chord-units per second
    for (var i = 0; i < N; i++) {
      var x = px[i], y = py[i];
      if (!velocity(x, y, k1)) { spawn(i, true); continue; }
      var xm = x + 0.5 * h * k1[0], ym = y + 0.5 * h * k1[1];
      if (!velocity(xm, ym, k2)) { spawn(i, true); continue; }
      var nx = x + h * k2[0], ny = y + h * k2[1];
      paths[bin(Math.sqrt(k2[0] * k2[0] + k2[1] * k2[1]))].push(sx(x), sy(y), sx(nx), sy(ny));
      px[i] = nx; py[i] = ny; age[i] += dt;
      if (nx > X1 + 0.05 || ny < Y0 - 0.2 || ny > Y1 + 0.2) spawn(i, false);
      else if (age[i] > life[i]) spawn(i, true);
    }
    ctx.lineWidth = 1.3 * dpr;
    ctx.lineCap = 'round';
    for (b = 0; b < bins; b++) {
      var p = paths[b];
      if (!p.length) continue;
      ctx.beginPath();
      for (var j = 0; j < p.length; j += 4) { ctx.moveTo(p[j], p[j + 1]); ctx.lineTo(p[j + 2], p[j + 3]); }
      ctx.strokeStyle = colours[b];
      ctx.stroke();
    }
    drawBody();
  }

  // Reduced motion, or a static redraw: integrate streamlines once and draw them.
  function drawStatic() {
    ctx.clearRect(0, 0, W, H);
    ctx.lineWidth = 1.1 * dpr;
    ctx.lineCap = 'round';
    var spacing = (Y1 - Y0) / 34;
    for (var y0 = Y0 + spacing / 2; y0 < Y1; y0 += spacing) {
      var x = X0, y = y0, n = 0;
      while (x < X1 && n < 3000) {
        if (!velocity(x, y, k1)) break;
        var hs = 0.02;
        var xm = x + 0.5 * hs * k1[0], ym = y + 0.5 * hs * k1[1];
        if (!velocity(xm, ym, k2)) break;
        var nx = x + hs * k2[0], ny = y + hs * k2[1];
        ctx.beginPath();
        ctx.moveTo(sx(x), sy(y)); ctx.lineTo(sx(nx), sy(ny));
        ctx.strokeStyle = colours[bin(Math.sqrt(k2[0] * k2[0] + k2[1] * k2[1]))];
        ctx.stroke();
        x = nx; y = ny; n++;
      }
    }
    drawBody();
  }

  function reducedMotion() { return motionQuery && motionQuery.matches; }

  function frame(t) {
    if (!running) return;
    var dt = last ? Math.min(0.05, (t - last) / 1000) : 0.016;
    last = t;
    step(dt);
    raf = requestAnimationFrame(frame);
  }
  function start() {
    if (running || reducedMotion() || !visible || document.hidden) return;
    running = true; last = 0;
    raf = requestAnimationFrame(frame);
  }
  function stop() { running = false; if (raf) cancelAnimationFrame(raf); raf = 0; }
  function refresh() {
    if (reducedMotion()) { stop(); drawStatic(); }
    else { ctx.clearRect(0, 0, W, H); start(); }
  }

  setAngle(slider ? parseFloat(slider.value) : 6);
  readColours();
  resize();
  refresh();

  if (slider) {
    slider.addEventListener('input', function () {
      setAngle(parseFloat(slider.value));
      if (reducedMotion()) drawStatic();
    });
  }
  document.addEventListener('themechange', function () { readColours(); refresh(); });
  if (motionQuery) {
    var onMotion = function () { refresh(); };
    if (motionQuery.addEventListener) motionQuery.addEventListener('change', onMotion);
    else if (motionQuery.addListener) motionQuery.addListener(onMotion);
  }
  document.addEventListener('visibilitychange', function () { if (document.hidden) stop(); else start(); });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
      if (visible) start(); else stop();
    }).observe(canvas);
  }
  if ('ResizeObserver' in window) {
    var lastWidth = 0;
    new ResizeObserver(function () {
      var w = canvas.getBoundingClientRect().width;
      if (Math.abs(w - lastWidth) < 1) return;
      lastWidth = w;
      resize();
      refresh();
    }).observe(canvas);
  }
})();
