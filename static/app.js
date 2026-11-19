document.addEventListener("DOMContentLoaded", () => {
  // Menu hamburguesa en celulares
  const toggleBtn = document.getElementById("menu-toggle");
  const mainNav = document.getElementById("main-nav");
  if (toggleBtn && mainNav) {
    toggleBtn.addEventListener("click", () => {
      const isOpen = mainNav.classList.toggle("open");
      toggleBtn.setAttribute("aria-expanded", String(isOpen));
    });
  }

  // Buscador y filtros instantaneos de vacantes
  const searchInput = document.getElementById("filter-search");
  const catSelect = document.getElementById("filter-category");
  const langSelect = document.getElementById("filter-language");
  const expSelect = document.getElementById("filter-experience");
  const countrySelect = document.getElementById("filter-country");
  const resetBtn = document.getElementById("filter-reset");
  const countEl = document.getElementById("results-count");
  const emptyEl = document.getElementById("empty-state");
  const cards = Array.from(document.querySelectorAll(".job-card"));

  if (!cards.length) return;

  const normalize = (str) =>
    (str || "")
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");

  function applyFilters() {
    const q = normalize(searchInput ? searchInput.value : "");
    const cat = normalize(catSelect ? catSelect.value : "");
    const lang = normalize(langSelect ? langSelect.value : "");
    const exp = normalize(expSelect ? expSelect.value : "");
    const country = normalize(countrySelect ? countrySelect.value : "");

    let visible = 0;

    cards.forEach((card) => {
      const text = normalize(card.dataset.search);
      const cats = normalize(card.dataset.categorias);
      const cardLang = normalize(card.dataset.idioma);
      const cardExp = normalize(card.dataset.experiencia);
      const cardCountries = normalize(card.dataset.paises);

      const matchQ = !q || text.includes(q);
      const matchCat = !cat || cats.includes(cat);
      const matchLang = !lang || cardLang.includes(lang);
      const matchExp = !exp || cardExp.includes(exp);
      const matchCountry =
        !country || cardCountries.includes(country) || cardCountries.includes("toda latam");

      if (matchQ && matchCat && matchLang && matchExp && matchCountry) {
        card.style.display = "";
        visible++;
      } else {
        card.style.display = "none";
      }
    });

    if (countEl) {
      countEl.textContent = `${visible} ${visible === 1 ? "vacante disponible" : "vacantes disponibles"}`;
    }
    if (emptyEl) {
      emptyEl.style.display = visible === 0 ? "block" : "none";
    }
  }

  [searchInput, catSelect, langSelect, expSelect, countrySelect].forEach((el) => {
    if (el) {
      el.addEventListener("input", applyFilters);
      el.addEventListener("change", applyFilters);
    }
  });

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      if (catSelect) catSelect.value = "";
      if (langSelect) langSelect.value = "";
      if (expSelect) expSelect.value = "";
      if (countrySelect) countrySelect.value = "";
      applyFilters();
    });
  }
});
