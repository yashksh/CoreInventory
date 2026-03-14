'use strict';

/* ============================================================
   CoreInventory – Operations Page JavaScript
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

// ═══════════════════════════════════════════════════════════════
// CREATE OPERATION MODAL
// ═══════════════════════════════════════════════════════════════

document.getElementById('btnCreateOp').addEventListener('click', () => {
  document.getElementById('opError').classList.add('hidden');
  openModal('modalCreateOp');
});

['closeCreateOp', 'cancelCreateOp', 'backdropCreateOp'].forEach(id => {
  document.getElementById(id).addEventListener('click', () => closeModal('modalCreateOp'));
});

// ── Add product line ──────────────────────────────────────────
document.getElementById('btnAddLine').addEventListener('click', () => {
  const container = document.getElementById('productLines');
  const firstLine = container.querySelector('.product-line');
  const clone = firstLine.cloneNode(true);
  clone.querySelector('.line-product').value = '';
  clone.querySelector('.line-qty').value = '';
  const removeBtn = clone.querySelector('.btn-remove-line');
  removeBtn.classList.remove('hidden');
  removeBtn.addEventListener('click', () => clone.remove());
  container.appendChild(clone);
});

// ── Submit create ─────────────────────────────────────────────
document.getElementById('submitCreateOp').addEventListener('click', async () => {
  const btn = document.getElementById('submitCreateOp');
  const errEl = document.getElementById('opError');

  const opType = document.getElementById('opType').value;
  const contactId = document.getElementById('opContact').value;
  const fromLocId = document.getElementById('opFromLoc').value;
  const toLocId = document.getElementById('opToLoc').value;
  const schedDate = document.getElementById('opDate').value;

  // Collect product lines
  const lineEls = document.querySelectorAll('.product-line');
  const lines = [];
  lineEls.forEach(el => {
    const pid = el.querySelector('.line-product').value;
    const qty = el.querySelector('.line-qty').value;
    if (pid && qty && parseInt(qty) > 0) {
      lines.push({ product_id: parseInt(pid), quantity: parseInt(qty) });
    }
  });

  if (!lines.length) {
    errEl.textContent = 'Add at least one product line with quantity.';
    errEl.classList.remove('hidden');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="material-symbols-outlined text-[18px] spin-icon">sync</span> Creating…';

  try {
    const res = await fetch('/api/operation/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        operation_type: opType,
        contact_id: contactId || null,
        from_location_id: fromLocId || null,
        to_location_id: toLocId || null,
        schedule_date: schedDate || null,
        lines: lines,
      }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalCreateOp');
      showToast(`Operation ${data.reference} created!`);
      setTimeout(() => location.reload(), 500);
    } else {
      errEl.textContent = data.error || 'Failed to create operation.';
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error. Please try again.';
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">add</span> Create Operation';
  }
});


// ═══════════════════════════════════════════════════════════════
// CONFIRM & VALIDATE BUTTONS
// ═══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  // Confirm buttons
  document.querySelectorAll('.btn-confirm').forEach(btn => {
    btn.addEventListener('click', async () => {
      const moveId = btn.dataset.id;
      btn.disabled = true;
      btn.textContent = 'Confirming…';
      try {
        const res = await fetch(`/api/operation/${moveId}/confirm`, {
          method: 'POST',
          credentials: 'same-origin',
        });
        const data = await res.json();
        if (data.success) {
          showToast('Operation confirmed!');
          setTimeout(() => location.reload(), 500);
        } else {
          showToast(data.error || 'Failed to confirm', 'error');
          btn.disabled = false;
          btn.textContent = 'Confirm';
        }
      } catch (e) {
        showToast('Network error', 'error');
        btn.disabled = false;
        btn.textContent = 'Confirm';
      }
    });
  });

  // Validate buttons
  document.querySelectorAll('.btn-validate').forEach(btn => {
    btn.addEventListener('click', async () => {
      const moveId = btn.dataset.id;
      btn.disabled = true;
      btn.textContent = 'Validating…';
      try {
        const res = await fetch(`/api/operation/${moveId}/validate`, {
          method: 'POST',
          credentials: 'same-origin',
        });
        const data = await res.json();
        if (data.success) {
          showToast('Operation validated! Inventory updated.');
          setTimeout(() => location.reload(), 500);
        } else {
          showToast(data.error || 'Failed to validate', 'error');
          btn.disabled = false;
          btn.textContent = 'Validate';
        }
      } catch (e) {
        showToast('Network error', 'error');
        btn.disabled = false;
        btn.textContent = 'Validate';
      }
    });
  });

  // View details buttons
  document.querySelectorAll('.btn-view-op').forEach(btn => {
    btn.addEventListener('click', async () => {
      const moveId = btn.dataset.id;
      try {
        const res = await fetch(`/api/operation/${moveId}`, { credentials: 'same-origin' });
        const data = await res.json();
        const title = document.getElementById('viewOpTitle');
        const content = document.getElementById('viewOpContent');

        title.textContent = data.reference;

        let linesHtml = '';
        if (data.lines && data.lines.length) {
          linesHtml = '<table class="w-full mt-2 text-sm"><thead><tr class="border-b"><th class="text-left py-1">Product</th><th class="text-right py-1">Qty</th></tr></thead><tbody>';
          data.lines.forEach(l => {
            linesHtml += `<tr class="border-b border-gray-100"><td class="py-1">${l.product_name} <span class="text-gray-400 text-xs">(${l.product_code})</span></td><td class="text-right py-1 font-semibold">${l.quantity}</td></tr>`;
          });
          linesHtml += '</tbody></table>';
        }

        content.innerHTML = `
          <div class="grid grid-cols-2 gap-3">
            <div><span class="text-gray-400 text-xs uppercase font-bold">Type</span><p class="font-semibold capitalize">${data.operation_type}</p></div>
            <div><span class="text-gray-400 text-xs uppercase font-bold">Status</span><p class="font-semibold capitalize">${data.status}</p></div>
            <div><span class="text-gray-400 text-xs uppercase font-bold">Contact</span><p>${data.contact_name}</p></div>
            <div><span class="text-gray-400 text-xs uppercase font-bold">Scheduled</span><p>${data.schedule_date || '—'}</p></div>
            <div><span class="text-gray-400 text-xs uppercase font-bold">From</span><p>${data.from_location}</p></div>
            <div><span class="text-gray-400 text-xs uppercase font-bold">To</span><p>${data.to_location}</p></div>
          </div>
          <hr class="my-3 border-gray-100"/>
          <p class="text-xs font-bold text-gray-400 uppercase mb-1">Product Lines</p>
          ${linesHtml || '<p class="text-gray-400">No lines</p>'}
        `;

        openModal('modalViewOp');
      } catch (e) {
        showToast('Failed to load details', 'error');
      }
    });
  });
});

// View modal close
['closeViewOp', 'cancelViewOp', 'backdropViewOp'].forEach(id => {
  document.getElementById(id).addEventListener('click', () => closeModal('modalViewOp'));
});
