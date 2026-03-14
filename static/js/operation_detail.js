'use strict';

/* ============================================================
   CoreInventory – Operation Detail Page JavaScript
   ============================================================ */

// ── Toast ─────────────────────────────────────────────────────
function showToast(msg, type = 'success') {
  const toast = document.getElementById('toast');
  const toastMsg = document.getElementById('toastMsg');
  const toastIcon = document.getElementById('toastIcon');
  toastMsg.textContent = msg;
  toast.className = toast.className.replace(/bg-\S+/g, '');
  toast.classList.add(type === 'error' ? 'bg-red-500' : 'bg-green-500');
  toastIcon.textContent = type === 'error' ? 'error' : 'check_circle';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}

// ── New Button Dropdown ───────────────────────────────────────
const btnNewDrop = document.getElementById('btnNewDrop');
const newDropMenu = document.getElementById('newDropMenu');

if (btnNewDrop && newDropMenu) {
  btnNewDrop.addEventListener('click', (e) => {
    e.stopPropagation();
    newDropMenu.classList.toggle('hidden');
  });
  document.addEventListener('click', () => newDropMenu.classList.add('hidden'));
}


// ── Auto-save field changes ───────────────────────────────────
function autoSaveField(field, key) {
  if (!field) return;
  field.addEventListener('change', async () => {
    const body = {};
    body[key] = field.value || null;
    try {
      const res = await fetch(`/api/operation/${MOVE_ID}/update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Saved');
      } else {
        showToast(data.error || 'Failed to save', 'error');
      }
    } catch (e) {
      showToast('Network error', 'error');
    }
  });
}

autoSaveField(document.getElementById('fieldContact'), 'contact_id');
autoSaveField(document.getElementById('fieldDate'), 'schedule_date');
autoSaveField(document.getElementById('fieldFromLoc'), 'from_location_id');
autoSaveField(document.getElementById('fieldToLoc'), 'to_location_id');


// ── Add Product Line ──────────────────────────────────────────
const btnAddLine = document.getElementById('btnAddLine');
if (btnAddLine) {
  btnAddLine.addEventListener('click', async () => {
    const productSelect = document.getElementById('newLineProduct');
    const qtyInput = document.getElementById('newLineQty');
    const productId = productSelect.value;
    const qty = parseInt(qtyInput.value);

    if (!productId || !qty || qty <= 0) {
      showToast('Select a product and enter quantity', 'error');
      return;
    }

    btnAddLine.disabled = true;
    btnAddLine.innerHTML = '<span class="material-symbols-outlined text-[16px] spin-icon">sync</span>';

    try {
      const res = await fetch(`/api/operation/${MOVE_ID}/add-line`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: parseInt(productId), quantity: qty }),
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        // Add row to table
        const tbody = document.getElementById('linesBody');
        const tr = document.createElement('tr');
        tr.className = 'product-line-row';
        tr.dataset.lineId = data.line.id;
        tr.innerHTML = `
          <td class="py-3 pr-4">
            <span class="font-semibold text-gray-900">[${data.line.product_code}] ${data.line.product_name}</span>
          </td>
          <td class="py-3 pr-4 text-right font-medium text-gray-700">${data.line.quantity}</td>
          <td class="py-3 text-right">
            <button class="btn-remove-line p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all"
                    data-line-id="${data.line.id}" title="Remove">
              <span class="material-symbols-outlined text-[18px]">close</span>
            </button>
          </td>
        `;
        tbody.appendChild(tr);
        attachRemoveHandler(tr.querySelector('.btn-remove-line'));

        // Clear inputs
        productSelect.value = '';
        qtyInput.value = '';
        showToast(`Added ${data.line.product_name}`);
      } else {
        showToast(data.error || 'Failed', 'error');
      }
    } catch (e) {
      showToast('Network error', 'error');
    } finally {
      btnAddLine.disabled = false;
      btnAddLine.innerHTML = '<span class="material-symbols-outlined text-[16px]">add</span> Add';
    }
  });
}


// ── Remove Product Line ───────────────────────────────────────
function attachRemoveHandler(btn) {
  btn.addEventListener('click', async () => {
    const lineId = btn.dataset.lineId;
    btn.disabled = true;
    try {
      const res = await fetch(`/api/operation/${MOVE_ID}/remove-line`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ line_id: parseInt(lineId) }),
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        btn.closest('tr').remove();
        showToast('Line removed');
      } else {
        showToast(data.error || 'Failed', 'error');
        btn.disabled = false;
      }
    } catch (e) {
      showToast('Network error', 'error');
      btn.disabled = false;
    }
  });
}

document.querySelectorAll('.btn-remove-line').forEach(attachRemoveHandler);


// ── Mark as Ready (draft → ready) ─────────────────────────────
const btnReady = document.getElementById('btnMarkReady');
if (btnReady) {
  btnReady.addEventListener('click', async () => {
    btnReady.disabled = true;
    btnReady.innerHTML = '<span class="material-symbols-outlined text-[18px] spin-icon">sync</span> Processing…';
    try {
      const res = await fetch(`/api/operation/${MOVE_ID}/confirm`, {
        method: 'POST',
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Marked as Ready!');
        setTimeout(() => location.reload(), 600);
      } else {
        showToast(data.error || 'Failed', 'error');
        btnReady.disabled = false;
        btnReady.innerHTML = '<span class="material-symbols-outlined text-[18px]">check</span> Mark as Ready';
      }
    } catch (e) {
      showToast('Network error', 'error');
      btnReady.disabled = false;
      btnReady.innerHTML = '<span class="material-symbols-outlined text-[18px]">check</span> Mark as Ready';
    }
  });
}


// ── Validate (ready → done) ───────────────────────────────────
const btnValidate = document.getElementById('btnValidate');
if (btnValidate) {
  btnValidate.addEventListener('click', async () => {
    btnValidate.disabled = true;
    btnValidate.innerHTML = '<span class="material-symbols-outlined text-[18px] spin-icon">sync</span> Validating…';
    try {
      const res = await fetch(`/api/operation/${MOVE_ID}/validate`, {
        method: 'POST',
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Validated! Inventory updated.');
        setTimeout(() => location.reload(), 600);
      } else {
        showToast(data.error || 'Failed', 'error');
        btnValidate.disabled = false;
        btnValidate.innerHTML = '<span class="material-symbols-outlined text-[18px]">verified</span> Validate';
      }
    } catch (e) {
      showToast('Network error', 'error');
      btnValidate.disabled = false;
      btnValidate.innerHTML = '<span class="material-symbols-outlined text-[18px]">verified</span> Validate';
    }
  });
}


// ── Cancel Operation ──────────────────────────────────────────
const btnCancel = document.getElementById('btnCancel');
if (btnCancel) {
  btnCancel.addEventListener('click', async () => {
    if (!confirm('Cancel this operation? This will delete it permanently.')) return;

    btnCancel.disabled = true;
    try {
      const res = await fetch(`/api/operation/${MOVE_ID}/cancel`, {
        method: 'POST',
        credentials: 'same-origin',
      });
      const data = await res.json();
      if (data.success) {
        showToast('Operation cancelled');
        setTimeout(() => { window.location.href = '/operations'; }, 600);
      } else {
        showToast(data.error || 'Failed', 'error');
        btnCancel.disabled = false;
      }
    } catch (e) {
      showToast('Network error', 'error');
      btnCancel.disabled = false;
    }
  });
}
