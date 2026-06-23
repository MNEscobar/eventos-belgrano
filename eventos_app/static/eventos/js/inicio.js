/* ═══════════════════════════════════════════════════════════
   EVENTOS BELGRANO — JAVASCRIPT: INICIO & API
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function() {

    // ── 1. ANIMACIÓN DE ESTADÍSTICAS (INTERSECTION OBSERVER) ────
    const statNums = document.querySelectorAll('.eb-stat-num');

    // Programación defensiva: Solo inicializamos el observer si existen los elementos
    if (statNums.length > 0) {
        const observerStats = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-num');
                    observerStats.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        statNums.forEach(el => observerStats.observe(el));
    }

    // ── 2. CONSUMO DE API EXTERNA: CÓCTELES (REQ. 6) ─────────────────────
    const cocktailName = document.getElementById('api-cocktail-name');
    const cocktailDesc = document.getElementById('api-cocktail-desc');
    const cocktailImg = document.getElementById('api-cocktail-img');
    const loading = document.getElementById('api-loading');

    // Programación defensiva: Solo hacemos el fetch si estamos en la página de inicio
    if (cocktailName && cocktailDesc && cocktailImg && loading) {
        
        // Consumimos TheCocktailDB para un trago aleatorio
        fetch('https://www.thecocktaildb.com/api/json/v1/1/random.php')
            .then(response => {
                if (!response.ok) throw new Error('Error de red al conectar con la API');
                return response.json(); 
            })
            .then(data => {
                // La API devuelve un array "drinks", tomamos el primer resultado
                const drink = data.drinks[0];
                
                // Ocultamos el spinner
                loading.style.display = 'none';
                
                // Inyectamos la imagen
                cocktailImg.src = drink.strDrinkThumb;
                cocktailImg.style.display = 'block';
                
                // Inyectamos los textos
                cocktailName.innerHTML = drink.strDrink;
                cocktailDesc.innerHTML = `Categoría: <strong>${drink.strCategory}</strong> <br> Vaso sugerido: <strong>${drink.strGlass}</strong>`;
            })
            .catch(error => {
                console.error('Error fetching the API:', error);
                loading.style.display = 'none';
                cocktailName.innerHTML = 'Margarita Clásica';
                cocktailDesc.innerHTML = 'Un clásico infalible para cualquier celebración elegante.';
            });
    }
});