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

function setupSignupForm() {
  const form = $('#signupForm');
  const errorEl = $('#signupError');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorEl.textContent = '';

    const formData = new FormData(form);
    const displayName = formData.get('displayName');
    const username = formData.get('username');
    const password = formData.get('password');
    const confirmPassword = formData.get('confirmPassword');

    if (password !== confirmPassword) {
      errorEl.textContent = 'Passwords do not match.';
      return;
    }

    const payload = { displayName, username, password };

    try {
      await api('/api/signup', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      // On success, send them to the login page
      window.location.href = '/login';
    } catch (err) {
      errorEl.textContent = err.message;
    }
  });
}

window.addEventListener('DOMContentLoaded', () => {
  setupSignupForm();
});

