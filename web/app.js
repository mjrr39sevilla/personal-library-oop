// ---------- Model (same design as the Python OOP version) ----------
class Book {
  constructor(title, author, dateRead = null, copies = 1) {
    this.id = Math.random().toString(36).slice(2, 10);
    this.title = title.trim();
    this.author = author.trim();
    this.dateRead = dateRead;
    this.copies = copies;
  }
  get isRead() {
    return !!this.dateRead;
  }
  get key() {
    return this.title
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, " ");
  }
}

class Library {
  constructor() {
    this.books = [];
  }
  add(title, author) {
    if (!title.trim()) return;
    this.books.push(new Book(title, author || "Desconocido"));
  }
  find(id) {
    return this.books.find((b) => b.id === id);
  }
  editTitle(id, t) {
    const b = this.find(id);
    if (b && t.trim()) b.title = t.trim();
  }
  remove(id) {
    this.books = this.books.filter((b) => b.id !== id);
  }
  markRead(id, date) {
    const b = this.find(id);
    if (b) b.dateRead = date || new Date().toISOString().slice(0, 10);
  }
  sorted(list) {
    return [...list].sort((a, b) => a.title.localeCompare(b.title, "es"));
  }
  read() {
    return this.sorted(this.books.filter((b) => b.isRead));
  }
  pending() {
    return this.sorted(this.books.filter((b) => !b.isRead));
  }

  duplicates() {
    const count = {};
    this.books.forEach((b) => {
      count[b.key] = (count[b.key] || 0) + 1;
    });
    return this.sorted(
      this.books.filter((b) => b.copies > 1 || count[b.key] > 1),
    );
  }

  load(arr) {
    this.books = arr
      .map((o) => {
        const read = o.status
          ? o.status === "read"
          : !!(o.date_read || o.dateRead);
        const date = read ? o.date_read || o.dateRead || "2022-01-01" : null;
        return new Book(
          o.title || "",
          o.author || "Desconocido",
          date,
          Number(o.copies) || 1,
        );
      })
      .filter((b) => b.title);
  }

  toJSON() {
    return this.books.map((b) => ({
      title: b.title,
      author: b.author,
      status: b.isRead ? "read" : "pending",
      copies: b.copies,
      date_read: b.dateRead,
    }));
  }
}

// ---------- App ----------
const lib = new Library();
const demo = [
  ["Los asesinos del emperador", "Santiago Posteguillo", "2022-01-01"],
  ["Circo Máximo", "Santiago Posteguillo", "2023-03-14"],
  ["La legión perdida", "Santiago Posteguillo", null],
  ["Yo, Julia", "Santiago Posteguillo", null],
  ["Circo Máximo", "Santiago Posteguillo", null],
  ["Africanus. El hijo del cónsul", "Santiago Posteguillo", "2024-06-02"],
];
demo.forEach((d) => {
  lib.add(d[0], d[1]);
  lib.books.at(-1).dateRead = d[2];
});
try {
  const s = localStorage.getItem("pl");
  if (s) lib.load(JSON.parse(s));
} catch (e) {}
let tab = "read",
  q = "";
const $ = (id) => document.getElementById(id);
const esc = (s) =>
  s.replace(
    /[&<>"]/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c],
  );
const save = () => {
  try {
    localStorage.setItem("pl", JSON.stringify(lib.toJSON()));
  } catch (e) {}
  render();
};
const tabs = {
  read: "Leídos",
  pending: "Pendientes",
  dup: "Duplicados",
  year: "Por año",
};
function render() {
  const r = lib.read(),
    p = lib.pending(),
    d = lib.duplicates();
  $("stats").innerHTML = [
    [lib.books.length, "Total"],
    [r.length, "Leídos"],
    [p.length, "Pendientes"],
    [d.length, "Duplicados"],
  ]
    .map((s) => `<div class="st"><b>${s[0]}</b><small>${s[1]}</small></div>`)
    .join("");
  $("tabs").innerHTML = Object.entries(tabs)
    .map(
      ([k, v]) =>
        `<button class="${k === tab ? "on" : ""}" data-t="${k}">${v}</button>`,
    )
    .join("");
  const f = (l) =>
    l.filter((b) => (b.title + b.author).toLowerCase().includes(q));
  let html = "";
  if (tab === "year") {
    const by = {};
    r.forEach((b) =>
      (by[b.dateRead.slice(0, 4)] = by[b.dateRead.slice(0, 4)] || []).push(b),
    );
    const ys = Object.keys(by).sort().reverse();
    html =
      ys
        .map(
          (y) =>
            `<div class="az">${y} · ${by[y].length} libros</div>` +
            f(by[y]).map(card).join(""),
        )
        .join("") || "";
  } else
    html = f(tab === "read" ? r : tab === "pending" ? p : d)
      .map(card)
      .join("");
  $("list").innerHTML =
    html || '<div class="empty">No hay libros aquí todavía 📚</div>';
}
function card(b) {
  const dup = lib.duplicates().includes(b);
  return `<div class="book ${b.isRead ? "" : "p"} ${dup && tab === "dup" ? "d" : ""}" data-id="${b.id}">
  <div class="t">${esc(b.title)}</div><div class="a">${esc(b.author)} ${b.copies > 1 ? `<span class="tag">${b.copies} copias</span>` : ""} ${b.isRead ? `· <span class="tag">leído ${b.dateRead}</span>` : '<span class="tag">pendiente</span>'}</div>
  <div class="act">${b.isRead ? "" : `<input type="date" class="dt"><button class="btn" data-a="read">Marcar leído</button>`}
  <button class="btn g" data-a="edit">Editar título</button><button class="btn r" data-a="del">Dar de baja</button></div></div>`;
}
document.addEventListener("click", (e) => {
  const t = e.target.closest("[data-t]");
  if (t) {
    tab = t.dataset.t;
    render();
    return;
  }
  const a = e.target.dataset.a;
  if (!a) return;
  const el = e.target.closest(".book"),
    id = el.dataset.id;
  if (a === "read") lib.markRead(id, el.querySelector(".dt").value);
  if (a === "edit") {
    const n = prompt("Nuevo título:", lib.find(id).title);
    if (n) lib.editTitle(id, n);
  }
  if (a === "del" && confirm("¿Dar de baja este libro?")) lib.remove(id);
  save();
});
$("addb").onclick = () => {
  lib.add($("nt").value, $("na").value);
  $("nt").value = $("na").value = "";
  tab = "pending";
  save();
};
$("q").oninput = (e) => {
  q = e.target.value.toLowerCase();
  render();
};
$("exp").onclick = () => {
  const w = window.open("", "_blank");
  if (w) {
    w.document.write(
      "<pre>" + esc(JSON.stringify(lib.toJSON(), null, 2)) + "</pre>",
    );
  }
};
$("imp").onclick = () => $("file").click();
$("file").onchange = (e) => {
  const f = e.target.files[0];
  if (!f) return;
  const r = new FileReader();
  r.onload = () => {
    try {
      const j = JSON.parse(r.result);
      lib.load(Array.isArray(j) ? j : j.books || []);
      save();
    } catch (x) {
      alert("JSON no válido");
    }
  };
  r.readAsText(f);
};
render();
