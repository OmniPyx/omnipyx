# Omnipyx Core

> Backend modular, extensible y multiempresa basado en Django – diseñado para construir plataformas empresariales de alto rendimiento, tanto en modo independiente como en la nube multisitio.

---

## 🌐 About Omnipyx Core

**Omnipyx Core** is the foundation of a powerful modular backend system written in Django. It enables the creation of:

- 🧩 Extensible modules via Python packages (e.g. `omnipyx-crm`, `omnipyx-inventory`)
- 🔁 Automatic loading and registration of installed modules
- 📊 Dynamic API documentation with Swagger / Redoc
- ☁️ Flexible SaaS architectures: self-hosted or multi-tenant cloud environments

It's the backbone of the upcoming **Zentryx** platform – a modern ERP-style cloud environment.

---

## 🚀 Features

- ✅ Modular architecture
- 📦 Installable modules via `pip install omnipyx-<module>`
- 🔧 Auto-discovery of Django apps and APIs
- 🧠 Swagger UI & Redoc auto-integrated
- 🏢 Multi-tenancy ready (`django-tenants` planned)
- 🌍 Multi-language and currency support (`parler`, `djmoney`)
- 🖌️ Admin UI enhancement with `django-admin-interface`

---

## 🧭 Roadmap Modular para Omnipyx SaaS
✅ 1. Fundamentos multitenant híbridos
  - Estructura modular Django + Poetry
  - Carga dinámica de apps con entry_points (omnipyx.modules)
  - Configurar multitenancy con múltiples bases de datos (una por sitio)
  - Manejo de tenant actual según dominio o cabecera HTTP (X-Tenant)

🔐 2. Sistema de licenciamiento
  - Validar licencias activas por instalación
  - Generación/registro de licencias (con firma y/o cifrado)
  - Comprobación automática al levantar instancia o ejecutar comando

⚙️ 3. Setup inicial dinámico
  - Si no hay sitios configurados, redirigir al wizard de instalación
  - Wizard de configuración de instancia: nombre del sistema, superusuario, conexión DB, dominio
  - Setup básico de licencia y validación

🏢 4. Soporte multiempresa dentro del sitio
  - Modelo Organization o Company relacionado por FK a cada recurso
  - Separación de datos por empresa dentro del tenant (via queryset managers)

🧩 5. Admin multisite (SuperAdmin)
  - Panel central de administración de sitios
  - Dashboard de estado por instancia (licencia, DB, uso)

📦 6. Distribución modular
  - Sistema de instalación estilo tienda de módulos (gratuitos/pagos)
  - Activación/desactivación desde panel web

---

## 📦 Requirements

- Python 3.11+
- Django >= 4.2
- PostgreSQL (recommended)

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/omnipyx-core.git
cd omnipyx-core
poetry install
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

Access the Swagger docs:
```
http://localhost:8000/api/docs/
```

---

## 📁 Project Structure

```bash
omnipyx/
├── omnipyx/             # Django project core
│   ├── modules/              # Dynamic module loader
│   ├── settings/             # Modular environment configs
├── requirements/             # Base, dev, and prod requirements
├── .env.example              # Default environment config
```

---

## 🔗 Useful Commands

```bash
# Apply migrations and collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# Generate OpenAPI schema manually (for drf-yasg)
python manage.py generateschema > schema.yaml
```

---

## 🛣️ Roadmap

- [x] Modular core setup
- [x] Swagger/Redoc API auto-generation
- [x] Module discovery
- [ ] Zentryx Panel (multi-site management)
- [ ] Multi-tenancy with `django-tenants`
- [ ] Dynamic provisioning API

---

## 📄 License

MIT © 2025 — Diego Asencio

---

## 🙌 Contributing

Want to help? Open an issue or submit a pull request! More coming soon in the [CONTRIBUTING.md](CONTRIBUTING.md).

---

Made with ❤️ for scalable systems.