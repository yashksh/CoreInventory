'use strict';

/* ============================================================
   CoreInventory – Settings Page JavaScript
   Handles tabs + CRUD for warehouses, locations, contacts.
   ============================================================ */

// ── Toast ─────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toastMsg');
  const toastIcon = document.getElementById('toastIcon');
  toastMsg.textContent = msg;
  toast.className = toast.className.replace(/bg-\S+/, '');
  toast.classList.add(type === 'error' ? 'bg-red-500' : 'bg-green-500');
  toastIcon.textContent = type === 'error' ? 'error' : 'check_circle';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// ── Modal helpers ─────────────────────────────────────────────
function openModal(id) {
  const el = document.getElementById(id);
  el.classList.remove('hidden');
  el.classList.add('flex');
}
function closeModal(id) {
  const el = document.getElementById(id);
  el.classList.add('hidden');
  el.classList.remove('flex');
}

// Close modal buttons
document.querySelectorAll('.close-modal').forEach(btn => {
  btn.addEventListener('click', () => closeModal(btn.dataset.modal));
});

// Backdrop close
['bdAddWH', 'bdAddLoc', 'bdAddContact'].forEach(id => {
  const el = document.getElementById(id);
  if (el) el.addEventListener('click', () => {
    closeModal(el.parentElement.id);
  });
});


// ═══════════════════════════════════════════════════════════════
// TABS
// ═══════════════════════════════════════════════════════════════
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    // Remove active from all tabs
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    // Hide all panels, show target
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
    document.getElementById('panel-' + btn.dataset.tab).classList.remove('hidden');
  });
});


// ═══════════════════════════════════════════════════════════════
// WAREHOUSES
// ═══════════════════════════════════════════════════════════════
document.getElementById('btnAddWH').addEventListener('click', () => {
  document.getElementById('whName').value = '';
  document.getElementById('whCode').value = '';
  document.getElementById('whAddress').value = '';
  document.getElementById('whError').classList.add('hidden');
  openModal('modalAddWH');
});

document.getElementById('submitWH').addEventListener('click', async () => {
  const errEl = document.getElementById('whError');
  const name = document.getElementById('whName').value.trim();
  const code = document.getElementById('whCode').value.trim();
  const address = document.getElementById('whAddress').value.trim();

  if (!name || !code) {
    errEl.textContent = 'Name and short code are required.';
    errEl.classList.remove('hidden');
    return;
  }

  try {
    const res = await fetch('/api/warehouse/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, short_code: code, address }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalAddWH');
      showToast('Warehouse added!');
      setTimeout(() => location.reload(), 500);
    } else {
      errEl.textContent = data.error;
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error.';
    errEl.classList.remove('hidden');
  }
});

// Delete warehouse
document.querySelectorAll('.btn-del-wh').forEach(btn => {
  btn.addEventListener('click', async () => {
    if (!confirm('Delete this warehouse? All its locations will also be deleted.')) return;
    try {
      const res = await fetch('/api/warehouse/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: btn.dataset.id }),
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Warehouse deleted!');
        setTimeout(() => location.reload(), 500);
      } else {
        showToast(data.error, 'error');
      }
    } catch (e) {
      showToast('Network error', 'error');
    }
  });
});


// ═══════════════════════════════════════════════════════════════
// LOCATIONS
// ═══════════════════════════════════════════════════════════════
document.getElementById('btnAddLoc').addEventListener('click', () => {
  document.getElementById('locName').value = '';
  document.getElementById('locCode').value = '';
  document.getElementById('locError').classList.add('hidden');
  openModal('modalAddLoc');
});

document.getElementById('submitLoc').addEventListener('click', async () => {
  const errEl = document.getElementById('locError');
  const warehouseId = document.getElementById('locWH').value;
  const name = document.getElementById('locName').value.trim();
  const code = document.getElementById('locCode').value.trim();

  if (!warehouseId || !name || !code) {
    errEl.textContent = 'All fields are required.';
    errEl.classList.remove('hidden');
    return;
  }

  try {
    const res = await fetch('/api/location/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ warehouse_id: warehouseId, name, short_code: code }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalAddLoc');
      showToast('Location added!');
      setTimeout(() => location.reload(), 500);
    } else {
      errEl.textContent = data.error;
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error.';
    errEl.classList.remove('hidden');
  }
});

// Delete location
document.querySelectorAll('.btn-del-loc').forEach(btn => {
  btn.addEventListener('click', async () => {
    if (!confirm('Delete this location?')) return;
    try {
      const res = await fetch('/api/location/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: btn.dataset.id }),
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Location deleted!');
        setTimeout(() => location.reload(), 500);
      } else {
        showToast(data.error, 'error');
      }
    } catch (e) {
      showToast('Network error', 'error');
    }
  });
});


// ═══════════════════════════════════════════════════════════════
// CONTACTS
// ═══════════════════════════════════════════════════════════════
document.getElementById('btnAddContact').addEventListener('click', () => {
  document.getElementById('ctName').value = '';
  document.getElementById('ctType').value = 'vendor';
  document.getElementById('ctEmail').value = '';
  document.getElementById('ctPhone').value = '';
  document.getElementById('ctError').classList.add('hidden');
  openModal('modalAddContact');
});

document.getElementById('submitContact').addEventListener('click', async () => {
  const errEl = document.getElementById('ctError');
  const name = document.getElementById('ctName').value.trim();
  const type = document.getElementById('ctType').value;
  const email = document.getElementById('ctEmail').value.trim();
  const phone = document.getElementById('ctPhone').value.trim();

  if (!name) {
    errEl.textContent = 'Name is required.';
    errEl.classList.remove('hidden');
    return;
  }

  try {
    const res = await fetch('/api/contact/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, type, email, phone }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalAddContact');
      showToast('Contact added!');
      setTimeout(() => location.reload(), 500);
    } else {
      errEl.textContent = data.error;
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error.';
    errEl.classList.remove('hidden');
  }
});

// Delete contact
document.querySelectorAll('.btn-del-contact').forEach(btn => {
  btn.addEventListener('click', async () => {
    if (!confirm('Delete this contact?')) return;
    try {
      const res = await fetch('/api/contact/delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: btn.dataset.id }),
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Contact deleted!');
        setTimeout(() => location.reload(), 500);
      } else {
        showToast(data.error, 'error');
      }
    } catch (e) {
      showToast('Network error', 'error');
    }
  });
});
