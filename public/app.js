async function api(path, options = {}) {
  const res = await fetch(path, {
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  let data = null;
  try {
    data = await res.json();
  } catch (e) {
    // ignore
  }

  if (!res.ok) {
    const message = data && data.error ? data.error : 'Something went wrong.';
    throw new Error(message);
  }

  return data;
}

function $(selector) {
  return document.querySelector(selector);
}

function createMushroomCard(m) {
  const card = document.createElement('article');
  card.className = 'mushroom-card';

  const label = document.createElement('div');
  label.className = 'mushroom-card__label';

  const ed = m.edibility.toLowerCase();
  if (ed.includes('toxic')) {
    label.classList.add('mushroom-card__label--toxic');
  } else if (ed.includes('choice')) {
    label.classList.add('mushroom-card__label--choice');
  } else {
    label.classList.add('mushroom-card__label--edible');
  }

  label.textContent = m.edibility;

  const title = document.createElement('h3');
  title.className = 'mushroom-card__title';
  title.textContent = m.name;

  const latin = document.createElement('p');
  latin.className = 'mushroom-card__latin';
  latin.textContent = m.latinName;

  const meta = document.createElement('div');
  meta.className = 'mushroom-card__meta';

  const habitat = document.createElement('div');
  habitat.className = 'mushroom-chip mushroom-chip--habitat';
  habitat.innerHTML = `<span class="mushroom-chip__dot"></span><span>${m.habitat}</span>`;

  const color = document.createElement('div');
  color.className = 'mushroom-chip mushroom-chip--color';
  color.innerHTML = `<span class="mushroom-chip__dot"></span><span>${m.color}</span>`;

  const vibe = document.createElement('div');
  vibe.className = 'mushroom-chip mushroom-chip--vibe';
  vibe.innerHTML = `<span class="mushroom-chip__dot"></span><span>${m.vibe}</span>`;

  meta.appendChild(habitat);
  meta.appendChild(color);
  meta.appendChild(vibe);

  const desc = document.createElement('p');
  desc.className = 'mushroom-card__description';
  desc.textContent = m.description;

  card.appendChild(label);
  card.appendChild(title);
  card.appendChild(latin);
  card.appendChild(meta);
  card.appendChild(desc);

  return card;
}

async function loadMushrooms() {
  const grid = $('#mushroomGrid');
  grid.innerHTML = '';

  try {
    const { mushrooms } = await api('/api/mushrooms');
    mushrooms.forEach((m) => {
      grid.appendChild(createMushroomCard(m));
    });
  } catch (e) {
    const error = document.createElement('p');
    error.textContent = 'Could not load mushrooms. The forest is sleepy.';
    grid.appendChild(error);
  }
}

function updateUserStatus(user) {
  const userStatus = $('#userStatus');
  const loginLink = $('#loginLink');
  const logoutBtn = $('#logoutBtn');

  if (user) {
    userStatus.classList.remove('user-status--logged-out');
    userStatus.classList.add('user-status--logged-in');
    userStatus.innerHTML = `<span class="user-status__greeting">Welcome,</span> <span class="user-status__name">${user.displayName}</span>`;
    if (loginLink) {
      loginLink.style.display = 'none';
    }
    logoutBtn.style.display = 'inline-flex';
  } else {
    userStatus.classList.add('user-status--logged-out');
    userStatus.classList.remove('user-status--logged-in');
    userStatus.innerHTML =
      '<span class="user-status__greeting">Guest wanderer</span>';
    if (loginLink) {
      loginLink.style.display = 'inline-flex';
    }
    logoutBtn.style.display = 'none';
  }
}

async function checkMe() {
  try {
    const { user } = await api('/api/me');
    updateUserStatus(user);
  } catch (e) {
    updateUserStatus(null);
  }
}

function setupLogoutButton() {
  const logoutBtn = $('#logoutBtn');

  logoutBtn.addEventListener('click', async () => {
    try {
      await api('/api/logout', { method: 'POST' });
    } catch (e) {
      // ignore
    }
    updateUserStatus(null);
  });
}

window.addEventListener('DOMContentLoaded', async () => {
  setupLogoutButton();
  await checkMe();
  await loadMushrooms();
});

