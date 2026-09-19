const TOKEN_KEY = "attckdef_token";
const USER_KEY = "attckdef_user";

function getToken() { return localStorage.getItem(TOKEN_KEY) || ""; }

async function apiFetch(path, opts = {}) {
  opts.headers = Object.assign({}, opts.headers);
  const t = getToken();
  if (t) opts.headers["Authorization"] = "Bearer " + t;
  if (opts.body && typeof opts.body === "string") {
    opts.headers["Content-Type"] = "application/json";
  }
  return fetch(path, opts);
}

function refreshNav() {
  const u = localStorage.getItem(USER_KEY);
  const navAuth = document.getElementById("nav-auth");
  const tag = document.getElementById("session-tag");
  if (u && navAuth) {
    navAuth.innerHTML = `<a href="/service/notes">${u}</a> · <a href="#" id="logout">sign out</a>`;
    const lo = document.getElementById("logout");
    if (lo) lo.onclick = async (e) => {
      e.preventDefault();
      await apiFetch("/api/logout", { method: "POST" });
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      location.href = "/";
    };
  }
  if (tag) tag.textContent = u ? "notestore session: " + u : "no notestore session";
}

async function wireForm(formId, url, outId) {
  const form = document.getElementById(formId);
  const out = document.getElementById(outId);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    const r = await apiFetch(url, { method: "POST", body: JSON.stringify(data) });
    const j = await r.json().catch(() => ({}));
    out.textContent = "HTTP " + r.status + "\n" + JSON.stringify(j, null, 2);
    if (r.ok && j.token) {
      localStorage.setItem(TOKEN_KEY, j.token);
      localStorage.setItem(USER_KEY, j.username);
      refreshNav();
    }
  });
}

let tickLeft = 0;
async function syncClock() {
  try {
    const r = await fetch("/api/game/status");
    const j = await r.json();
    document.getElementById("tick-now").textContent = j.current_tick;
    tickLeft = j.seconds_remaining;
    updateTickBar(j.tick_seconds);
  } catch (e) {}
}
function updateTickBar(total) {
  const fill = document.getElementById("tick-fill");
  const left = document.getElementById("tick-left");
  if (!fill || !left) return;
  fill.style.width = Math.max(0, 100 * (1 - tickLeft / total)) + "%";
  left.textContent = tickLeft + "s";
}
setInterval(() => { if (tickLeft > 0) { tickLeft--; updateTickBar(120); } else syncClock(); }, 1000);
syncClock();

refreshNav();
