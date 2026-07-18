# Startup Navigator

A production-ready, full-stack AI-powered web application that helps entrepreneurs navigate every stage of building a startup in India — from company registration to fundraising, legal compliance to AI tools.

---

## Live Demo

| Service | URL |
|---------|-----|
| Frontend | https://startup-navigator-rouge.vercel.app |
| Backend API | https://startup-navigator-api-vkbr.onrender.com |
| API Docs | https://startup-navigator-api-vkbr.onrender.com/docs |

---

## Seed Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@startupnav.com` | `StartupNav#2026Admin` |
| User | `user@startupnav.com` | `TestUser#2026` |

---

## Project Overview

Startup Navigator combines a curated knowledge base of 20+ expert-written articles with a RAG (Retrieval-Augmented Generation) pipeline powered by Google Gemini. Users can browse topics, ask questions in plain English, and get precise answers cited from the knowledge base.

### Key Features

- **10 topic categories**: Registration, Funding, Legal, Hiring, Branding, Marketing, Taxation, Fundraising, AI Tools, Growth
- **AI Search**: Chat-style interface backed by LangChain + ChromaDB + Gemini
- **User accounts**: JWT auth with httpOnly cookies, search history, dashboard
- **Admin panel**: Full CRUD on articles/resources, analytics, one-click AI reindex
- **Dark mode**: System-aware with manual toggle
- **Mobile-first**: Fully responsive at 375px, 768px, 1280px+

---

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for full Mermaid diagrams covering:
- System architecture (frontend ↔ backend ↔ DB ↔ vector store ↔ Gemini)
- RAG query flow step by step
- Article indexing flow
- Database schema (ERD)

### High-level summary

```
Browser → Next.js (Vercel)
            ↓ REST API (credentials: include, httpOnly cookies)
         FastAPI (Render)
            ↓ SQLAlchemy ORM
         PostgreSQL (Neon)
            ↓ RAG pipeline
         ChromaDB (local file) ← Gemini Embeddings (gemini-embedding-001)
            ↓ context
         Gemini Generation (gemini-2.0-flash) → Answer
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 14 (App Router) + TypeScript | Server components, file-based routing, Vercel-optimised |
| Styling | Tailwind CSS | Utility-first, dark mode via `class` strategy |
| Fonts | Space Grotesk (headings) + Inter (body) via `next/font` | No CDN latency, GDPR-safe |
| Backend | FastAPI (Python 3.11) | Async, typed, auto-generates OpenAPI docs |
| ORM | SQLAlchemy 2 + Alembic | Type-safe queries, schema migrations |
| Database | PostgreSQL (Neon free tier) | Relational, ACID, free hosted option |
| Auth | JWT (access 15min + refresh 7days) + bcrypt | Stateless, secure httpOnly cookies |
| Vector store | ChromaDB (local file) | Zero-config, persistent, runs on Render |
| RAG framework | LangChain | Clean abstraction over embedding + retrieval + generation |
| Embeddings | `gemini-embedding-001` (3072 dims) | Best quality available on free Gemini tier |
| Generation | `gemini-2.0-flash` | Fast, capable, generous free quota |
| AI SDK | `langchain-google-genai` | Official LangChain ↔ Gemini integration |
| Retry logic | `tenacity` | Handles Gemini transient rate limits |
| Toast notifications | `react-hot-toast` | Lightweight, accessible |
| Theme | `next-themes` | SSR-safe dark mode |

---

## AI Tools & Models Used

### Gemini Embedding — `gemini-embedding-001`
Used to convert article chunks and user queries into 3072-dimensional vectors stored in ChromaDB. Chosen because it's the highest-quality embedding model available on the Gemini free tier and returned 3072-dim embeddings confirmed working.

### Gemini Generation — `gemini-2.0-flash`
Used to synthesise answers from retrieved context chunks. The system prompt explicitly instructs the model to answer **only from provided context** and say so when it can't find an answer — preventing hallucination.

### RAG Approach
1. Articles are chunked (1000 chars, 150 overlap) at insert time and embedded into ChromaDB
2. At query time: embed query → retrieve top-5 chunks → de-duplicate by article → pass as context to Gemini
3. Every query, answer, and sources list is stored in `search_history` for dashboard/analytics

### System Prompt Strategy
```
Answer ONLY from the context provided. Be specific and cite relevant details.
If the answer is not in the context, say explicitly that you don't have enough information.
Do not use prior training knowledge about specific laws or regulations.
```
This grounds the model and makes answers trustworthy for a legal/regulatory domain.

---

## Local Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL database (Neon free tier recommended)
- Google AI Studio API key (aistudio.google.com)

### Backend

```cmd
cd backend
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt

copy .env.example .env
:: Edit .env — fill in DATABASE_URL, JWT_SECRET_KEY, GOOGLE_API_KEY

alembic revision --autogenerate -m "initial schema"
alembic upgrade head
python seed.py

uvicorn app.main:app --reload --port 8000
```

Verify: `http://localhost:8000/health` → `{"status":"ok"}`
API docs: `http://localhost:8000/docs`

### Frontend

```cmd
cd frontend
npm install
copy .env.example .env.local
:: .env.local already has NEXT_PUBLIC_API_URL=http://localhost:8000

npm run dev
```

Open: `http://localhost:3000`

### Run Tests

```cmd
cd backend
.venv\Scripts\activate.bat
pytest -v
```

Expected: **22 tests pass** (auth, CRUD, search — RAG calls mocked)

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string (Neon/Supabase) |
| `JWT_SECRET_KEY` | ✅ | Random 32-byte hex secret for JWT signing |
| `GOOGLE_API_KEY` | ✅ | Gemini API key from aistudio.google.com |
| `GEMINI_EMBEDDING_MODEL` | optional | Default: `models/gemini-embedding-001` |
| `GEMINI_GENERATION_MODEL` | optional | Default: `gemini-2.0-flash` |
| `FRONTEND_URL` | optional | Default: `http://localhost:3000` |
| `ENVIRONMENT` | optional | `development` or `production` |
| `CHROMA_PERSIST_DIR` | optional | Default: `./chroma_db` |
| `RAG_TOP_K` | optional | Number of chunks to retrieve. Default: `5` |

Generate JWT secret:
```cmd
python -c "import secrets; print(secrets.token_hex(32))"
```

### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ | URL of the FastAPI backend |

---

## Deployment

### Backend → Render (Free Tier)

1. Push your repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your GitHub repo, select the `backend` folder
4. Settings:
   - **Runtime**: Python 3
   - **Build command**: `pip install -r requirements.txt && alembic upgrade head && python seed.py`
   - **Start command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (all from `backend/.env`)
6. Deploy

> ⚠️ **ChromaDB on Render free tier**: Render's free tier has ephemeral disk — ChromaDB data is lost on every restart. After each deploy, call `POST /admin/reindex` (as admin) to rebuild the vector store from PostgreSQL.

### Frontend → Vercel (Free Tier)

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repo
3. Set **Root Directory** to `frontend`
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = your Render backend URL (e.g. `https://startup-navigator-api.onrender.com`)
5. Deploy

> Make sure to update `FRONTEND_URL` in your Render backend env vars to your Vercel URL so CORS works.

---

## Project Structure

```
startup-navigator/
├── frontend/                    # Next.js 14 App Router
│   ├── app/
│   │   ├── (main)/             # Public pages with Navbar + Footer
│   │   │   ├── page.tsx        # Home
│   │   │   ├── explore/        # Article browser + detail
│   │   │   ├── search/         # AI chat interface
│   │   │   ├── resources/      # External resources
│   │   │   ├── about/
│   │   │   └── contact/
│   │   ├── (auth)/             # Login + Signup (no nav)
│   │   ├── dashboard/          # User dashboard (protected)
│   │   └── admin/              # Admin panel (role-protected)
│   ├── components/
│   │   ├── providers/          # ThemeProvider, AuthProvider
│   │   ├── ui/                 # Badge, Skeleton
│   │   └── layout/             # Navbar, Footer
│   └── lib/                    # api.ts, types.ts, utils.ts
│
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── models/             # SQLAlchemy models (5 tables)
│   │   ├── schemas/            # Pydantic v2 schemas
│   │   ├── routers/            # 7 API routers
│   │   ├── services/           # auth_service, rag_service
│   │   ├── config.py           # pydantic-settings
│   │   ├── database.py         # SQLAlchemy engine + session
│   │   ├── dependencies.py     # get_current_user, require_admin
│   │   └── main.py             # FastAPI app + CORS
│   ├── alembic/                # DB migrations
│   ├── tests/                  # 22 pytest tests
│   ├── seed.py                 # Seeds DB + ChromaDB
│   └── requirements.txt
│
├── docs/
│   └── architecture.md         # Mermaid diagrams
└── README.md
```

---

## Known Limitations

| Limitation | Detail | Workaround |
|-----------|--------|------------|
| Gemini free tier quota | 15 RPM, ~1500 req/day for generation | Use paid API key or wait for daily reset |
| ChromaDB on Render free tier | Ephemeral disk resets on restart | Call `POST /admin/reindex` after each deploy |
| No email service | Contact form stores to DB only | Integrate SendGrid/Resend for production |
| JWT in httpOnly cookies | Requires `credentials: include` and matching CORS | Already configured; ensure `FRONTEND_URL` is set correctly on Render |
