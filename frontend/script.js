const API = 'http://127.0.0.1:8000';

const themeToggle = document.getElementById('themeToggle');
const themeIcon = themeToggle.querySelector('.theme-icon');

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  themeIcon.textContent = theme === 'dark' ? '☽' : '☀';
  localStorage.setItem('flo-theme', theme);
}

themeToggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
});

setTheme(localStorage.getItem('flo-theme') || 'light');

const navBtns = document.querySelectorAll('.nav-btn');
const views   = document.querySelectorAll('.view');

navBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    navBtns.forEach(b => b.classList.remove('active'));
    views.forEach(v => v.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`view-${btn.dataset.view}`).classList.add('active');
    if (btn.dataset.view === 'dashboard') loadDashboard();
    if (btn.dataset.view === 'expenses') loadExpenses();
  });
});

let toastTimer;
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.remove('hidden');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add('hidden'), 2800);
}

async function api(path, method = 'GET', body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API}${path}`, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

function fmtAmount(n) {
  return `R ${parseFloat(n).toFixed(2)}`;
}

function fmtDate(str) {
  if (!str) return '—';
  const d = new Date(str);
  return d.toLocaleDateString('en-ZA', { day: 'numeric', month: 'short', year: 'numeric' });
}

function buildRows(expenses, includeActions = true) {
  if (!expenses || expenses.length === 0) {
    const cols = includeActions ? 5 : 4;
    return `<tr><td colspan="${cols}" class="empty-cell">No expenses found.</td></tr>`;
  }
  return expenses.map(e => `
    <tr data-id="${e.id}">
      <td>${e.name}</td>
      <td><span class="category-badge">${e.category}</span></td>
      <td class="amount-cell">${fmtAmount(e.amount)}</td>
      <td class="date-cell">${fmtDate(e.date)}</td>
      ${includeActions ? `
        <td>
          <button class="btn-icon" onclick="openEdit('${e.id}','${e.name}',${e.amount},'${e.category}')">✎</button>
          <button class="btn-icon delete" onclick="deleteExpense('${e.id}')">✕</button>
        </td>` : '<td></td>'}
    </tr>
  `).join('');
}

async function loadDashboard() {
  try {
    const [expData, summaryData] = await Promise.all([
      api('/expenses'),
      api('/expenses/summary')
    ]);

    const expenses = expData.expenses || [];
    const total = expenses.reduce((s, e) => s + parseFloat(e.amount), 0);

    document.getElementById('totalSpent').textContent = fmtAmount(total);
    document.getElementById('totalExpenses').textContent = expenses.length;

    // Category breakdown from summary
    const cats = summaryData.spending_by_category || {};
    const catEntries = Object.entries(cats);
    document.getElementById('totalCategories').textContent = catEntries.length;

    const maxVal = Math.max(...catEntries.map(([, v]) => v), 1);
    const catList = document.getElementById('categoryList');

    if (catEntries.length === 0) {
      catList.innerHTML = `<div class="empty-state">No data yet. Add some expenses.</div>`;
      return;
    }

    catList.innerHTML = catEntries
      .sort((a, b) => b[1] - a[1])
      .map(([name, amount]) => `
        <div class="category-row">
          <span class="cat-name">${name}</span>
          <div class="cat-bar-wrap">
            <div class="cat-bar" style="width: ${(amount / maxVal * 100).toFixed(1)}%"></div>
          </div>
          <span class="cat-amount">${fmtAmount(amount)}</span>
        </div>
      `).join('');
  } catch (e) {
    toast('Could not load dashboard — is the API running?');
  }
}

let allExpenses = [];

async function loadExpenses() {
  try {
    const data = await api('/expenses');
    allExpenses = data.expenses || [];
    renderExpenseTable(allExpenses);
  } catch (e) {
    toast('Could not load expenses.');
  }
}

function renderExpenseTable(expenses) {
  document.getElementById('expenseTableBody').innerHTML = buildRows(expenses);
}

// Search
document.getElementById('searchInput').addEventListener('input', async function () {
  const q = this.value.trim();
  if (!q) { renderExpenseTable(allExpenses); return; }
  try {
    const data = await api(`/expenses/search?q=${encodeURIComponent(q)}`);
    renderExpenseTable(data.expenses || []);
  } catch {
    renderExpenseTable([]);
  }
});

// Add expense
document.getElementById('addBtn').addEventListener('click', async () => {
  const name     = document.getElementById('expenseName').value.trim();
  const amount   = document.getElementById('expenseAmount').value.trim();
  const category = document.getElementById('expenseCategory').value.trim();
  const errEl    = document.getElementById('formError');

  if (!name || !amount || !category) {
    errEl.classList.remove('hidden');
    return;
  }
  errEl.classList.add('hidden');

  try {
    await api('/expenses', 'POST', { name, amount: parseFloat(amount), category });
    document.getElementById('expenseName').value = '';
    document.getElementById('expenseAmount').value = '';
    document.getElementById('expenseCategory').value = '';
    toast('Expense added ✓');
    await loadExpenses();
  } catch (e) {
    toast(`Error: ${e.message}`);
  }
});

// Delete
async function deleteExpense(id) {
  if (!confirm('Delete this expense?')) return;
  try {
    await api(`/expenses/${id}`, 'DELETE');
    toast('Expense deleted.');
    await loadExpenses();
  } catch (e) {
    toast(`Error: ${e.message}`);
  }
}

function openEdit(id, name, amount, category) {
  document.getElementById('editId').value = id;
  document.getElementById('editName').value = name;
  document.getElementById('editAmount').value = amount;
  document.getElementById('editCategory').value = category;
  document.getElementById('editModal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('editModal').classList.add('hidden');
}

document.getElementById('closeModal').addEventListener('click', closeModal);
document.getElementById('cancelEdit').addEventListener('click', closeModal);
document.getElementById('editModal').addEventListener('click', e => {
  if (e.target === document.getElementById('editModal')) closeModal();
});

document.getElementById('saveEdit').addEventListener('click', async () => {
  const id       = document.getElementById('editId').value;
  const name     = document.getElementById('editName').value.trim();
  const amount   = parseFloat(document.getElementById('editAmount').value);
  const category = document.getElementById('editCategory').value.trim();

  if (!name || isNaN(amount) || !category) { toast('Please fill in all fields.'); return; }

  try {
    await api(`/expenses/${id}`, 'PUT', { name, amount, category });
    toast('Expense updated ✓');
    closeModal();
    await loadExpenses();
  } catch (e) {
    toast(`Error: ${e.message}`);
  }
});

document.querySelectorAll('.filter-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.filter-panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(`filter-${tab.dataset.filter}`).classList.add('active');
  });
});

async function applyFilter(type) {
  let path;
  try {
    if (type === 'category') {
      const cat = document.getElementById('filterCategory').value.trim();
      if (!cat) { toast('Enter a category.'); return; }
      path = `/expenses/filter?category=${encodeURIComponent(cat)}`;
    } else if (type === 'month') {
      const month = document.getElementById('filterMonth').value;
      const year  = document.getElementById('filterYear').value;
      if (!month || !year) { toast('Enter month and year.'); return; }
      path = `/expenses/filter?month=${month}&year=${year}`;
    } else if (type === 'range') {
      const start = document.getElementById('filterStart').value;
      const end   = document.getElementById('filterEnd').value;
      if (!start || !end) { toast('Select both dates.'); return; }
      path = `/expenses/filter?start_date=${start}&end_date=${end}`;
    }

    const data = await api(path);
    const expenses = data.expenses || [];
    document.getElementById('filterTableBody').innerHTML = buildRows(expenses, false);
  } catch (e) {
    toast(`Error: ${e.message}`);
    document.getElementById('filterTableBody').innerHTML =
      `<tr><td colspan="4" class="empty-cell">No results found.</td></tr>`;
  }
}

loadDashboard();
loadExpenses();