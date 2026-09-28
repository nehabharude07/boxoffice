const $ = (id) => document.getElementById(id);
const form = $("form");

const usd = (n) => {
  const a = Math.abs(n), s = n < 0 ? "-" : "";
  if (a >= 1e9) return `${s}$${(a / 1e9).toFixed(2)}B`;
  if (a >= 1e6) return `${s}$${(a / 1e6).toFixed(1)}M`;
  return `${s}$${Math.round(a).toLocaleString()}`;
};

// Show a readable version of large numbers under each money field
const money = ["budget", "opening_revenue", "domestic_revenue"];
money.forEach((name) => {
  const input = form.elements[name], hint = document.querySelector(`[data-for="${name}"]`);
  input.addEventListener("input", () => (hint.textContent = input.value ? usd(+input.value) : ""));
});

$("sample").addEventListener("click", () => {
  Object.entries(window.SAMPLE || {}).forEach(([k, v]) => {
    form.elements[k].value = Math.round(v);
    form.elements[k].dispatchEvent(new Event("input"));
  });
  if (!form.elements.title.value) form.elements.title.value = "Untitled Feature";
});

function countUp(el, to) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return (el.textContent = usd(to));
  const t0 = performance.now(), dur = 900;
  const tick = (t) => {
    const p = Math.min(1, (t - t0) / dur);
    el.textContent = usd(to * (1 - Math.pow(1 - p, 3)));
    if (p < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}

function showError(msg, field) {
  const box = $("error");
  box.textContent = msg || "";
  box.hidden = !msg;
  form.querySelectorAll("input").forEach((i) => i.classList.toggle("bad", i.name === field));
  if (field) form.elements[field].focus();
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  showError("");
  const btn = form.querySelector(".go");
  btn.disabled = true;
  btn.textContent = "Printing…";
  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    const r = await res.json();
    if (!res.ok) return showError(r.error, r.field);

    $("t-label").textContent = "Admit one";
    $("t-title").textContent = r.title;
    $("t-sub").textContent = "Predicted worldwide gross";
    countUp($("t-gross"), r.prediction);

    const max = Math.max(r.high, r.prediction) * 1.08 || 1;
    $("band").style.left = (r.low / max) * 100 + "%";
    $("band").style.width = ((r.high - r.low) / max) * 100 + "%";
    $("pin").style.left = `calc(${(r.prediction / max) * 100}% - 2px)`;
    $("lo").textContent = `Likely low ${usd(r.low)}`;
    $("hi").textContent = `Likely high ${usd(r.high)}`;
    $("range").hidden = false;

    const p = $("t-profit");
    p.textContent = (r.profit >= 0 ? "+" : "") + usd(r.profit);
    p.classList.toggle("neg", r.profit < 0);
    $("t-multiple").textContent = r.multiple.toFixed(2) + "× budget";

    const t = $("ticket");
    t.classList.remove("printed");
    void t.offsetWidth; // restart animation
    t.classList.add("printed");
  } catch {
    showError("Couldn't reach the server. Check that the app is still running and try again.");
  } finally {
    btn.disabled = false;
    btn.textContent = "Print my forecast";
  }
});
