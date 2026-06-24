# Programación Web ll — Segundo Parcial

| Nombre | Matrícula |
|--------|-----------|
| Matías Escobar | 151251 |

## Eventos Belgrano 

Sitio Django para salón de eventos y casamientos, con panel de administración propio, autenticación con validación por código, API REST (DRF) y consumo de API externa.

## 🛠️ Tecnologías Utilizadas
- Django 6 + Django REST Framework
- PostgreSQL
- Bootstrap 5 (UX/UI y Responsive Design)
- Whitenoise & Gunicorn (Producción)

## 🌐 APIs Externas Consumidas
- **Open-Meteo:** [https://api.open-meteo.com/v1/forecast](https://api.open-meteo.com/v1/forecast) 
  *(Consumida vía Backend con `requests` para mostrar el clima actual de Belgrano, CABA en la sección de Contacto).*
- **TheCocktailDB:** [https://www.thecocktaildb.com/api/json/v1/1/random.php](https://www.thecocktaildb.com/api/json/v1/1/random.php) 
  *(Consumida vía Frontend con `fetch` de JavaScript para sugerir tragos aleatorios en la página de Inicio).*

## 🔌 API Propia (DRF)
- `GET /api/consultas/` → Retorna el listado de solicitudes de contacto y reservas recibidas (Formato JSON).

## 🚀 Despliegue en Producción
El proyecto fue desplegado exitosamente utilizando Render y PostgreSQL.
- **Sitio Web:** [https://eventos-belgrano.onrender.com/](https://eventos-belgrano.onrender.com/)

## 🔐 Acceso al Dashboard

Para simular el proceso completo de registro y validación (con envío real de correo),
cloná el repositorio y ejecutalo en local con las credenciales SMTP del archivo `.env`.

- **Correo autorizado para pruebas:** annavillegas@live.com.ar
- **Código de validación:** WEB226
- **Flujo:** Registro (`/auth/registro/`) → revisar el correo recibido → Validar (`/auth/validar/`) → Login (`/auth/login/`)

En producción (Render), por las limitaciones del envío de correo saliente, se puede
acceder directamente con las credenciales ya validadas si el correo no llega a tiempo.