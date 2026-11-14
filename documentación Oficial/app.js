document.addEventListener("DOMContentLoaded", () => {
  // 1. Live search across all cards, rows and sections
  const searchInput = document.getElementById("docSearch");
  const searchable = document.querySelectorAll("[data-search]");
  if (searchInput) {
    searchInput.addEventListener("input", () => {
      const q = searchInput.value.trim().toLowerCase();
      searchable.forEach((el) => {
        const txt = (el.textContent + " " + (el.dataset.search || "")).toLowerCase();
        el.style.display = !q || txt.includes(q) ? "" : "none";
      });
    });
  }

  // 2. Interactive Tabs
  document.querySelectorAll("[data-tab-group]").forEach((group) => {
    const buttons = group.querySelectorAll(".tab-btn");
    const panels = group.querySelectorAll(".tab-panel");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = btn.dataset.tab;
        buttons.forEach((b) => b.classList.toggle("active", b === btn));
        panels.forEach((p) => p.classList.toggle("active", p.id === target));
      });
    });
  });

  // 2b. Category Filter Pills (e.g. Action Catalog)
  document.querySelectorAll("[data-filter-group]").forEach((group) => {
    const buttons = group.querySelectorAll("[data-filter]");
    const items = group.querySelectorAll("[data-cat]");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const cat = btn.dataset.filter;
        buttons.forEach((b) => b.classList.toggle("active", b === btn));
        items.forEach((item) => {
          item.style.display = cat === "all" || item.dataset.cat === cat ? "" : "none";
        });
      });
    });
  });

  // 3. Accordions
  document.querySelectorAll(".acc-head").forEach((head) => {
    head.addEventListener("click", () => {
      const item = head.parentElement;
      item.classList.toggle("open");
      const icon = head.querySelector(".acc-icon");
      if (icon) icon.textContent = item.classList.contains("open") ? "−" : "+";
    });
  });

  // 4. Copy Code Buttons
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const pre = btn.parentElement.querySelector("pre");
      if (!pre) return;
      try {
        await navigator.clipboard.writeText(pre.textContent);
        const orig = btn.textContent;
        btn.textContent = "Copiado ✓";
        setTimeout(() => (btn.textContent = orig), 1600);
      } catch {
        btn.textContent = "Error";
      }
    });
  });

  // 5. Image Lightbox Modal
  const modal = document.getElementById("imgModal");
  const modalImg = document.getElementById("modalImg");
  if (modal && modalImg) {
    document.querySelectorAll(".shot-card img").forEach((img) => {
      img.addEventListener("click", () => {
        modalImg.src = img.src;
        modal.classList.add("open");
      });
    });
    modal.addEventListener("click", () => modal.classList.remove("open"));
  }

  // 6. Active Sidebar Link on Scroll
  const links = document.querySelectorAll(".nav-link");
  const sections = [...document.querySelectorAll("main section")];
  window.addEventListener("scroll", () => {
    let current = sections[0]?.id || "";
    const pos = window.scrollY + 120;
    sections.forEach((sec) => {
      if (sec.offsetTop <= pos) current = sec.id;
    });
    links.forEach((l) => {
      l.classList.toggle("active", l.getAttribute("href") === "#" + current);
    });
  });
});
