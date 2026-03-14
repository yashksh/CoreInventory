// CoreInventory – main.js

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 4 seconds
    document.querySelectorAll('.alert').forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // Generic table search (used on pages without server-side search)
    const genericSearch = document.getElementById('genericSearch');
    if (genericSearch) {
        const tableId = genericSearch.dataset.table;
        const table = document.getElementById(tableId);
        if (table) {
            genericSearch.addEventListener('input', function () {
                const q = this.value.toLowerCase();
                table.querySelectorAll('tbody tr').forEach(function (row) {
                    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
                });
            });
        }
    }

    // Confirm delete buttons
    document.querySelectorAll('[data-confirm]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Keep dropdown open on navbar active link
    document.querySelectorAll('.ci-navbar .nav-link.active.dropdown-toggle').forEach(function (link) {
        link.closest('.dropdown')?.classList.add('active');
    });

    // Highlight active nav item based on URL
    const path = window.location.pathname;
    document.querySelectorAll('.ci-navbar .nav-link').forEach(function (link) {
        if (link.getAttribute('href') === path) {
            link.classList.add('active');
        }
    });
});
