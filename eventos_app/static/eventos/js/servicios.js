/* ═══════════════════════════════════════════════════════════
   EVENTOS BELGRANO — JAVASCRIPT: SERVICIOS
   ═══════════════════════════════════════════════════════════ */

// Seleccionamos todos los paquetes
const paquetes = document.querySelectorAll('.eb-paquete-card');

paquetes.forEach(paquete => {
    paquete.addEventListener('click', function() {
        
        // 1. Limpieza: Le quitamos la clase 'featured' a todos los paquetes
        paquetes.forEach(p => {
            p.classList.remove('eb-paquete-featured');
            
            // Regresamos todos los botones al diseño secundario (outline oscuro)
            const btn = p.querySelector('.eb-pk-footer a');
            if (btn) {
                btn.classList.remove('eb-btn-primary');
                btn.classList.add('eb-btn-outline-dark');
            }
        });

        // 2. Activación: Le agregamos la clase 'featured' al paquete clickeado
        this.classList.add('eb-paquete-featured');
        
        // Convertimos el botón de este paquete específico en principal (dorado)
        const btnDestacado = this.querySelector('.eb-pk-footer a');
        if (btnDestacado) {
            btnDestacado.classList.remove('eb-btn-outline-dark');
            btnDestacado.classList.add('eb-btn-primary');
        }
    });
});