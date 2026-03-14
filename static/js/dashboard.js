/* ============================================================
   CoreInventory – Dashboard JavaScript
   Fetches /api/dashboard-stats every 60 seconds and updates
   the DOM without a full page reload.  Animates number
   changes so operators immediately notice updates.
   ============================================================ */

'use strict';

// ── Stat field → DOM element id map ──────────────────────────
const STAT_IDS = [
  'pending_receipts',
  'late_receipts',
  'waiting_receipts',
  'total_receipt_operations',
  'pending_deliveries',
  'late_deliveries',
  'waiting_deliveries',
  'total_delivery_operations',
];

// ── Helpers ───────────────────────────────────────────────────

/**
 * Animate counting from current displayed value to newVal.
 * Falls back to an instant set if the delta is large (>200).
 */
function animateCount(el, newVal) {
  const current = parseInt(el.textContent, 10) || 0;
  const diff = newVal - current;

  if (diff === 0) return;

  // Large jump → instant update with flash
  if (Math.abs(diff) > 200) {
    el.textContent = newVal;
    triggerFlash(el);
    return;
  }

  const steps = 20;
  const duration = 300; // ms
  const stepTime = duration / steps;
  let step = 0;

  const timer = setInterval(() => {
    step++;
    el.textContent = Math.round(current + (diff * step) / steps);
    if (step >= steps) {
      clearInterval(timer);
      el.textContent = newVal;
      triggerFlash(el);
    }
  }, stepTime);
}

/** Brief scale+opacity flash to signal the number changed. */
function triggerFlash(el) {
  el.classList.remove('num-flash');
  // Force reflow so animation re-triggers even if class already present
  void el.offsetWidth;
  el.classList.add('num-flash');
  el.addEventListener('animationend', () => el.classList.remove('num-flash'), { once: true });
}

/** Format current time as HH:MM:SS for the "Last updated" label. */
function nowFormatted() {
  return new Date().toLocaleTimeString(undefined, {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

// ── Core refresh function (also called by the Refresh button) ─

async function refreshStats() {
  const btn        = document.getElementById('refreshBtn');
  const icon       = document.getElementById('refreshIcon');
  const liveDot    = document.getElementById('liveDot');
  const lastUpdated = document.getElementById('lastUpdated');

  // Spin the icon while fetching
  icon.classList.add('spin');
  btn.disabled = true;

  try {
    const res  = await fetch('/api/dashboard-stats', { credentials: 'same-origin' });

    if (!res.ok) {
      // Session expired → redirect to login
      if (res.status === 401 || res.status === 302) {
        window.location.href = '/login';
        return;
      }
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();

    // Update every stat with animated counting
    STAT_IDS.forEach(key => {
      const el = document.getElementById(key);
      if (el && data[key] !== undefined) {
        animateCount(el, data[key]);
      }
    });

    // Timestamp
    lastUpdated.textContent = nowFormatted();

    // Green dot – pulse once to signal success
    liveDot.style.backgroundColor = '#22c55e'; // green-500

  } catch (err) {
    console.error('[CoreInventory] Dashboard refresh failed:', err);
    // Turn dot red briefly to signal error
    liveDot.style.backgroundColor = '#ef4444';
    setTimeout(() => { liveDot.style.backgroundColor = ''; }, 3000);
  } finally {
    icon.classList.remove('spin');
    btn.disabled = false;
  }
}

// ── Auto-refresh every 60 seconds ────────────────────────────

let autoRefreshTimer = setInterval(refreshStats, 60_000);

// ── Page visibility API – pause when tab is hidden ───────────

document.addEventListener('visibilitychange', () => {
  if (document.hidden) {
    clearInterval(autoRefreshTimer);
  } else {
    // Immediately refresh when user returns to the tab
    refreshStats();
    autoRefreshTimer = setInterval(refreshStats, 60_000);
  }
});

// ── Initialise timestamp on first load ───────────────────────

document.addEventListener('DOMContentLoaded', () => {
  const lastUpdated = document.getElementById('lastUpdated');
  if (lastUpdated) lastUpdated.textContent = nowFormatted();
});
