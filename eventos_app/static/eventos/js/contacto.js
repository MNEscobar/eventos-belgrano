/* ═══════════════════════════════════════════════════════════
   EVENTOS BELGRANO — JAVASCRIPT: CONTACTO & VALIDACIONES
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function() {
    
    // ── 1. ANIMACIÓN DE CAMPOS DEL FORMULARIO
    document.querySelectorAll('.eb-input').forEach(input => {
        // Cuando el usuario entra al campo
        input.addEventListener('focus', () => {
            input.closest('.col-md-6, .mb-3, .mb-4')?.classList.add('eb-field-active');
        });
        
        // Cuando el usuario sale del campo
        input.addEventListener('blur', () => {
            input.closest('.col-md-6, .mb-3, .mb-4')?.classList.remove('eb-field-active');
        });
    });

    // ── 2. VALIDACIÓN DEL FORMULARIO EN FRONTEND 
    const form = document.querySelector('form');
    
    // Verificamos si existe el formulario en esta vista
    if (form) {
        // Capturamos los inputs por los IDs que genera Django automáticamente
        const nombreInput = document.getElementById('id_nombre');
        const emailInput = document.getElementById('id_email');
        const telefonoInput = document.getElementById('id_telefono');
        const fechaInput = document.getElementById('id_fecha_evento');
        const invitadosInput = document.getElementById('id_cantidad_invitados');
        const mensajeInput = document.getElementById('id_mensaje');

        form.addEventListener('submit', function(event) {
            let isValid = true;
            let errorMessage = '';

            // Limpiamos estilos de error anteriores de Bootstrap
            const inputs = [nombreInput, emailInput, telefonoInput, fechaInput, invitadosInput, mensajeInput];
            inputs.forEach(input => {
                if (input) {
                    input.classList.remove('is-invalid');
                }
            });

            // Validación: Nombre vacío
            if (nombreInput && nombreInput.value.trim() === '') {
                isValid = false;
                nombreInput.classList.add('is-invalid');
                errorMessage += '• El nombre completo es obligatorio.\n';
            }

            // Validación: Formato de Email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (emailInput && (!emailRegex.test(emailInput.value.trim()) || emailInput.value.trim() === '')) {
                isValid = false;
                emailInput.classList.add('is-invalid');
                errorMessage += '• Ingrese un correo electrónico válido (ej: usuario@dominio.com).\n';
            }

            // Validación: Fecha vacía o pasada
            if (fechaInput) {
                if (fechaInput.value.trim() === '') {
                    isValid = false;
                    fechaInput.classList.add('is-invalid');
                    errorMessage += '• Debe seleccionar una fecha tentativa para el evento.\n';
                } else {
                    // Obtenemos la fecha seleccionada
                    const fechaSeleccionada = new Date(fechaInput.value);
                            // Obtenemos la fecha de hoy a las 00:00 para comparar solo el calendario
                            const hoy = new Date();
                            hoy.setHours(0, 0, 0, 0);
        
                            // Ajustamos la zona horaria del input para evitar desfases de UTC
                            fechaSeleccionada.setMinutes(fechaSeleccionada.getMinutes() + fechaSeleccionada.getTimezoneOffset());
                            if (fechaSeleccionada < hoy) {
                                isValid = false;
                                fechaInput.classList.add('is-invalid');
                                errorMessage += '• La fecha del evento no puede ser una fecha pasada.\n';
                            }
                        }
                    }

            // Validación: Cantidad de invitados (Mínimo 1)
            if (invitadosInput && (invitadosInput.value.trim() === '' || parseInt(invitadosInput.value) < 1)) {
                isValid = false;
                invitadosInput.classList.add('is-invalid');
                errorMessage += '• La cantidad de invitados debe ser un número válido mayor a 0.\n';
            }

            // Validación: Mensaje (Mínimo 10 caracteres)
            if (mensajeInput && mensajeInput.value.trim().length < 10) {
                isValid = false;
                mensajeInput.classList.add('is-invalid');
                errorMessage += '• El mensaje debe contener al menos 10 caracteres detallando su consulta.\n';
            }

            // Si hay errores, frenamos el envío del formulario y mostramos alerta
            if (!isValid) {
                event.preventDefault(); // ¡Evita la recarga de página y el viaje al servidor!
                alert("Atención - Eventos Belgrano:\n\nPor favor, corrija los siguientes errores antes de enviar su consulta:\n\n" + errorMessage);
            }
        });

        // ── 3. LÓGICA DINÁMICA DEL CLIMA (API EXTERNA) ───────────────────
        const climaValueEl = document.getElementById('eb-clima-value');
        const climaIconEl = document.getElementById('eb-clima-icon');

        // Programación defensiva: Solo se ejecuta si el widget del clima está en pantalla
        if (climaValueEl && climaIconEl) {
            // Leemos el valor numérico exacto desde el atributo data-temp
            const temperatura = parseFloat(climaValueEl.getAttribute('data-temp'));
            if (!isNaN(temperatura)) {
                // Lógica de negocio: 24°C o más se considera un día cálido/caluroso
            if (temperatura >= 24) {
                // Aplicamos colores cálidos (anaranjado)
                climaValueEl.classList.add('eb-temp-calido');
                climaIconEl.classList.add('eb-temp-calido');
                
                // UX Extra: Cambiamos el icono a un Sol radiante
                climaIconEl.classList.remove('bi-cloud-sun');
                climaIconEl.classList.add('bi-sun');
            } else {
                // Aplicamos colores templados/fríos
                climaValueEl.classList.add('eb-temp-templado');
                climaIconEl.classList.add('eb-temp-templado');
                
                // Dejamos el icono de sol y nubes
                }
            }
        }
    }
});