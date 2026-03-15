# 🎨 TweetCraft AI

> Convierte tus borradores en tweets que la gente lee — con IA que mejora tu contenido y genera imágenes listas para compartir.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-AGPL--3.0%20%2B%20Commons%20Clause-red.svg)](#-licencia)

---

## ✨ Características

- 🤖 **IA Inteligente** — GPT-4o-mini genera 3 variaciones por tweet (profesional, casual, viral)
- ⚡ **Rápido** — variaciones en 2-3 segundos con llamadas en paralelo
- 🎨 **8 temas visuales** — claro, oscuro, gradiente, sunset, ocean, forest, fire, midnight
- 📸 **Imágenes HD** — screenshots reales con Playwright (Linux) o Pillow (Windows dev)
- 🔒 **Rate limiting** — límite diario por IP con fallback en memoria si Supabase no está disponible
- 🧪 **Tests incluidos** — unitarios, integración y mocks de OpenAI/Supabase

---

## 🚀 Quick Start

```bash
# 1. Clonar el repositorio
git clone https://github.com/tuusuario/tweetcraft-ai.git
cd tweetcraft-ai

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Instalar Playwright (Linux/Mac — en Windows se usa Pillow automáticamente)
playwright install chromium

# 5. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# 6. Arrancar el backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 7. Servir el frontend (en otra terminal)
cd frontend && python -m http.server 3000
```

Abre **http://localhost:3000** en el navegador.

---

## 📁 Estructura del proyecto

```
tweetcraft-ai/
├── app/
│   ├── __init__.py
│   ├── ai.py           # Llamadas a OpenAI
│   ├── config.py       # Variables de entorno y clientes
│   ├── database.py     # Cliente Supabase
│   ├── feedback.py     # Persistencia de feedback
│   ├── prompts.py      # Prompts de mejora de tweets
│   ├── rate_limiter.py # Límite diario por IP + analytics
│   ├── render.py       # Generación HTML + screenshot
│   └── schemas.py      # Modelos Pydantic
├── frontend/
│   ├── index.html
│   └── main.js
├── tests/
│   ├── conftest.py
│   ├── test_ai.py
│   ├── test_config.py
│   ├── test_endpoints.py
│   ├── test_rate_limiter.py
│   ├── test_render.py
│   └── test_schemas.py
├── main.py             # Entry point FastAPI
├── requirements.txt
├── pytest.ini
└── .env.example
```

---

## 💡 Cómo funciona

```
Usuario escribe tweet
        ↓
POST /improve  →  OpenAI genera 3 variaciones en paralelo
        ↓
Usuario selecciona su favorita
        ↓
POST /generate-image  →  Playwright renderiza HTML y captura PNG
        ↓
Usuario descarga / comparte la imagen
```

---

## 🛠️ Stack

| Capa | Tecnología |
|------|-----------|
| Backend | FastAPI + Pydantic v2 |
| IA | OpenAI GPT-4o-mini |
| Base de datos | Supabase (PostgreSQL) |
| Imágenes | Playwright (prod) · Pillow (dev Windows) |
| Frontend | HTML + CSS + Vanilla JS |
| Tests | pytest + pytest-asyncio |
| Deploy | Railway (backend) · cualquier static host (frontend) |

---

## ⚙️ Variables de entorno

Copia `.env.example` a `.env` y rellena:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini          # opcional, default: gpt-4o-mini

SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyJ...               # usa la service_role key

MAX_FREE_GENERATIONS_PER_DAY=5    # opcional, default: 5
ADMIN_API_KEY=cambia-esto
```

> **Importante**: usa siempre la `service_role` key de Supabase en el backend, nunca la `anon` key. Nunca subas el `.env` a GitHub.

---

## 🗄️ Base de datos (Supabase)

Ejecuta este SQL en el **SQL Editor** de tu proyecto Supabase:

```sql
create table rate_limits (
  id           bigserial primary key,
  ip           text not null,
  date         date not null,
  count        int  not null default 1,
  last_used_at timestamptz,
  created_at   timestamptz default now(),
  unique(ip, date)
);

create table generations (
  id             bigserial primary key,
  ip             text,
  tweet_original text,
  tweet_improved text,
  style          text,
  created_at     timestamptz default now()
);

create table feedback_logs (
  id            bigserial primary key,
  ip            text,
  feedback_text text,
  created_at    timestamptz default now()
);
```

---

## 🧪 Tests

```bash
# Todos los tests
pytest

# Verbose con detalle de fallos
pytest --tb=short -v

# Un módulo concreto
pytest tests/test_endpoints.py -v
```

Los tests mockean completamente OpenAI y Supabase — no necesitas credenciales reales para ejecutarlos.

---

## 🌐 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET`  | `/` | Info de la API |
| `GET`  | `/health` | Health check |
| `POST` | `/improve` | Mejora un tweet (3 variaciones) |
| `POST` | `/generate-image` | Genera PNG del tweet |
| `GET`  | `/rate-limit/status` | Estado del límite del usuario |
| `POST` | `/feedback` | Enviar feedback |
| `GET`  | `/admin/stats?api_key=` | Estadísticas (protegido) |

Documentación interactiva disponible en `http://localhost:8000/docs`.

---

## 🚢 Deploy en Railway

1. Sube el proyecto a GitHub
2. Conecta el repo en [railway.app](https://railway.app)
3. Añade las variables de entorno del `.env.example` en el panel de Railway
4. Comando de inicio: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Build command: `pip install -r requirements.txt && playwright install chromium --with-deps`
6. Actualiza `API_URL` en `frontend/main.js` con la URL que Railway te asigne

---

## 🗺️ Roadmap

### ✅ Fase 1 — MVP
- [x] Backend FastAPI + OpenAI
- [x] 3 estilos de mejora (profesional, casual, viral)
- [x] 8 temas visuales
- [x] Generación de imágenes con Playwright
- [x] Rate limiting por IP con fallback en memoria
- [x] Tests unitarios e integración
- [x] Frontend con modo claro/oscuro

### 🚧 Fase 2 — Autenticación
- [ ] Sistema de usuarios (Supabase Auth)
- [ ] Dashboard personal
- [ ] Historial de tweets generados

### 📋 Fase 3 — Monetización
- [ ] Integración Stripe
- [ ] Planes: Free (5/día), Pro (ilimitado, €12/mes), Teams (€39/mes)
- [ ] Webhooks para suscripciones

### 🎨 Fase 4 — Features avanzadas
- [ ] Optimización por plataforma (LinkedIn, Instagram, Threads)
- [ ] Personalización de imágenes (logo propio, colores, fuentes)
- [ ] Análisis de engagement estimado por variación
- [ ] Soporte para threads largos
- [ ] Exportación a múltiples formatos
- [ ] Soporte multilingüe (en, fr, pt)
- [ ] Publicación directa vía Twitter/X API

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Abre un issue antes de empezar un cambio grande
2. Haz fork del repositorio y crea una rama: `git checkout -b feature/mi-feature`
3. Asegúrate de que los tests pasan: `pytest`
4. Abre un Pull Request describiendo el cambio

> **Nota de licencia**: al contribuir aceptas que tu código se distribuye bajo los mismos términos que este proyecto (AGPL-3.0 + Commons Clause). El proyecto puede usarse libremente de forma no comercial, pero **no puede usarse para ofrecer un servicio de pago** sin permiso explícito del autor.

---

## 📄 Licencia

Copyright © 2025 Jorge Vinagre

Este proyecto está licenciado bajo **GNU AGPLv3 con Commons Clause**.

| ¿Puedo...? | |
|---|---|
| Ver y estudiar el código | ✅ |
| Modificarlo y mejorarlo | ✅ |
| Usarlo para proyectos personales | ✅ |
| Distribuir versiones modificadas | ✅ con la misma licencia |
| Ofrecerlo como servicio SaaS de pago | ❌ sin permiso |
| Venderlo o sublicenciarlo | ❌ sin permiso |

Para licencias comerciales: [jorgecdev444@gmail.com](mailto:jorgecdev444@gmail.com)

El texto completo está en el archivo [`LICENSE`](./LICENSE).

---

## ⚠️ Aviso legal

TweetCraft AI utiliza la API de OpenAI. Los usuarios deben cumplir con los [términos de uso de OpenAI](https://openai.com/policies). El autor no se responsabiliza por el contenido generado por los usuarios.

---

## 📞 Contacto

- 📧 [jorgecdev444@gmail.com](mailto:jorgecdev444@gmail.com)
- 🐦 [@vinagre444](https://x.com/vinagre444)
- 💬 [Discord](https://discord.gg/TtEeWScb)

---

**Hecho con ❤️ para la comunidad de creators**
