/* ═══════════════════════════════════════════════════════════
   EVENTOS BELGRANO — JAVASCRIPT: GALERÍA
   ═══════════════════════════════════════════════════════════ */

// ── FILTRO POR CATEGORÍA ─────────────────────────────────
const filtros   = document.querySelectorAll('.eb-filtro-btn');
const items     = document.querySelectorAll('.eb-gal-item');
const noResults = document.getElementById('noResults');

filtros.forEach(btn => {
    btn.addEventListener('click', () => {
        filtros.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filtro = btn.dataset.filter;
        let visibles = 0;

        items.forEach(item => {
            const match = filtro === 'todos' || item.dataset.categoria === filtro;
            if (match) {
                item.style.display = '';
                item.classList.add('eb-gal-visible');
                visibles++;
            } else {
                item.style.display = 'none';
                item.classList.remove('eb-gal-visible');
            }
        });

        noResults.classList.toggle('d-none', visibles > 0);
    });
});


// ── LIGHTBOX ─────────────────────────────────────────────
const lightbox   = document.getElementById('lightbox');
const backdrop   = document.getElementById('lightboxBackdrop');
const lbImg      = document.getElementById('lbImg');
const lbPlaceholder = document.getElementById('lbPlaceholder');
const lbCaption  = document.getElementById('lbCaption');
const lbClose    = document.getElementById('lbClose');
const lbPrev     = document.getElementById('lbPrev');
const lbNext     = document.getElementById('lbNext');

let currentIndex = 0;
let visibleCards = [];

function getVisibleCards() {
    return [...document.querySelectorAll('.eb-gal-item:not([style*="display: none"]) .eb-gal-card')];
}

function openLightbox(index) {
    visibleCards = getVisibleCards();
    currentIndex = index;
    showImage(currentIndex);
    if(lightbox && backdrop) {
        lightbox.classList.add('active');
        backdrop.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeLightbox() {
    if(lightbox && backdrop) {
        lightbox.classList.remove('active');
        backdrop.classList.remove('active');
        document.body.style.overflow = '';
    }
}

function showImage(index) {
    if(!visibleCards[index]) return;
    const card = visibleCards[index];
    const src  = card.dataset.src;
    const alt  = card.dataset.alt;
    const titulo = card.dataset.titulo;

    if(lbImg && lbCaption && lbPlaceholder) {
        lbImg.src = src;
        lbImg.alt = alt;
        lbCaption.textContent = titulo;

        lbImg.style.display = 'block';
        lbPlaceholder.style.display = 'none';

        lbImg.onerror = () => {
            lbImg.style.display = 'none';
            lbPlaceholder.style.display = 'flex';
        };
    }
}

document.querySelectorAll('.eb-gal-card').forEach((card, i) => {
    card.addEventListener('click', () => {
        visibleCards = getVisibleCards();
        const idx = visibleCards.indexOf(card);
        openLightbox(idx >= 0 ? idx : 0);
    });
});

if(lbClose) lbClose.addEventListener('click', closeLightbox);
if(backdrop) backdrop.addEventListener('click', closeLightbox);

if(lbNext) {
    lbNext.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % visibleCards.length;
        showImage(currentIndex);
    });
}

if(lbPrev) {
    lbPrev.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + visibleCards.length) % visibleCards.length;
        showImage(currentIndex);
    });
}

document.addEventListener('keydown', (e) => {
    if (!lightbox || !lightbox.classList.contains('active')) return;
    if (e.key === 'Escape')      closeLightbox();
    if (e.key === 'ArrowRight')  { currentIndex = (currentIndex + 1) % visibleCards.length; showImage(currentIndex); }
    if (e.key === 'ArrowLeft')   { currentIndex = (currentIndex - 1 + visibleCards.length) % visibleCards.length; showImage(currentIndex); }
});