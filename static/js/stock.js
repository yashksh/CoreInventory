'use strict';

/* ============================================================
   CoreInventory – Stock Page JavaScript
   Handles:
   - Live search (debounced, hits /api/products/search)
   - Add Product modal  → POST /api/product/add
   - Edit Product modal → POST /api/product/update
   - Update Stock modal → POST /api/stock/update
   - Re-renders table rows + insight stat cards after every mutation
   ============================================================ */

// ── Utility: show toast ───────────────────────────────────────
function showToast(msg, type = 'success') {
  const toast   = document.getElementById('toast');
  const toastMsg  = document.getElementById('toastMsg');
  const toastIcon = document.getElementById('toastIcon');

  toastMsg.textContent = msg;

  if (type === 'error') {
    toast.className = toast.className.replace(/bg-\S+/, '');
    toast.classList.add('bg-red-500');
    toastIcon.textContent = 'error';
  } else {
    toast.className = toast.className.replace(/bg-\S+/, '');
    toast.classList.add('bg-green-500');
    toastIcon.textContent = 'check_circle';
  }

  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

// ── Utility: open / close modals ─────────────────────────────
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

// ── Utility: flash stat number ────────────────────────────────
function flashNum(el, newVal) {
  el.textContent = newVal;
  el.classList.remove('num-flash');
  void el.offsetWidth;
  el.classList.add('num-flash');
  el.addEventListener('animationend', () => el.classList.remove('num-flash'), { once: true });
}

// ── Build a table row from a product object ───────────────────
function buildRow(p) {
  // Free-to-use colour
  let freeClass = 'bg-green-50 text-green-700';
  if (p.free_to_use < 15)                          freeClass = 'bg-red-50 text-red-600';
  else if (p.free_to_use < p.on_hand)              freeClass = 'bg-amber-50 text-amber-700';

  return `
  <tr class="hover:bg-sky-50/30 transition-colors group" data-id="${p.id}">
    <td class="px-6 py-5">
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-lg bg-gray-100 flex items-center justify-center text-gray-400 group-hover:bg-sky-100 group-hover:text-sky-600 transition-colors">
          <span class="material-symbols-outlined">inventory_2</span>
        </div>
        <div>
          <span class="font-semibold text-gray-900 product-name">${escHtml(p.name)}</span>
          <span class="block text-xs text-gray-400">${escHtml(p.product_code)}</span>
        </div>
      </div>
    </td>
    <td class="px-6 py-5 text-gray-600 product-cost">${Math.round(p.unit_cost)} Rs</td>
    <td class="px-6 py-5">
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium bg-gray-100 text-gray-700 on-hand">
        ${p.on_hand}
      </span>
    </td>
    <td class="px-6 py-5">
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium ${freeClass} free-to-use">
        ${p.free_to_use}
      </span>
    </td>
    <td class="px-6 py-5 text-right">
      <div class="flex justify-end gap-2">
        <button class="p-2 text-gray-400 hover:text-sky-600 hover:bg-sky-100 rounded-lg transition-all btn-edit"
                title="Edit Product"
                data-id="${p.id}" data-name="${escHtml(p.name)}" data-cost="${p.unit_cost}">
          <span class="material-symbols-outlined text-[20px]">edit</span>
        </button>
        <button class="flex items-center gap-1 px-3 py-1.5 text-xs font-bold text-sky-600 border border-sky-200 hover:bg-sky-600 hover:text-white rounded-lg transition-all btn-update"
                data-id="${p.id}" data-name="${escHtml(p.name)}">
          <span class="material-symbols-outlined text-[16px]">sync</span>
          Update
        </button>
      </div>
    </td>
  </tr>`;
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ── Render table from product array ───────────────────────────
function renderTable(products) {
  const tbody = document.getElementById('stockTableBody');
  if (!products.length) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="px-6 py-16 text-center text-gray-400">
          <span class="material-symbols-outlined text-4xl block mb-2">inventory_2</span>
          No products found.
        </td>
      </tr>`;
    return;
  }
  tbody.innerHTML = products.map(buildRow).join('');
  bindRowButtons();
}

// ── Update insight stat cards ──────────────────────────────────
function updateStats(data) {
  const ls  = document.getElementById('lowStockVal');
  const iv  = document.getElementById('invValueVal');
  const rs  = document.getElementById('reservedVal');
  const badge = document.getElementById('productCountBadge');

  if (ls) flashNum(ls, data.low_stock_items);
  if (iv) flashNum(iv, data.inventory_value + ' Rs');
  if (rs) flashNum(rs, data.reserved_stock + ' Units');
  if (badge) badge.textContent = data.total + ' Products';
}

// ── Fetch + render (search or full reload) ─────────────────────
async function fetchAndRender(q = '') {
  try {
    const url = '/api/products/search' + (q ? `?q=${encodeURIComponent(q)}` : '');
    const res  = await fetch(url, { credentials: 'same-origin' });
    if (!res.ok) throw new Error('fetch failed');
    const data = await res.json();
    renderTable(data.products);
    updateStats(data);
  } catch (e) {
    console.error('[Stock] fetch error', e);
  }
}

// ── Debounced search ──────────────────────────────────────────
let searchTimer = null;
document.getElementById('searchInput').addEventListener('input', function () {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => fetchAndRender(this.value.trim()), 300);
});

// ═══════════════════════════════════════════════════════════════
// ADD PRODUCT MODAL
// ═══════════════════════════════════════════════════════════════
document.getElementById('btnAddProduct').addEventListener('click', () => {
  document.getElementById('addCode').value = '';
  document.getElementById('addName').value = '';
  document.getElementById('addCost').value = '';
  document.getElementById('addError').classList.add('hidden');
  openModal('modalAddProduct');
});

['closeAddModal', 'cancelAdd', 'backdropAdd'].forEach(id => {
  document.getElementById(id).addEventListener('click', () => closeModal('modalAddProduct'));
});

document.getElementById('submitAdd').addEventListener('click', async () => {
  const btn  = document.getElementById('submitAdd');
  const errEl = document.getElementById('addError');
  const code = document.getElementById('addCode').value.trim();
  const name = document.getElementById('addName').value.trim();
  const cost = document.getElementById('addCost').value;

  if (!code || !name) {
    errEl.textContent = 'Product code and name are required.';
    errEl.classList.remove('hidden');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="material-symbols-outlined text-[18px] spin-icon">sync</span> Saving…';

  try {
    const res  = await fetch('/api/product/add', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ product_code: code, name, unit_cost: cost || 0 }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalAddProduct');
      showToast('Product added successfully!');
      await fetchAndRender(document.getElementById('searchInput').value.trim());
    } else {
      errEl.textContent = data.error || 'Failed to add product.';
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error. Please try again.';
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">add</span> Add Product';
  }
});

// ═══════════════════════════════════════════════════════════════
// EDIT PRODUCT MODAL
// ═══════════════════════════════════════════════════════════════
function openEditModal(id, name, cost) {
  document.getElementById('editProductId').value = id;
  document.getElementById('editName').value       = name;
  document.getElementById('editCost').value       = cost;
  document.getElementById('editError').classList.add('hidden');
  openModal('modalEditProduct');
}

['closeEditModal', 'cancelEdit', 'backdropEdit'].forEach(id => {
  document.getElementById(id).addEventListener('click', () => closeModal('modalEditProduct'));
});

document.getElementById('submitEdit').addEventListener('click', async () => {
  const btn     = document.getElementById('submitEdit');
  const errEl   = document.getElementById('editError');
  const pid     = document.getElementById('editProductId').value;
  const name    = document.getElementById('editName').value.trim();
  const cost    = document.getElementById('editCost').value;

  if (!name) {
    errEl.textContent = 'Product name is required.';
    errEl.classList.remove('hidden');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="material-symbols-outlined text-[18px] spin-icon">sync</span> Saving…';

  try {
    const res  = await fetch('/api/product/update', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ product_id: pid, name, unit_cost: cost }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalEditProduct');
      showToast('Product updated successfully!');
      await fetchAndRender(document.getElementById('searchInput').value.trim());
    } else {
      errEl.textContent = data.error || 'Failed to update product.';
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error. Please try again.';
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">save</span> Save Changes';
  }
});

// ═══════════════════════════════════════════════════════════════
// UPDATE STOCK MODAL
// ═══════════════════════════════════════════════════════════════
function openUpdateModal(id, name) {
  document.getElementById('updateProductId').value   = id;
  document.getElementById('updateProductName').textContent = name;
  document.getElementById('updateLocation').value   = '';
  document.getElementById('updateQty').value        = '';
  document.getElementById('updateError').classList.add('hidden');
  openModal('modalUpdateStock');
}

['closeUpdateModal', 'cancelUpdate', 'backdropUpdate'].forEach(id => {
  document.getElementById(id).addEventListener('click', () => closeModal('modalUpdateStock'));
});

document.getElementById('submitUpdate').addEventListener('click', async () => {
  const btn     = document.getElementById('submitUpdate');
  const errEl   = document.getElementById('updateError');
  const pid     = document.getElementById('updateProductId').value;
  const locId   = document.getElementById('updateLocation').value;
  const qty     = document.getElementById('updateQty').value;

  if (!locId) {
    errEl.textContent = 'Please select a location.';
    errEl.classList.remove('hidden');
    return;
  }
  if (qty === '' || Number(qty) < 0) {
    errEl.textContent = 'Please enter a valid quantity.';
    errEl.classList.remove('hidden');
    return;
  }

  btn.disabled = true;
  btn.innerHTML = '<span class="material-symbols-outlined text-[18px] spin-icon">sync</span> Updating…';

  try {
    const res  = await fetch('/api/stock/update', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ product_id: pid, location_id: locId, quantity: qty }),
      credentials: 'same-origin',
    });
    const data = await res.json();
    if (data.success) {
      closeModal('modalUpdateStock');
      showToast('Stock updated successfully!');
      await fetchAndRender(document.getElementById('searchInput').value.trim());
    } else {
      errEl.textContent = data.error || 'Failed to update stock.';
      errEl.classList.remove('hidden');
    }
  } catch (e) {
    errEl.textContent = 'Network error. Please try again.';
    errEl.classList.remove('hidden');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<span class="material-symbols-outlined text-[18px]">sync</span> Update Stock';
  }
});

// ── Bind Edit / Update buttons on table rows ──────────────────
function bindRowButtons() {
  document.querySelectorAll('.btn-edit').forEach(btn => {
    btn.addEventListener('click', () => {
      openEditModal(btn.dataset.id, btn.dataset.name, btn.dataset.cost);
    });
  });
  document.querySelectorAll('.btn-update').forEach(btn => {
    btn.addEventListener('click', () => {
      openUpdateModal(btn.dataset.id, btn.dataset.name);
    });
  });
}

// ── Init: bind buttons on first load (Jinja-rendered rows) ────
document.addEventListener('DOMContentLoaded', () => {
  bindRowButtons();
});