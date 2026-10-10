'use strict';
const columns = ['model_group', 'public_exam_auto', 'real_case_auto', 'citation', 'constraint', 'argument', 'public_exam_human', 'real_case_human'];
const columnLabels = {
  model_group: 'Model', public_exam_auto: 'Exam · automatic', real_case_auto: 'Case mean · automatic',
  citation: 'Citation', constraint: 'Constraint', argument: 'Argument',
  public_exam_human: 'Exam · human', real_case_human: 'Case · human'
};
const tbody = document.querySelector('#performance-table tbody');
const search = document.querySelector('#model-search');
const status = document.querySelector('#results-status');
let results = [];
let sortKey = null;
let sortAscending = false;

// Rank displayed values over the complete roster, never over a filtered view.
// Equal scores share a rank; second best means the next distinct score.
function scoreLeaders(data) {
  return Object.fromEntries(columns.slice(1).map(column => [column,
    [...new Set(data.map(row => Number(row[column].toFixed(1))))].sort((a, b) => b - a).slice(0, 2)
  ]));
}

function renderResults() {
  const query = search.value.trim().toLowerCase();
  const leaders = scoreLeaders(results);
  const rows = results.filter(row => row.model_group.toLowerCase().includes(query));
  if (sortKey) rows.sort((a, b) => {
    const comparison = sortKey === 'model_group' ? a[sortKey].localeCompare(b[sortKey]) : a[sortKey] - b[sortKey];
    return (sortAscending ? comparison : -comparison) || a.paper_order - b.paper_order;
  });
  tbody.replaceChildren();
  for (const row of rows) {
    const tr = document.createElement('tr');
    for (const column of columns) {
      const td = document.createElement(column === 'model_group' ? 'th' : 'td');
      td.textContent = column === 'model_group' ? row[column] : row[column].toFixed(1);
      if (column === 'model_group') {
        td.scope = 'row';
      } else {
        const rank = leaders[column].indexOf(Number(row[column].toFixed(1)));
        if (rank !== -1) {
          const label = rank === 0 ? 'Best' : 'Second best';
          td.classList.add(rank === 0 ? 'score-best' : 'score-second');
          td.title = `${label} displayed ${columnLabels[column].toLowerCase()} score across all ${results.length} model groups; ties share rank.`;
          const value = document.createElement('span');
          value.className = 'score-value';
          value.textContent = row[column].toFixed(1);
          const rankLabel = document.createElement('span');
          rankLabel.className = 'sr-only';
          rankLabel.textContent = ` (${label.toLowerCase()} in column)`;
          td.replaceChildren(value, rankLabel);
        }
      }
      tr.append(td);
    }
    tbody.append(tr);
  }
  status.textContent = rows.length ? `${rows.length} of ${results.length} model groups${sortKey ? ' · sorted by ' + columnLabels[sortKey] : ' · paper order'}` : 'No matching models. Try another name.';
  document.querySelectorAll('[data-sort]').forEach(button => {
    const th = button.closest('th');
    if (button.dataset.sort === sortKey) th.setAttribute('aria-sort', sortAscending ? 'ascending' : 'descending');
    else th.removeAttribute('aria-sort');
  });
}

fetch('data/results.json').then(response => {
  if (!response.ok) throw new Error('Results unavailable');
  return response.json();
}).then(data => { results = data; renderResults(); }).catch(() => {
  status.textContent = 'The interactive table could not load. The complete published results remain available in the CSV download.';
});
search.addEventListener('input', renderResults);
document.querySelectorAll('[data-sort]').forEach(button => button.addEventListener('click', () => {
  const next = button.dataset.sort;
  sortAscending = sortKey === next ? !sortAscending : next === 'model_group';
  sortKey = next;
  renderResults();
}));

const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
function selectTab(selected) {
  for (const tab of tabs) {
    const active = selected === tab;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
  }
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    let next = event.key === 'ArrowRight' ? (index + 1) % tabs.length : (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    tabs[next].focus();
    selectTab(tabs[next]);
  });
});

document.querySelectorAll('[data-expand-text]').forEach(button => {
  const module = button.closest('.text-module');
  const text = document.getElementById(button.getAttribute('aria-controls'));
  const expandLabel = button.textContent;
  module.classList.add('is-collapsible');
  const updateControl = () => {
    if (!module.getClientRects().length) return;
    button.hidden = text.scrollHeight <= Math.min(320, window.innerHeight * .45) + 1;
  };
  new ResizeObserver(updateControl).observe(text);
  window.addEventListener('resize', updateControl);
  updateControl();
  button.addEventListener('click', () => {
    const expanded = module.classList.toggle('is-expanded');
    button.setAttribute('aria-expanded', String(expanded));
    button.textContent = expanded ? 'Collapse' : expandLabel;
    if (!expanded && module.getBoundingClientRect().top < 0) module.scrollIntoView({block: 'start'});
  });
});

document.querySelector('#copy-citation').addEventListener('click', async () => {
  const output = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(document.querySelector('#bibtex').textContent);
    output.textContent = 'BibTeX copied.';
  } catch {
    const range = document.createRange();
    range.selectNodeContents(document.querySelector('#bibtex'));
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    output.textContent = 'Citation selected. Use your browser’s Copy command.';
  }
});
