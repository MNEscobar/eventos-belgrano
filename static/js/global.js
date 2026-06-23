/* ═══════════════════════════════════════════════════════════
   EVENTOS BELGRANO — JAVASCRIPT GLOBAL
   ═══════════════════════════════════════════════════════════ */

// ── NAVBAR SCROLL EFFECT ─────────────────────────────────
const navbar = document.getElementById('mainNavbar');

// Nos aseguramos de que el elemento exista para evitar errores
if (navbar) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}