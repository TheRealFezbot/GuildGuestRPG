# Forgeborn Chronicles

A browser-based RPG with turn-based combat, zone progression, character classes, gear, and a stamina-gated grind loop. Built as a portfolio project with a MUD-inspired combat log and a dark fantasy aesthetic.

---

## Features

- **4 Character Classes** — Warrior, Mage, Rogue, Ranger, each with unique passives
- **Turn-based Combat** — hit chance, crits, dodge, stamina costs, boss fights
- **Zone Progression** — 4 zones, unlock the next by defeating the boss
- **Items & Equipment** — class-specific gear across 6 slots, power level recalculation on equip
- **Shop System** — buy gear from unlocked zones with gold earned in combat
- **Inventory Management** — equip/unequip items, stat bonuses applied in real time
- **Auth System** — JWT + refresh tokens, email verification, password reset
- **Stamina System** — regenerates over time (Redis-cached), limits grinding

## Planned
- PvP arena (async combat, Elo ratings)
- Guild system
- Leaderboards
- Potion system
- Item drops from monsters

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS v4 |
| Backend | FastAPI (Python) |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Cache | Redis (stamina, leaderboard caching) |
| Auth | JWT (access + refresh tokens) |
| Email | Resend |
| Dev | Docker Compose |

---

## Local Setup

### Prerequisites
- Docker + Docker Compose
- Node.js 18+

### 1. Clone and configure environment

```bash
git clone https://github.com/therealfezbot/GuildGuestRPG.git
cd GuildGuestRPG
cp .env.example .env
```

Fill in `.env` with your values (DB credentials, JWT secret, Resend API key, etc.).

### 2. Start the backend

```bash
docker compose up -d
```

### 3. Run migrations and seed data

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seed.run_seeds
```

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`, backend at `http://localhost:8000`.

API docs available at `http://localhost:8000/docs`.

---

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── core/          # Config, security, enums, game logic
│   │   ├── crud/          # DB query functions
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # FastAPI route handlers
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── seed/          # Seed data scripts
│   │   └── services/      # Combat engine, email
│   └── alembic/           # Database migrations
├── frontend/
│   └── src/
│       ├── api/           # Axios API functions
│       ├── components/    # Shared UI components
│       ├── context/       # Auth context
│       ├── pages/         # Route pages
│       └── types/         # TypeScript interfaces
└── docker-compose.yml
```
