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

function setupLoginForm() {
  const form = $('#loginForm');
  const errorEl = $('#loginError');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorEl.textContent = '';

    const formData = new FormData(form);
    const payload = {
      username: formData.get('username'),
      password: formData.get('password'),
    };

    try {
      await api('/api/login', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      // On success, go back to the main mushroom page
      window.location.href = '/';
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  setupLoginForm();
});

