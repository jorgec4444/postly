# Postly

**Publish faster. Manage better.**

Postly is an open-source social media management tool for community managers and agencies. Create AI-powered content, schedule posts, and manage multiple client accounts — all in one place.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-AGPL--3.0%20%2B%20Commons%20Clause-red.svg)](#license)

---

## ✨ Features

- 🤖 **AI Content Generation** — GPT-4o-mini rewrites your draft in 3 styles: professional, casual and viral
- 📸 **Image Generation** — capture your post as a shareable PNG directly in the browser (no server needed)
- 🎨 **8 visual themes** — light, dark, gradient, sunset, ocean, forest, fire, midnight
- 🔒 **Rate limiting** — daily limit per IP with in-memory fallback if Supabase is unavailable
- 🧪 **Tests included** — unit tests, integration tests and mocks for OpenAI/Supabase

### Coming soon
- 📅 **Post scheduling** — schedule content for a specific date, time or on a recurring basis
- 📱 **Instagram publishing** — publish photos, carousels and reels via the Meta Graph API
- 💼 **LinkedIn & Twitter/X** — multi-platform support
- 👥 **Multiple accounts** — manage several client profiles from a single dashboard
- 💳 **Stripe payments** — Free, Pro and Agency plans

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/tuusuario/postly.git
cd postly

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# 5. Start the backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 6. Serve the frontend (in a second terminal)
cd frontend && python -m http.server 3000
```

Open **http://localhost:3000** in your browser.

---

## 📁 Project structure

```
postly/
postly/
├── backend/
│   ├── app/
│     ├── __init__.py
│     ├── ai.py           # OpenAI calls
│     ├── config.py       # Environment variables and clients
│     ├── database.py     # Supabase client
│     ├── feedback.py     # Feedback persistence
│     ├── prompts.py      # AI improvement prompts
│     ├── rate_limiter.py # Daily IP rate limiting + analytics
│     └── schemas.py      # Pydantic models
|   ├── main.py           # FastAPI entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   └── main.js
├── tests/
│   ├── conftest.py
│   ├── test_ai.py
│   ├── test_config.py
│   ├── test_endpoints.py
│   ├── test_rate_limiter.py
│   └── test_schemas.py
├── pytest.ini
└── .env.example
```

---

## 💡 How it works

```
User writes a draft
        ↓
POST /improve  →  OpenAI generates 3 variations in parallel
        ↓
User picks their favourite
        ↓
html2canvas captures the styled card as PNG in the browser
        ↓
User downloads or shares the image
```

---

## 🛠️ Tech stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI + Pydantic v2 |
| AI | OpenAI GPT-4o-mini |
| Database | Supabase (PostgreSQL) |
| Image generation | html2canvas (browser-side) |
| Frontend | HTML + CSS + Vanilla JS |
| Tests | pytest + pytest-asyncio |
| Deploy | Railway (backend) · any static host (frontend) |

---

## ⚙️ Environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini          # optional, default: gpt-4o-mini

SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyJ...               # use the service_role key

MAX_FREE_GENERATIONS_PER_DAY=5    # optional, default: 5
ADMIN_API_KEY=change-me
```

> **Important**: always use the Supabase `service_role` key in the backend, never the `anon` key. Never commit your `.env` file to Git.

---

## 🗄️ Database setup (Supabase)

Run this SQL in your Supabase **SQL Editor**:

```sql
-- WARNING: This schema is for context only and is not meant to be run.
-- Table order and constraints may not be valid for execution.

CREATE TABLE public.clients (
  id bigint NOT NULL DEFAULT nextval('clients_id_seq'::regclass),
  user_id uuid NOT NULL,
  client_name text NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  brand_voice text NULL,
  CONSTRAINT clients_pkey PRIMARY KEY (id),
  CONSTRAINT clients_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);
CREATE TABLE public.feedback_logs (
  id bigint NOT NULL DEFAULT nextval('feedback_logs_id_seq'::regclass),
  ip text,
  feedback_text text,
  created_at timestamp with time zone DEFAULT now(),
  user_id uuid,
  CONSTRAINT feedback_logs_pkey PRIMARY KEY (id),
  CONSTRAINT feedback_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);
CREATE TABLE public.generations (
  id bigint NOT NULL DEFAULT nextval('generations_id_seq'::regclass),
  ip text,
  text_original text,
  text_improved text,
  style text,
  created_at timestamp with time zone DEFAULT now(),
  client_id bigint,
  CONSTRAINT generations_pkey PRIMARY KEY (id),
  CONSTRAINT generations_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id)
);
CREATE TABLE public.profiles (
  id bigint NOT NULL DEFAULT nextval('profiles_id_seq'::regclass),
  user_id uuid NOT NULL,
  current_plan USER-DEFINED NOT NULL DEFAULT 'free'::plan_type,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  CONSTRAINT profiles_pkey PRIMARY KEY (id),
  CONSTRAINT profiles_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);
CREATE TABLE public.rate_limits (
  id bigint NOT NULL DEFAULT nextval('rate_limits_id_seq'::regclass),
  ip text NOT NULL,
  date date NOT NULL,
  count integer NOT NULL DEFAULT 1,
  last_used_at timestamp with time zone,
  created_at timestamp with time zone DEFAULT now(),
  user_id uuid,
  CONSTRAINT rate_limits_pkey PRIMARY KEY (id),
  CONSTRAINT rate_limits_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id)
);
CREATE TABLE public.social_accounts (
  id bigint NOT NULL DEFAULT nextval('social_accounts_id_seq'::regclass),
  platform USER-DEFINED NOT NULL,
  username text NOT NULL,
  access_token text NOT NULL,
  token_expires_at timestamp with time zone NOT NULL,
  client_id bigint NOT NULL,
  status USER-DEFINED NOT NULL,
  account_id text NOT NULL,
  CONSTRAINT social_accounts_pkey PRIMARY KEY (id),
  CONSTRAINT social_accounts_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clients(id)
);
```
![Postly dabase schema](assets/supabase-schema.svg)

---

## 🧪 Tests

```bash
# Run all tests
pytest

# Verbose output
pytest --tb=short -v

# Single module
pytest tests/test_endpoints.py -v
```

Tests mock OpenAI and Supabase completely — no real credentials needed.

---

## 🌐 API endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET`  | `/` | API info |
| `GET`  | `/health` | Health check |
| `POST` | `/improve` | Improve a post (3 variations) |
| `GET`  | `/rate-limit/status` | Current rate limit status |
| `POST` | `/feedback` | Submit feedback |
| `GET`  | `/admin/stats?api_key=` | Usage statistics (protected) |

Interactive docs available at `http://localhost:8000/docs`.

---

## 🚢 Deploy

The backend runs in **Google Cloud Run** and the frontend as **Cloudflare Worker** with CI/CD via GitHub Actions.

---

### 🔧 Backend — Google Cloud Run

#### Pre-requisites
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install) installed and authenticated
- Docker installed
- GCP proyect created

#### Environment variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |

#### Steps for deploying
```bash
# 1. Authenticate in GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 2. Enable necessary services (only the first time)
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 3. Build and push the image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/YOUR_SERVICE_NAME

# 4. Deploy in Cloud Run
gcloud run deploy YOUR_SERVICE_NAME \
  --image gcr.io/YOUR_PROJECT_ID/YOUR_SERVICE_NAME \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_api_key_here
```

Once deployed, GCP will give you an URL like this one:
`https://YOUR_SERVICE_NAME-xxxxxxxxxx-XX.a.run.app`

Then, the deploy is done with **GitHub Actions** when pushing to `main` branch.
To do that, you will need to access gcloud, IAM tab and create a user that will have pormisions to deploy the backend from github to gcloud.
After creating it you will be able to generate a json as an access key for that user to do those actions. That json will be used for CI in github. 

#### Secrets in GitHub Actions

Ensure to have these secrets configured in **Settings → Secrets → Actions** of your repo:

| Secret | Description |
|---|---|
| `GCP_CREDENTIALS` | GCP json generated when creating an IAM user in gcloud |
| `OPENAI_API_KEY`  | Your OpenAI api key |


---

### 🌐 Frontend — Cloudflare Workers

#### Connect wit the backend

In main.js, update the backend URL provided by Cloud Run:
```javascript
const API_URL = "https://YOUR_SERVICE_NAME-xxxxxxxxxx-XX.a.run.app";
```

#### Deploy

The deploy is automatic via **GitHub Actions** when pushing to `main` branch.

to re-deploy manually:
```bash
# Install Wrangler before
npm install -g wrangler

# Manual deploy
wrangler deploy
```

---

### 🔁 Complete flow
```
GitHub push → Actions build → wrangler deploy → Cloudflare Worker
                                                        ↓
                                              calls Cloud Run (backend)
                                                        ↓
                                                  OpenAI API
```

---

## 🗺️ Roadmap

### ✅ Phase 1 — MVP
- [x] FastAPI backend + OpenAI
- [x] 3 improvement styles (professional, casual, viral)
- [x] 8 visual themes
- [x] Browser-side image generation with html2canvas
- [x] IP rate limiting with in-memory fallback
- [x] Unit and integration tests
- [x] Light / dark mode frontend
- [x] Auto-updating footer year
 
### 🚧 Phase 2 — Authentication & client management
- [ ] Google OAuth login (Supabase Auth)
- [ ] Client dashboard — manage all clients from one place
- [ ] Brand kit per client — tone of voice, custom prompt, examples
- [ ] Generation history per client
- [ ] Personal account settings
 
### 📝 Phase 3 — AI content features
- [ ] Platform-specific generation — Instagram, LinkedIn, TikTok each get tailored output
- [ ] Custom tones per client — brand voice used automatically in every generation
- [ ] Hashtag recommendations per post and platform
- [ ] Content repurposing — paste a long text, get posts for every platform
- [ ] Carousel generation — structured slide-by-slide content for Instagram
 
### 📋 Phase 4 — Social publishing
- [ ] Instagram publishing (Meta Graph API) — photos, carousels, reels
- [ ] LinkedIn publishing
- [ ] Twitter / X publishing
- [ ] Multiple social accounts per client
 
### 📅 Phase 5 — Scheduling & calendar
- [ ] Schedule posts for a specific date and time
- [ ] Recurring posts
- [ ] AI-powered content calendar — suggest a full week of content per client
 
### Based on competitor research

#### Must-have for agencies
- [ ] Cloud media library per client — store logos, images, videos and brand assets (bindings Cloudlfare R2)
- [ ] Approval workflow — review and approve content before it goes live
- [ ] Post preview — show exactly how the post will look on each platform
- [ ] Image auto-resize — automatically adapt images to each platform's specs
- [ ] Video validation — check video specs before publishing (length, size, format)

#### Nice to have
- [ ] Post templates — save frequently used formats per client or platform
- [ ] Bulk scheduling — upload and schedule multiple posts at once
- [ ] Canva integration — import designs directly from Canva
- [ ] Per-client analytics — impressions, clicks and performance per client

### 💳 Phase 6 — Monetisation
- [ ] Stripe integration
- [ ] Plans: Free (5/day, no account), Starter (€12/mo, 1 client), Pro (€29/mo, 5 clients), Agency (€79/mo, unlimited clients)
- [ ] Video support (Pro feature)
- [ ] Donations via Ko-fi or Buy Me a Coffee

---

## 🤝 Contributing

Contributions are welcome. Please:

1. Open an issue before starting a large change
2. Fork the repo and create a branch: `git checkout -b feature/my-feature`
3. Make sure tests pass: `pytest`
4. Open a Pull Request describing the change

> **License note**: by contributing you agree your code is distributed under the same terms as this project (AGPL-3.0 + Commons Clause). The project can be used freely for non-commercial purposes, but **cannot be used to offer a paid service** without explicit permission from the author.

---

## 📄 License

Copyright © 2026 Jorge Vinagre

Licensed under **GNU AGPLv3 with Commons Clause**.

| Can I...? | |
|-----------|---|
| View and study the code | ✅ |
| Modify and improve it | ✅ |
| Use it for personal projects | ✅ |
| Distribute modified versions | ✅ same license |
| Offer it as a paid SaaS | ❌ without permission |
| Sell or sublicense it | ❌ without permission |

For commercial licensing: [jorgecdev444@gmail.com](mailto:jorgecdev444@gmail.com)

Full license text in [`LICENSE`](./LICENSE).

---

## ⚠️ Legal notice

Postly uses the OpenAI API. Users must comply with [OpenAI's usage policies](https://openai.com/policies). The author is not responsible for content generated by users.

---

## 📞 Contact

- 📧 [jorgecdev444@gmail.com](mailto:jorgecdev444@gmail.com)
- 🐦 [@vinagre444](https://x.com/vinagre444)
- 💬 [Discord](https://discord.gg/fxJXWPF5)

---

**Built for the creator and agency community ❤️**
