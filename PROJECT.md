# Guild Quest RPG - Project Specification

A text-based multiplayer RPG with monsters, gear, guilds, PvP, and leaderboards.
Modern web UI with a MUD-inspired combat log. Portfolio-quality MVP targeting 40-60 hours.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React + TypeScript + Vite |
| Styling | Tailwind CSS (custom gold/brown/bordeaux palette) |
| Backend | FastAPI (Python) |
| Database | PostgreSQL |
| Cache/Timers | Redis (stamina recharge, leaderboard caching) |
| Real-time | WebSockets (FastAPI) — future guild chat |
| Auth | JWT tokens |
| Email | Resend or SendGrid (verification, password reset, admin blasts) |
| Dev Environment | Docker-compose (FastAPI + PostgreSQL + Redis) |
| Production | AWS ECS (Fargate) + RDS, or Fly.io/Railway as cheaper alternative |

---

## Project File Layout

```
guild-quest-rpg/
├── docker-compose.yml                  # FastAPI + PostgreSQL + Redis services
├── .env                                # Environment variables (DB URL, Redis, JWT secret, email API key)
├── .env.example                        # Template for env vars (committed to git)
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile                      # Python container for FastAPI
│   ├── requirements.txt                # Python dependencies
│   ├── alembic.ini                     # Alembic config (points to migrations/)
│   │
│   ├── alembic/
│   │   ├── env.py                      # Alembic environment setup
│   │   └── versions/                   # Auto-generated migration files
│   │       ├── 001_create_users.py
│   │       ├── 002_create_characters.py
│   │       ├── 003_create_zones_and_monsters.py
│   │       ├── 004_create_combat_logs.py
│   │       ├── 005_create_items_and_inventory.py
│   │       ├── 006_create_potions.py
│   │       ├── 007_create_shop_listings.py
│   │       ├── 008_create_pvp_tables.py
│   │       └── ...
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI app creation, CORS, router includes, startup events
│   │   ├── config.py                   # Settings from env vars (pydantic BaseSettings)
│   │   │
│   │   ├── core/                       # Shared utilities and infrastructure
│   │   │   ├── __init__.py
│   │   │   ├── database.py             # SQLAlchemy engine, session factory, Base model
│   │   │   ├── redis.py               # Redis connection and helpers
│   │   │   ├── security.py            # JWT creation/verification, password hashing (bcrypt)
│   │   │   ├── email.py               # Email service (Resend/SendGrid) — send verification, reset, blast
│   │   │   ├── deps.py                # Dependency injection: get_db, get_current_user, get_admin_user
│   │   │   └── exceptions.py          # Custom HTTP exceptions (NotFound, Forbidden, InsufficientGold, etc.)
│   │   │
│   │   ├── models/                     # SQLAlchemy ORM models (database tables)
│   │   │   ├── __init__.py             # Re-export all models for Alembic auto-detection
│   │   │   ├── user.py                # User model (email, password_hash, is_verified, is_admin, is_banned)
│   │   │   ├── character.py           # Character model (name, class, stats, stamina, pvp_tokens)
│   │   │   ├── zone.py               # Zone model (name, description, order)
│   │   │   ├── monster.py            # Monster model (base stats, zone FK, order_in_zone, is_zone_boss)
│   │   │   ├── monster_level.py      # MonsterLevel model (level 1-5 multipliers)
│   │   │   ├── monster_progress.py   # MonsterProgress model (character's progress per monster)
│   │   │   ├── zone_progress.py      # ZoneProgress model (character's zone unlock state)
│   │   │   ├── item.py               # Item model (name, type, rarity, stat bonuses, price)
│   │   │   ├── inventory.py          # Inventory model (character FK, item FK, is_equipped)
│   │   │   ├── potion.py             # Potion model (name, type, effect_value, price)
│   │   │   ├── potion_inventory.py   # PotionInventory model (character FK, potion FK, quantity)
│   │   │   ├── combat_log.py         # CombatLog model (fight results, combat_text JSON, rewards)
│   │   │   ├── shop_listing.py       # ShopListing model (zone FK, item/potion FK, stock)
│   │   │   ├── pvp_match.py          # PvPMatch model (challenger, defender, result, rating_change)
│   │   │   └── pvp_ranking.py        # PvPRanking model (character FK, rating, wins, losses)
│   │   │
│   │   ├── schemas/                    # Pydantic schemas (request/response validation)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # RegisterRequest, LoginRequest, TokenResponse, PasswordResetRequest
│   │   │   ├── character.py          # CharacterCreate, CharacterResponse, CharacterPublic
│   │   │   ├── zone.py               # ZoneResponse, ZoneWithProgress
│   │   │   ├── monster.py            # MonsterResponse, MonsterWithProgress
│   │   │   ├── combat.py             # FightRequest, CombatLogResponse, CombatLogDetail
│   │   │   ├── item.py               # ItemResponse
│   │   │   ├── inventory.py          # InventoryResponse, EquipRequest
│   │   │   ├── potion.py             # PotionResponse, PotionInventoryResponse
│   │   │   ├── shop.py               # ShopListingResponse, BuyRequest
│   │   │   ├── pvp.py                # PvPOpponentResponse, PvPMatchResponse, PvPRankingResponse
│   │   │   ├── leaderboard.py        # LeaderboardEntry, LeaderboardResponse
│   │   │   └── admin.py              # UserListResponse, BanRequest, EmailBlastRequest, StatsResponse
│   │   │
│   │   ├── routers/                    # API route handlers (thin layer — delegates to services)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py               # /auth/* endpoints (register, login, refresh, verify, reset)
│   │   │   ├── characters.py         # /characters/* endpoints (create, get me, get by id)
│   │   │   ├── zones.py              # /zones/* endpoints (list zones, list monsters in zone)
│   │   │   ├── combat.py             # /combat/* endpoints (fight, logs)
│   │   │   ├── inventory.py          # /inventory/* endpoints (list, equip, unequip, discard)
│   │   │   ├── shop.py               # /shop/* endpoints (list, buy, sell)
│   │   │   ├── pvp.py                # /pvp/* endpoints (opponents, challenge, history, rankings)
│   │   │   ├── leaderboards.py       # /leaderboards/* endpoints (power, level, pvp)
│   │   │   └── admin.py              # /admin/* endpoints (users, ban, email, stats)
│   │   │
│   │   ├── services/                   # Business logic (called by routers)
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # Register, login, token refresh, email verification, password reset
│   │   │   ├── character_service.py  # Create character, get stats, calculate power level
│   │   │   ├── stamina_service.py    # Calculate current stamina, deduct stamina, check recharge
│   │   │   ├── zone_service.py       # Get zones/monsters with progress, check unlocks
│   │   │   ├── combat_service.py     # Turn-by-turn combat engine, damage/hit/crit/dodge calcs
│   │   │   ├── reward_service.py     # XP, gold, item drop rolls, level-up logic, class bonuses
│   │   │   ├── inventory_service.py  # Equip/unequip, discard, enforce slot rules, power recalc
│   │   │   ├── potion_service.py     # Carry limits, combat integration, deduction after fight
│   │   │   ├── shop_service.py       # Buy/sell validation, gold transactions
│   │   │   ├── pvp_service.py        # Matchmaking, async combat, ELO rating, token management
│   │   │   ├── leaderboard_service.py # Query + cache leaderboards in Redis, own-rank lookup
│   │   │   └── admin_service.py      # User search, ban/unban, email blast, game stats queries
│   │   │
│   │   └── seed/                       # Seed data scripts
│   │       ├── __init__.py
│   │       ├── run_seeds.py           # Master seed runner (calls all seed scripts in order)
│   │       ├── seed_zones.py          # Insert 4 zones
│   │       ├── seed_monsters.py       # Insert 16 monsters with base stats
│   │       ├── seed_monster_levels.py # Insert level 1-5 multipliers
│   │       ├── seed_items.py          # Insert items for all zones
│   │       ├── seed_potions.py        # Insert health potions (S/M/L) + attack potion
│   │       └── seed_shop.py           # Insert shop listings per zone
│   │
│   └── tests/                          # Backend tests
│       ├── conftest.py                # Test DB setup, fixtures (test client, test user, test character)
│       ├── test_auth.py               # Auth endpoint tests (register, login, verify, reset)
│       ├── test_characters.py         # Character creation and retrieval tests
│       ├── test_combat.py             # Combat engine tests (damage calc, crit, dodge, potions)
│       ├── test_progression.py        # Zone/monster unlock logic tests
│       ├── test_inventory.py          # Equip, unequip, discard, slot enforcement tests
│       ├── test_shop.py               # Buy, sell, gold validation tests
│       ├── test_pvp.py                # Matchmaking, rating, token tests
│       └── test_leaderboards.py       # Leaderboard query and caching tests
│
└── frontend/
    ├── Dockerfile                      # Node container for React dev server
    ├── package.json
    ├── tsconfig.json
    ├── vite.config.ts                  # Vite config (proxy API to backend in dev)
    ├── tailwind.config.ts              # Tailwind config with custom color palette
    ├── postcss.config.js
    ├── index.html                      # Vite entry point
    │
    ├── public/
    │   └── favicon.ico
    │
    └── src/
        ├── main.tsx                    # React entry point, mount App
        ├── App.tsx                     # Router setup, auth provider, layout wrapper
        ├── index.css                   # Tailwind @import directives, global styles
        │
        ├── api/                        # API client layer
        │   ├── client.ts              # Axios/fetch instance with base URL, JWT interceptor, auto-refresh
        │   ├── auth.ts                # register(), login(), refreshToken(), verifyEmail(), resetPassword()
        │   ├── characters.ts          # createCharacter(), getMyCharacter(), getCharacter()
        │   ├── zones.ts              # getZones(), getZoneMonsters()
        │   ├── combat.ts             # fight(), getCombatLogs(), getCombatLog()
        │   ├── inventory.ts          # getInventory(), equipItem(), unequipItem(), discardItem()
        │   ├── shop.ts               # getShop(), buyItem(), sellItem()
        │   ├── pvp.ts                # getOpponents(), challenge(), getPvPHistory()
        │   ├── leaderboards.ts       # getPowerLeaderboard(), getLevelLeaderboard(), getPvPLeaderboard()
        │   └── admin.ts              # getUsers(), banUser(), sendEmailBlast(), getStats()
        │
        ├── hooks/                      # Custom React hooks
        │   ├── useAuth.ts             # Access auth context (user, login, logout, isAuthenticated)
        │   ├── useCharacter.ts        # Fetch and cache character data, refetch on changes
        │   ├── useStamina.ts          # Real-time stamina countdown (calculate from stamina_updated_at)
        │   ├── usePvPTokens.ts        # PvP token state with daily reset logic
        │   └── usePolling.ts          # Generic polling hook for leaderboard/stamina refresh
        │
        ├── context/                    # React context providers
        │   └── AuthContext.tsx         # Auth state (user, tokens), login/logout, token refresh, persist to localStorage
        │
        ├── types/                      # TypeScript type definitions
        │   ├── auth.ts                # User, LoginRequest, RegisterRequest, TokenResponse
        │   ├── character.ts           # Character, CharacterClass, CreateCharacterRequest
        │   ├── zone.ts               # Zone, ZoneWithProgress
        │   ├── monster.ts            # Monster, MonsterWithProgress, MonsterLevel
        │   ├── combat.ts             # FightRequest, CombatLog, CombatLogEntry
        │   ├── item.ts               # Item, Rarity, ItemType
        │   ├── inventory.ts          # InventoryItem
        │   ├── potion.ts             # Potion, PotionInventory
        │   ├── shop.ts               # ShopListing
        │   ├── pvp.ts                # PvPOpponent, PvPMatch, PvPRanking
        │   ├── leaderboard.ts        # LeaderboardEntry
        │   └── admin.ts              # AdminUser, GameStats, EmailBlast
        │
        ├── components/                 # Reusable UI components
        │   ├── layout/
        │   │   ├── GameLayout.tsx     # Main game shell: sidebar nav + content area + stamina bar
        │   │   ├── AdminLayout.tsx    # Admin shell: sidebar nav + content area
        │   │   ├── Sidebar.tsx        # Navigation sidebar (zones, inventory, shop, pvp, leaderboards)
        │   │   └── Header.tsx         # Top bar with character name, gold, stamina
        │   │
        │   ├── common/
        │   │   ├── ProtectedRoute.tsx # Redirect to /login if not authenticated
        │   │   ├── AdminRoute.tsx     # Redirect if not admin
        │   │   ├── LoadingSpinner.tsx # Loading indicator
        │   │   ├── ErrorToast.tsx     # Toast notification for errors
        │   │   ├── ConfirmDialog.tsx  # "Are you sure?" modal
        │   │   ├── EmptyState.tsx     # Placeholder for empty lists
        │   │   └── ProgressBar.tsx    # XP bar, stamina bar, HP bar
        │   │
        │   ├── character/
        │   │   ├── ClassSelector.tsx  # Class picker cards with stats preview (character creation)
        │   │   ├── StatBlock.tsx      # Character stats display (HP, ATK, DEF, level, power)
        │   │   └── EquippedGear.tsx   # Shows 3 equipped item slots with item details
        │   │
        │   ├── combat/
        │   │   ├── CombatLog.tsx      # Scrolling turn-by-turn text log with styled events
        │   │   ├── FightSetup.tsx     # Pre-fight: select monster level, toggle potions, confirm
        │   │   ├── CombatResult.tsx   # Victory/defeat banner + reward summary
        │   │   └── CombatHistoryItem.tsx # Single row in combat history list
        │   │
        │   ├── zone/
        │   │   ├── ZoneCard.tsx       # Zone card with name, lock state, progress bar
        │   │   └── MonsterCard.tsx    # Monster card with levels, progress, fight button
        │   │
        │   ├── inventory/
        │   │   ├── InventoryGrid.tsx  # Grid of item cards with rarity colors
        │   │   ├── ItemCard.tsx       # Single item: name, stats, rarity border, equip/sell buttons
        │   │   ├── ItemTooltip.tsx    # Hover tooltip: stat comparison vs equipped item
        │   │   └── PotionList.tsx     # Potion inventory with quantities
        │   │
        │   ├── shop/
        │   │   ├── ShopGrid.tsx       # Grid of shop items with buy buttons
        │   │   ├── ShopItem.tsx       # Single shop item: name, stats, price, buy button
        │   │   └── ZoneSelector.tsx   # Dropdown/tabs to switch between zone shops
        │   │
        │   ├── pvp/
        │   │   ├── OpponentCard.tsx   # PvP opponent: name, class, power indicator, challenge button
        │   │   ├── PvPResult.tsx      # PvP fight result with rating change
        │   │   └── PvPHistoryItem.tsx # Single row in PvP match history
        │   │
        │   ├── leaderboard/
        │   │   ├── LeaderboardTable.tsx # Ranked table with highlight for current player
        │   │   └── LeaderboardTabs.tsx  # Tab switcher (Power / Level / PvP)
        │   │
        │   └── admin/
        │       ├── UserTable.tsx      # Searchable user list with ban/unban actions
        │       ├── UserDetail.tsx     # Full user detail panel (stats, history, actions)
        │       ├── StatCards.tsx      # Dashboard stat cards (total users, active, fights, etc.)
        │       └── EmailBlastForm.tsx # Form: recipient filter, subject, body, preview, send
        │
        └── pages/                      # Page-level components (one per route)
            ├── LandingPage.tsx        # /                — game intro, register CTA
            ├── LoginPage.tsx          # /login           — login form
            ├── RegisterPage.tsx       # /register        — registration form
            ├── VerifyEmailPage.tsx    # /verify-email    — email verification handler
            ├── ForgotPasswordPage.tsx # /forgot-password — request reset email
            ├── ResetPasswordPage.tsx  # /reset-password  — reset password form
            │
            ├── game/
            │   ├── DashboardPage.tsx      # /game              — character summary, stamina, quick actions
            │   ├── CharacterPage.tsx      # /game/character     — full stats, equipment, power level
            │   ├── ZonesPage.tsx          # /game/zones         — zone map, progression overview
            │   ├── ZoneDetailPage.tsx     # /game/zones/:id     — monster list, fight selection
            │   ├── CombatResultPage.tsx   # /game/combat/:logId — combat log view
            │   ├── InventoryPage.tsx      # /game/inventory     — items + potions management
            │   ├── ShopPage.tsx           # /game/shop          — buy/sell items and potions
            │   ├── PvPPage.tsx            # /game/pvp           — arena, matchmaking, history
            │   └── LeaderboardsPage.tsx   # /game/leaderboards  — rankings tabs
            │
            └── admin/
                ├── AdminDashboardPage.tsx  # /admin          — stat cards, charts
                ├── AdminUsersPage.tsx      # /admin/users     — user management table
                └── AdminEmailPage.tsx      # /admin/email     — email broadcast tool
```

---

## Core Game Loop

```
Create Character → Pick Class → Enter Zone 1
        ↓
Fight Monsters → Earn Gold / XP / Item Drops → Level Up → Buy Gear
        ↓
Climb Power Level → Unlock New Monsters → Unlock New Zones
        ↓
Compete on Leaderboard → Challenge Players in PvP Arena
```

---

## Classes

Four classes, each with a distinct path to building power:

| Class | HP | ATK | DEF | Identity | Passive Bonus |
|-------|-----|-----|-----|----------|---------------|
| **Warrior** | 120 | 10 | 8 | Tank / Steady | +2 DEF per level (instead of +1). Higher base survivability. |
| **Mage** | 80 | 15 | 4 | Burst / Gold | +15% bonus gold from monster kills. High risk, high reward farming. |
| **Rogue** | 100 | 12 | 5 | Luck / Drops | +10% item drop chance. Higher crit chance (15% base vs 10%). |
| **Ranger** | 100 | 11 | 6 | Efficiency / XP | +15% bonus XP from kills. Reaches higher levels faster. |

### Stat Growth Per Level

| Stat | Warrior | Mage | Rogue | Ranger |
|------|---------|------|-------|--------|
| Max HP | +12 | +6 | +8 | +10 |
| Attack | +2 | +3 | +2 | +2 |
| Defense | +2 | +1 | +1 | +1 |

### XP & Leveling

```python
xp_to_next_level = level * 100  # Level 1→2 = 100xp, 2→3 = 200xp, etc.
```

> **TODO — Balancing**: XP rewards from monsters and the leveling curve need a dedicated balancing pass. The goal is that players progress through each zone over ~2-3 days of active play (using full stamina 2x/day). Monster XP values in seed data are placeholder estimates — test and adjust once the combat loop is playable.

---

## Combat System

### Overview
- **Auto-resolve**: combat plays out turn-by-turn on the backend, no player input during fight
- **Output**: detailed text log returned to the frontend (MUD-style)
- **Stamina cost**: 5 per normal fight, 10 per boss fight

### Combat Flow

```
1. Player selects monster + level
2. (Optional) Player uses attack potion pre-fight
3. Backend simulates turn-by-turn combat:
   a. Determine turn order (could be speed-based or alternating)
   b. Each turn: calculate hit/miss, damage, crit chance
   c. Auto-use health potions if HP < 30% (up to 3 per fight)
   d. Continue until one side reaches 0 HP or player flees
4. Return detailed combat log + rewards to frontend
5. HP resets after every fight
```

### Damage Formula

```python
base_damage = attacker.attack - (defender.defense / 2)
base_damage = max(1, base_damage)  # minimum 1 damage

# Variance: ±20% randomness
damage = base_damage * random.uniform(0.8, 1.2)
damage = round(damage)
```

### Hit & Crit System

```python
# Hit chance: based on level difference
hit_chance = 0.85 + (attacker.level - defender.level) * 0.03
hit_chance = clamp(hit_chance, 0.50, 0.95)

# Crit chance: flat base, Rogues get bonus
crit_chance = 0.10  # 10% base, Rogue = 15%
crit_multiplier = 1.5

# Dodge chance
dodge_chance = 0.05 + (defender.defense / 200)
dodge_chance = clamp(dodge_chance, 0.05, 0.20)
```

### Win Chance (PvE Approximation)

Players with a higher power level than the monster's effective power have a strong advantage, but crits and dodges can swing outcomes. Fighting monsters well above your power level is risky but possible.

### Example Combat Log Output

```
⚔️ Battle: Warrior Theron vs Goblin (Stage 3)

Turn 1: You strike Goblin for 14 damage. (Goblin HP: 46/60)
Turn 2: Goblin hits you for 7 damage. (Your HP: 113/120)
Turn 3: You strike Goblin for 11 damage. (Goblin HP: 35/60)
Turn 4: Goblin misses!
Turn 5: Critical hit! You deal 21 damage to Goblin. (Goblin HP: 14/60)
Turn 6: Goblin hits you for 8 damage. (Your HP: 105/120)
Turn 7: You strike Goblin for 13 damage. Goblin defeated!

🏆 Victory!
  +30 XP (Ranger bonus: +4 XP)
  +22 Gold
  🎁 Item Drop: Iron Dagger (uncommon)
```

---

## Zone & Monster Progression

### Structure

- **4 Zones** in MVP, each with **4 Monsters**
- Each monster has **5 Levels** (stages of increasing difficulty)
- **16 unique monsters**, **80 monster variants** total

### Unlocking Rules

- **Next monster**: beat Level 3 of current monster to unlock the next monster in the zone
- **Next zone**: beat Level 5 of the final monster in the current zone
- **Boss fights**: Level 5 of the final monster in each zone is a "boss" (costs 10 stamina)

### Zone Layout

```
Zone 1: Whispering Forest (levels ~1-5)
├── Slime         → Levels 1-5
├── Goblin        → Levels 1-5  (unlocked after Slime lvl 3)
├── Wolf          → Levels 1-5  (unlocked after Goblin lvl 3)
└── Treant        → Levels 1-5  (unlocked after Wolf lvl 3)
    └── Treant lvl 5 = Zone Boss → unlocks Zone 2

Zone 2: Darkstone Caves (levels ~5-10)
├── Bat           → Levels 1-5
├── Spider        → Levels 1-5
├── Orc           → Levels 1-5
└── Cave Troll    → Levels 1-5
    └── Cave Troll lvl 5 = Zone Boss → unlocks Zone 3

Zone 3: Shattered Ruins (levels ~10-16)
├── Skeleton      → Levels 1-5
├── Wraith        → Levels 1-5
├── Golem         → Levels 1-5
└── Lich          → Levels 1-5
    └── Lich lvl 5 = Zone Boss → unlocks Zone 4

Zone 4: Ember Volcano (levels ~16-22)
├── Fire Imp      → Levels 1-5
├── Lava Serpent  → Levels 1-5
├── Infernal Orc  → Levels 1-5
└── Elder Dragon  → Levels 1-5
    └── Elder Dragon lvl 5 = Final Boss
```

### Monster Scaling Per Level

Each monster level multiplies base stats:

| Monster Level | HP | ATK | DEF | XP Reward | Gold Range |
|---------------|-----|-----|-----|-----------|------------|
| 1 | 1.0x | 1.0x | 1.0x | 1.0x | 1.0x |
| 2 | 1.3x | 1.2x | 1.2x | 1.4x | 1.3x |
| 3 | 1.6x | 1.4x | 1.4x | 1.8x | 1.6x |
| 4 | 2.0x | 1.7x | 1.7x | 2.3x | 2.0x |
| 5 | 2.5x | 2.0x | 2.0x | 3.0x | 2.5x |

---

## Stamina System

| Setting | Value |
|---------|-------|
| Max stamina | 100 |
| Normal fight cost | 5 stamina |
| Boss fight cost | 10 stamina (level 5 of final zone monster) |
| Recharge rate | 1 stamina per 3 minutes |
| Full recharge time | ~5 hours |
| Fights per full bar | 20 normal fights (or 10 boss fights) |

- Stamina recharges passively via server-side timer (Redis)
- Future monetization: stamina refills, bonus stamina items

---

## Items & Equipment

### Equipment Slots (MVP)

| Slot | Type |
|------|------|
| Weapon | Swords, staffs, daggers, bows |
| Armor | Chest armor, robes, leather |
| Accessory | Rings, amulets, charms |

### Item Rarity

| Rarity | Color | Drop Zone | Stat Multiplier |
|--------|-------|-----------|-----------------|
| Common | Gray | Zone 1+ | 1.0x |
| Uncommon | Green | Zone 1+ | 1.5x |
| Rare | Blue | Zone 2+ | 2.5x |
| Epic | Purple | Zone 3+ | 4.0x |
| Legendary | Orange | Special events / rewards only | 7.0x |

Drop chance increases with zone progression. Zone 4 has a realistic chance for epic drops. Legendary items are exclusive to special events, achievements, or future content.

### Item Drops From Monsters

- Base drop chance: ~10% per fight (Rogue: ~20%)
- Rarity roll happens after drop is confirmed
- Higher monster levels within a zone slightly increase drop chance and rarity odds

### Power Level Calculation

```python
power_level = (
    character.level * 10 +
    character.attack +
    character.defense +
    character.max_hp / 2 +
    sum(item.attack_bonus for item in equipped_items) +
    sum(item.defense_bonus for item in equipped_items) +
    sum(item.hp_bonus for item in equipped_items) / 2
)
```

---

## Potions

### Types

| Potion | Effect | Usage | Shop Price |
|--------|--------|-------|------------|
| Health Potion (S) | Restores 30 HP during combat | Auto-used when HP < 30%, max 3/fight | 20 gold |
| Health Potion (M) | Restores 60 HP during combat | Auto-used when HP < 30%, max 3/fight | 50 gold |
| Health Potion (L) | Restores 100 HP during combat | Auto-used when HP < 30%, max 3/fight | 100 gold |
| Attack Potion | +20% ATK for one fight | Used pre-fight, 1 per fight | 40 gold |

### Rules

- Bought from shop, small chance to drop from monsters
- **Carry limit**: 10 health potions, 5 attack potions at a time
- **Usage limit**: max 3 health potions per fight (auto-used), 1 attack potion per fight (pre-combat)
- Health potions are consumed strongest-first when HP drops below 30%

---

## Shop

- **Per-zone inventory**: each zone has gear appropriate for that level range
- Zone 1 shop sells common gear, Zone 2 sells uncommon, etc.
- Potions available at all zones
- Players can **sell** items back at reduced price (e.g., 40% of buy price)

### Shop Endpoints

```
GET    /shop                    - View current zone's shop items
GET    /shop?zone={zone_id}     - View specific zone's shop
POST   /shop/buy/{item_id}      - Buy item
POST   /shop/sell/{inventory_id} - Sell item from inventory
```

---

## PvP Arena (Simplified for MVP)

### Overview
- **Async PvP**: challenger attacks, defender does not need to be online
- Same auto-resolve system as PvE — stats + gear vs stats + gear
- Separate **PvP ranking points** (not based on power level)

### PvP Tokens
- Players receive **3-5 PvP tokens per day** (daily reset)
- Each PvP challenge costs **1 token**
- PvP does **not** cost stamina — separate resource
- Future monetization: bonus PvP tokens

### Matchmaking
- System shows **3 opponents** close to your PvP point total
- Each opponent shows their **power level indicator** (e.g., "similar", "stronger", "much stronger")
- Players choose who to challenge from those 3

### Rewards
- Winner gains ranking points
- Loser loses a small amount of points (or nothing — TBD for balance)
- Small gold reward for winning

### PvP Ranking

```python
starting_rating = 1000

# Simple ELO-inspired system
points_gained = 20 + (opponent_rating - your_rating) / 25
points_gained = clamp(points_gained, 5, 50)
```

### Future Expansion
- Seasons / resets
- PvP-exclusive gear rewards
- Ranked tiers (Bronze, Silver, Gold, etc.)
- Best-of-3 format

---

## Leaderboards

| Leaderboard | Ranked By | Scope |
|-------------|-----------|-------|
| **Power Level** (primary) | Power level calculation | All players |
| **PvP Rankings** | PvP rating points | All PvP participants |
| **Highest Level** | Character level | All players |

- Cached in Redis, recalculated every 5 minutes
- Show top 100 + your own rank

---

## Account System

### Authentication
- Email + password registration
- JWT token auth (access + refresh tokens)
- Email verification on registration (must verify to play)
- Password reset via email link

### Account Rules
- **One character per account**
- Character name must be unique
- Email must be unique

---

## Admin Dashboard

### MVP Admin Features
- View / search users (by name, email, registration date)
- Ban / suspend accounts (with reason)
- Send email to all users or targeted (by level range, zone, etc.)
- Game stats dashboard: total users, daily active, total fights, most popular class, etc.

### Access
- Admin flag on user account (`is_admin` boolean)
- Separate admin API endpoints with role-based guards
- Admin UI accessible at `/admin` (same React app, guarded routes)

---

## Database Schema

### Core Tables

```sql
-- Users & Authentication
users
├── id (UUID, PK)
├── email (unique)
├── username (unique)
├── password_hash
├── is_verified (boolean, default false)
├── is_admin (boolean, default false)
├── is_banned (boolean, default false)
├── ban_reason (nullable)
├── created_at
└── updated_at

-- Player Characters (one per user)
characters
├── id (UUID, PK)
├── user_id (FK → users, unique)
├── name (unique)
├── class (warrior/mage/rogue/ranger)
├── level (default 1)
├── xp (default 0)
├── gold (default 100)
├── hp (current, resets after combat)
├── max_hp
├── attack
├── defense
├── power_level (cached, recalculated on changes)
├── stamina (default 100)
├── stamina_updated_at (for recharge calculation)
├── pvp_tokens (default 3)
├── pvp_tokens_reset_at (for daily reset)
├── created_at
└── updated_at

-- Zones (static game data)
zones
├── id (UUID, PK)
├── name
├── description
├── order (1-4, determines unlock sequence)
├── recommended_level_min
└── recommended_level_max

-- Monster Templates (static game data)
monsters
├── id (UUID, PK)
├── zone_id (FK → zones)
├── name
├── base_hp
├── base_attack
├── base_defense
├── base_xp_reward
├── base_gold_min
├── base_gold_max
├── order_in_zone (1-4, determines unlock sequence)
└── is_zone_boss (boolean, true for 4th monster)

-- Monster Levels (per-monster scaling data, static)
monster_levels
├── id (UUID, PK)
├── monster_id (FK → monsters)
├── level (1-5)
├── hp_multiplier
├── attack_multiplier
├── defense_multiplier
├── xp_multiplier
├── gold_multiplier
├── drop_chance_bonus
└── UNIQUE(monster_id, level)

-- Monster Drops (which items each monster can drop, static)
monster_drops
├── id (UUID, PK)
├── monster_id (FK → monsters)
├── item_id (FK → items)
├── drop_chance (float, 0.0–1.0)
└── UNIQUE(monster_id, item_id)

-- Player Monster Progress
monster_progress
├── id (UUID, PK)
├── character_id (FK)
├── monster_id (FK)
├── highest_level_beaten (0-5)
├── total_kills
└── UNIQUE(character_id, monster_id)

-- Zone Progress
zone_progress
├── id (UUID, PK)
├── character_id (FK)
├── zone_id (FK)
├── is_unlocked (boolean)
└── UNIQUE(character_id, zone_id)
```

### Items & Inventory

```sql
-- Item Templates (static game data)
items
├── id (UUID, PK)
├── name
├── type (weapon/armor/accessory)
├── rarity (common/uncommon/rare/epic/legendary)
├── attack_bonus
├── defense_bonus
├── hp_bonus
├── buy_price
├── sell_price
├── zone_id (FK, nullable — which zone shop sells this)
└── level_requirement

-- Player Inventory
inventory
├── id (UUID, PK)
├── character_id (FK)
├── item_id (FK)
├── is_equipped (boolean)
└── acquired_at

-- Potion Templates (static game data)
potions
├── id (UUID, PK)
├── name
├── type (health/attack)
├── effect_value (HP restored or ATK % boost)
├── buy_price
└── sell_price

-- Player Potion Inventory
potion_inventory
├── id (UUID, PK)
├── character_id (FK)
├── potion_id (FK)
└── quantity
```

### Combat & PvP

```sql
-- Combat Logs
combat_logs
├── id (UUID, PK)
├── character_id (FK)
├── monster_id (FK)
├── monster_level (1-5)
├── result (win/lose/flee)
├── xp_gained
├── gold_gained
├── item_dropped_id (FK, nullable)
├── turns_taken
├── combat_text (JSON — full turn-by-turn log)
├── potions_used (JSON — list of potions consumed)
├── damage_dealt
├── damage_taken
└── created_at

-- PvP Matches
pvp_matches
├── id (UUID, PK)
├── challenger_id (FK → characters)
├── defender_id (FK → characters)
├── winner_id (FK, nullable)
├── combat_text (JSON — full turn-by-turn log)
├── challenger_damage
├── defender_damage
├── rating_change (points gained/lost)
└── created_at

-- PvP Rankings
pvp_rankings
├── character_id (PK, FK)
├── rating (default 1000)
├── wins
├── losses
└── updated_at
```

### Shop

```sql
-- Shop Listings (per zone)
shop_listings
├── id (UUID, PK)
├── zone_id (FK)
├── item_id (FK, nullable)
├── potion_id (FK, nullable)
├── stock (nullable = infinite)
└── is_active (boolean)
```

---

## API Endpoints

### Auth
```
POST   /auth/register              - Create account (sends verification email)
POST   /auth/login                 - Get JWT tokens
POST   /auth/refresh               - Refresh access token
POST   /auth/verify-email          - Verify email with token
POST   /auth/forgot-password       - Request password reset email
POST   /auth/reset-password        - Reset password with token
GET    /auth/me                    - Get current user
```

### Characters
```
POST   /characters                 - Create character (pick name + class)
GET    /characters/me              - Get my character (stats, power level, stamina)
GET    /characters/{id}            - View any character's public profile
```

### Zones & Monsters
```
GET    /zones                      - List all zones (with unlock status)
GET    /zones/{id}/monsters        - List monsters in zone (with progress)
GET    /monsters/{id}              - Monster details + level scaling info
```

### Combat
```
POST   /combat/fight               - Fight a monster (body: monster_id, level, potions)
GET    /combat/logs                 - My combat history (paginated)
GET    /combat/logs/{id}            - Specific fight details + combat text
```

### Inventory & Equipment
```
GET    /inventory                   - My inventory (items + potions)
POST   /inventory/equip/{id}        - Equip item
POST   /inventory/unequip/{id}      - Unequip item
DELETE /inventory/{id}              - Discard item
```

### Shop
```
GET    /shop                        - View shop items (default: current zone)
GET    /shop?zone={zone_id}         - View specific zone's shop
POST   /shop/buy/{listing_id}       - Buy item or potion
POST   /shop/sell/{inventory_id}    - Sell item from inventory
```

### PvP
```
GET    /pvp/opponents               - Get 3 matched opponents
POST   /pvp/challenge/{char_id}     - Challenge a player
GET    /pvp/history                  - My PvP match history
GET    /pvp/rankings                 - PvP leaderboard
```

### Leaderboards
```
GET    /leaderboards/power          - Top players by power level
GET    /leaderboards/level          - Top players by character level
GET    /leaderboards/pvp            - Top players by PvP rating
```

### Admin
```
GET    /admin/users                  - List/search users
GET    /admin/users/{id}             - User details
PATCH  /admin/users/{id}/ban         - Ban/unban user
POST   /admin/email/blast            - Send email to users (all or filtered)
GET    /admin/stats                  - Game statistics dashboard data
```

---

## Frontend Pages

```
/                          - Landing page (game intro, register CTA)
/login                     - Login form
/register                  - Registration form
/verify-email              - Email verification page
/forgot-password           - Password reset request
/reset-password            - Password reset form

/game                      - Main game dashboard (character summary, stamina, quick actions)
/game/character            - Character stats, equipment, power level
/game/zones                - Zone map, progression overview
/game/zones/{id}           - Monster list for zone, fight selection
/game/combat/{log_id}      - Combat result / detailed log view
/game/inventory            - Inventory management (items + potions)
/game/shop                 - Buy/sell items and potions
/game/pvp                  - PvP arena (matchmaking, fight, history)
/game/leaderboards         - Rankings (power, level, PvP)

/admin                     - Admin dashboard
/admin/users               - User management
/admin/email               - Email broadcast tool
/admin/stats               - Game statistics
```

### UI Theme
- **Color palette**: warm gold, brown, red, bordeaux accents
- **Style**: modern web interface, clean layout, not terminal/dark MUD
- **Combat log**: styled text output panel (monospace optional for log, modern UI for everything else)
- **Responsive**: desktop-first, mobile as stretch goal

---

## Development Phases

### Phase 1: Foundation & Core (Target: ~15-20 hours)

- [x] **Project setup**
  - [x] Initialize FastAPI backend project with project structure (`app/`, `routers/`, `models/`, `schemas/`, `services/`, `core/`)
  - [x] Initialize React + TypeScript frontend with Vite
  - [x] Install and configure Tailwind CSS v4 with `@tailwindcss/vite` plugin
  - [x] Create `docker-compose.yml` with FastAPI, PostgreSQL, and Redis services
  - [x] Set up environment variables (`.env` + `.env.example`)
  - [x] Create `.gitignore`
  - [x] Verify all services start and can communicate

- [ ] **PostgreSQL + Redis setup with migrations**
  - [x] Install SQLAlchemy + Alembic for database ORM and migrations
  - [x] Configure `app/core/config.py` (pydantic-settings, reads from `.env`)
  - [x] Configure `app/core/database.py` (SQLAlchemy engine, session, Base)
  - [x] Configure `app/main.py` (FastAPI app, CORS, health check endpoint)
  - [x] Configure `alembic/env.py` (reads DB URL from app settings, uses Base.metadata)
  - [x] Configure `app/core/enums.py` (ClassType, ItemRarity, ItemType, PotionType, CombatResult)
  - [x] Create `models/user.py` (UUID PK, email, username, hashed_password, is_verified, is_admin, is_banned, ban_reason, timestamps)
  - [x] Create `models/character.py` (UUID PK, user_id FK, stats, power_level, stamina, pvp_tokens default 3, check constraints, timestamps — pvp_rating lives in pvp_rankings)
  - [x] Create `models/zone.py`, `models/monster.py`, `models/monster_level.py`, `models/monster_progress.py`, `models/zone_progress.py`
  - [x] Create `models/item.py`, `models/inventory.py`, `models/potion.py`, `models/potion_inventory.py`
  - [x] Create `models/combat_logs.py`, `models/pvp_matches.py`, `models/monster_drops.py`, `models/shop_listings.py`, `models/pvp_ranking.py`
  - [x] Run first migration: `alembic revision --autogenerate -m "initial"` and `alembic upgrade head`
  - [x] Run second migration: `alembic revision --autogenerate -m "add remaining models"` and `alembic upgrade head`
  - [ ] Verify Redis connection and basic get/set operations
  - [ ] Create a seed script runner for loading static game data later

- [x] **User auth (register, login, JWT, email verification, password reset)**
  - [x] Create Pydantic schemas for register, login, token response, password reset
  - [x] Implement password hashing with bcrypt
  - [x] `POST /auth/register` — validate email uniqueness, hash password, create user, send verification email, return success
  - [x] `POST /auth/login` — verify email + password, check is_verified, check is_banned, return access + refresh JWT tokens
  - [x] `POST /auth/refresh` — validate refresh token, issue new access token
  - [x] `GET /auth/me` — JWT-protected endpoint, return current user info
  - [x] `GET /auth/verify` — accept token from email link, set is_verified = true
  - [x] `POST /auth/forgot-password` — validate email exists, send password reset email with token
  - [x] `POST /auth/reset-password` — accept token + new password, update password_hash
  - [x] Create JWT utility functions (create_access_token, create_refresh_token, decode_token)
  - [x] Create auth dependency (`get_current_user`) for protecting routes

- [x] **Email service integration**
  - [x] Choose and set up Resend account
  - [x] Create email utility module (`app/services/email.py`)
  - [x] Create email verification template (HTML with token link)
  - [x] Create password reset template (HTML with reset link)
  - [x] Test email sending in development (Resend onboarding@resend.dev sender)

- [x] **Character creation (name, class selection)**
  - [x] `POST /characters` — validate name uniqueness, validate class enum (warrior/mage/rogue/ranger), set starting stats based on class table, create character linked to user
  - [x] Apply class-specific base stats: Warrior (120 HP, 10 ATK, 8 DEF), Mage (80/15/4), Rogue (100/12/5), Ranger (100/11/6)
  - [x] Set defaults: level 1, xp 0, gold 100, stamina 100
  - [ ] Ensure one character per user (unique constraint on user_id)
  - [ ] Frontend: class selection screen with class descriptions, stat previews, and name input

- [x] **Character stats view + power level calculation**
  - [x] `GET /characters/me` — return full character stats, current stamina (calculated), power level, equipped items (empty for now)
  - [x] `GET /characters/{id}` — return public profile (name, class, level, power level — no gold/stamina)
  - [x] Implement power level formula: `level*10 + attack + defense + max_hp/2 + equipment bonuses`
  - [ ] Create utility function to recalculate and cache power_level on character changes
  - [ ] Frontend: character stats page showing all stats, class, level, XP progress bar, power level

- [ ] **Stamina system**
  - [ ] Implement stamina calculation on-read: `current_stamina = min(100, stored_stamina + minutes_since_update / 3)`
  - [ ] Create stamina deduction function: subtract stamina, update `stamina_updated_at` timestamp
  - [ ] Return stamina + time until next stamina point in character API responses
  - [ ] Frontend: stamina bar display with current/max and time-to-next-point countdown

- [ ] **Frontend foundation**
  - [ ] Set up React Router with route structure (/, /login, /register, /game, /game/character, etc.)
  - [ ] Create auth context/store (JWT storage, login/logout, auto-refresh)
  - [ ] Create protected route wrapper (redirect to /login if not authenticated)
  - [ ] Build landing page with game intro and register CTA
  - [ ] Build login and register forms with validation
  - [ ] Build main game layout shell (sidebar nav, content area, stamina bar)
  - [ ] Set up API client (axios or fetch wrapper with JWT headers)

### Phase 2: Combat & Progression (Target: ~10-15 hours)

- [ ] **Zone and monster seed data**
  - [x] Create migrations: `zones` table (id, name, description, order, recommended_level_min/max)
  - [x] Create migrations: `monsters` table (id, zone_id FK, name, base_hp/attack/defense, base_xp_reward, base_gold_min/max, order_in_zone, is_zone_boss)
  - [x] Create migrations: `monster_levels` table (monster_id FK, level 1-5, multipliers for hp/attack/defense/xp/gold, drop_chance_bonus — per-monster, not global)
  - [x] Create migrations: `monster_drops` table (monster_id FK, item_id FK, drop_chance float — explicit per-monster item drop pool)
  - [x] Create migrations: `monster_progress` table (character_id, monster_id, highest_level_beaten, total_kills)
  - [x] Create migrations: `zone_progress` table (character_id, zone_id, is_unlocked)
  - [ ] Write seed data script: insert all 4 zones with descriptions
  - [ ] Write seed data script: insert all 16 monsters with base stats (see Seed Data section)
  - [ ] Write seed data script: insert monster level multipliers (1.0x through 2.5x)
  - [ ] Auto-unlock Zone 1 for new characters on creation

- [ ] **Monster progression system (unlock logic)**
  - [ ] `GET /zones` — list all zones with is_unlocked status for current character
  - [ ] `GET /zones/{id}/monsters` — list monsters in zone with progress (highest_level_beaten, total_kills, is_unlocked)
  - [ ] Implement unlock check: next monster unlocks when current monster's highest_level_beaten >= 3
  - [ ] Implement zone unlock check: zone N+1 unlocks when final monster in zone N has highest_level_beaten = 5
  - [ ] First monster in each zone auto-unlocks when zone is unlocked
  - [ ] Frontend: zone overview page with zone cards showing lock/unlock state and progress
  - [ ] Frontend: monster list page per zone with level progress indicators and fight buttons

- [ ] **Turn-by-turn combat engine (auto-resolve)**
  - [ ] Create combat service (`app/services/combat.py`)
  - [ ] Load monster stats: base stats × level multiplier for the selected monster level
  - [ ] Load character stats: base stats + equipped item bonuses + potion buffs
  - [ ] Implement combat loop:
    - Alternate turns: player attacks → monster attacks (repeat)
    - Each turn: roll hit chance (0.85 + level_diff × 0.03, clamped 0.50-0.95)
    - On hit: calculate damage (attack - defense/2, ±20% variance, min 1)
    - Roll crit chance (10% base, 15% Rogue): multiply damage by 1.5
    - Roll dodge chance (5% + defense/200, clamped 5%-20%): negate damage
    - Check health potion auto-use: if HP < 30% and potions available (max 3/fight), restore HP
    - Check if either side HP <= 0 → end combat
  - [ ] Return structured combat result: winner, turns taken, damage dealt/taken, potions used

- [ ] **Combat log generation (detailed text)**
  - [ ] Build turn-by-turn text log during combat simulation
  - [ ] Format: "Turn X: You strike [Monster] for Y damage. ([Monster] HP: current/max)"
  - [ ] Include hit/miss/crit/dodge events: "Goblin misses!", "Critical hit! You deal X damage"
  - [ ] Include potion events: "Health potion used! Restored 60 HP."
  - [ ] Include victory/defeat summary with XP, gold, item drops
  - [ ] Store as JSON array of log entries in combat_logs table

- [ ] **XP, gold, and loot rewards**
  - [ ] Create migration: `combat_logs` table (character_id, monster_id, monster_level, result, xp_gained, gold_gained, item_dropped_id, turns_taken, combat_text JSON, potions_used JSON, damage_dealt, damage_taken, created_at)
  - [ ] On win: calculate gold (random between monster gold_min and gold_max × level multiplier)
  - [ ] Apply class bonus: Mage gets +15% gold
  - [ ] On win: calculate XP (monster base_xp × level multiplier)
  - [ ] Apply class bonus: Ranger gets +15% XP
  - [ ] On win: roll for item drop (base 10% chance, Rogue 20%) — placeholder until Phase 3
  - [ ] On lose: no rewards, but stamina is still consumed
  - [ ] Update character gold, xp, and monster_progress (highest_level_beaten, total_kills)
  - [ ] Check and trigger unlock events (next monster, next zone)
  - [ ] Wrap all reward logic in a database transaction

- [ ] **Level up system with class-based stat growth**
  - [ ] After XP is added, check if `xp >= level * 100`
  - [ ] On level up: subtract xp_to_next from current xp, increment level
  - [ ] Apply class stat growth: Warrior (+12 HP, +2 ATK, +2 DEF), Mage (+6/+3/+1), Rogue (+8/+2/+1), Ranger (+10/+2/+1)
  - [ ] Recalculate power_level after stat changes
  - [ ] Handle multi-level-ups (if XP gained covers multiple levels, loop)
  - [ ] Include level up events in combat log: "Level up! You are now level X!"

- [ ] **Combat UI**
  - [ ] `POST /combat/fight` — accept body: { monster_id, monster_level, use_attack_potion: bool }
  - [ ] Validate: character has stamina, monster is unlocked, monster level is <= highest_beaten + 1
  - [ ] `GET /combat/logs` — paginated combat history (most recent first)
  - [ ] `GET /combat/logs/{id}` — specific fight details with full combat text
  - [ ] Frontend: fight initiation screen (select monster level, toggle attack potion, confirm)
  - [ ] Frontend: combat result page with scrolling turn-by-turn text log, styled with color for crits/misses/potions
  - [ ] Frontend: victory/defeat banner with reward summary (XP, gold, item drop, level up)
  - [ ] Frontend: combat history page with recent fights list

### Phase 3: Items & Economy (Target: ~8-10 hours)

- [ ] **Item system (templates, rarity)**
  - [ ] Create migration: `items` table (id, name, type, rarity, attack_bonus, defense_bonus, hp_bonus, buy_price, sell_price, zone_id FK nullable, level_requirement)
  - [ ] Write seed data: Zone 1 items (common + uncommon weapons, armor, accessories)
  - [ ] Write seed data: Zone 2 items (uncommon + rare)
  - [ ] Write seed data: Zone 3 items (rare + epic)
  - [ ] Write seed data: Zone 4 items (epic, small chance for special items)
  - [ ] Define sell_price = 40% of buy_price for all items
  - [ ] Set level_requirement per item (roughly matching zone recommended levels)

- [ ] **Inventory management (equip, unequip, discard)**
  - [ ] Create migration: `inventory` table (id, character_id FK, item_id FK, is_equipped boolean, acquired_at)
  - [ ] `GET /inventory` — return all items in character's inventory with equipped status and item details
  - [ ] `POST /inventory/equip/{id}` — validate: item exists in inventory, character meets level_requirement, slot not already occupied (auto-unequip if it is)
  - [ ] `POST /inventory/unequip/{id}` — set is_equipped = false
  - [ ] `DELETE /inventory/{id}` — remove item from inventory (cannot discard equipped items)
  - [ ] Recalculate power_level after any equip/unequip change
  - [ ] Enforce equipment rules: only 1 weapon, 1 armor, 1 accessory equipped at a time
  - [ ] Frontend: inventory grid showing items with rarity color coding (gray/green/blue/purple/orange)
  - [ ] Frontend: equip/unequip buttons, stat comparison tooltip when hovering items
  - [ ] Frontend: equipped items display on character stats page

- [ ] **Potion system**
  - [ ] Create migration: `potions` table (id, name, type, effect_value, buy_price, sell_price)
  - [ ] Create migration: `potion_inventory` table (character_id FK, potion_id FK, quantity)
  - [ ] Seed data: Health Potion S (30 HP, 20g), M (60 HP, 50g), L (100 HP, 100g), Attack Potion (+20% ATK, 40g)
  - [ ] Enforce carry limits: max 10 health potions total, max 5 attack potions
  - [ ] Integrate with combat engine: auto-use health potions when HP < 30% (strongest first, max 3/fight)
  - [ ] Integrate with combat engine: apply attack potion buff (+20% ATK) when use_attack_potion = true
  - [ ] Deduct potions from potion_inventory after combat
  - [ ] Include potion usage in combat log text
  - [ ] Frontend: potion inventory display with quantities
  - [ ] Frontend: pre-fight screen shows potion selection (toggle attack potion, set health potion loadout)

- [ ] **Shop per zone (buy/sell)**
  - [ ] Create migration: `shop_listings` table (id, zone_id FK, item_id FK nullable, potion_id FK nullable, stock nullable, is_active)
  - [ ] Seed data: populate shop listings for each zone with appropriate items + all potions
  - [ ] `GET /shop?zone={zone_id}` — return shop listings for a zone (default: character's highest unlocked zone)
  - [ ] `POST /shop/buy/{listing_id}` — validate: character has enough gold, item meets requirements, carry limit not exceeded (potions), deduct gold, add to inventory/potion_inventory
  - [ ] `POST /shop/sell/{inventory_id}` — validate: item not equipped, calculate sell price (40% buy), add gold, remove from inventory
  - [ ] Frontend: shop page with tabs for weapons/armor/accessories/potions
  - [ ] Frontend: buy button with gold cost, sell button with gold return
  - [ ] Frontend: zone selector to browse shops from different zones

- [ ] **Item drops from monsters**
  - [ ] On combat win: roll drop chance (base 10%, Rogue 20%, + drop_chance_bonus from monster_levels row)
  - [ ] If drop confirmed: pick a random item from the monster's monster_drops entries, weighted by drop_chance
  - [ ] Fallback: if monster has no monster_drops entries, no item drops
  - [ ] Add dropped item to character's inventory
  - [ ] Store item_dropped_id in combat_log
  - [ ] Include drop in combat log text: "Item Drop: [Item Name] ([rarity])"
  - [ ] Frontend: highlight item drops in combat result with rarity color

- [ ] **Power level recalculation on gear changes**
  - [ ] Call power_level recalc on: equip, unequip, level up, item discard
  - [ ] Include equipped item bonuses in formula: sum attack_bonus, defense_bonus, hp_bonus/2
  - [ ] Update cached power_level field on character record
  - [ ] Verify power_level updates propagate to leaderboard (Phase 4)

### Phase 4: Competition & Social (Target: ~8-12 hours)

- [ ] **Leaderboards (power level, character level, PvP)**
  - [ ] `GET /leaderboards/power` — top 100 players by power_level + requesting player's own rank
  - [ ] `GET /leaderboards/level` — top 100 players by character level (tiebreaker: XP)
  - [ ] `GET /leaderboards/pvp` — top 100 players by PvP rating
  - [ ] Cache leaderboard results in Redis with 5-minute TTL
  - [ ] On cache miss: query DB, sort, cache result, return
  - [ ] Include player's own rank even if not in top 100
  - [ ] Frontend: leaderboard page with tabs for Power/Level/PvP
  - [ ] Frontend: highlight current player's row, show rank number, class icon, name, score
  - [ ] Frontend: click player name to view their public profile

- [ ] **PvP arena (matchmaking, async combat, rankings)**
  - [ ] Create migration: `pvp_matches` table (challenger_id, defender_id, winner_id, combat_text JSON, challenger_damage, defender_damage, rating_change, created_at)
  - [ ] Create migration: `pvp_rankings` table (character_id PK, rating default 1000, wins, losses, updated_at)
  - [ ] Auto-create pvp_rankings row when character first enters PvP
  - [ ] `GET /pvp/opponents` — find 3 players closest to character's PvP rating (exclude self, exclude recently fought)
  - [ ] Return opponent info: name, class, level, power_level, PvP rating, power indicator ("weaker"/"similar"/"stronger"/"much stronger")
  - [ ] `POST /pvp/challenge/{char_id}` — validate: character has PvP tokens, opponent exists
  - [ ] Deduct 1 PvP token, run combat simulation (character vs opponent's stats+gear)
  - [ ] Calculate rating change: `20 + (opponent_rating - your_rating) / 25`, clamped 5-50
  - [ ] Winner gains points, loser loses half that amount (minimum 0)
  - [ ] Update pvp_rankings for both players, save pvp_match record
  - [ ] Implement daily PvP token reset: on read, if pvp_tokens_reset_at is before today, reset to 3 tokens
  - [ ] `GET /pvp/history` — paginated PvP match history with opponent names and results
  - [ ] Frontend: PvP arena page showing remaining tokens, 3 opponent cards with stats
  - [ ] Frontend: challenge confirmation modal with opponent comparison
  - [ ] Frontend: PvP combat result with turn-by-turn log (same style as PvE)
  - [ ] Frontend: PvP match history list

- [ ] **Admin dashboard**
  - [ ] Create admin auth middleware: check `is_admin = true` on user, reject with 403 if not
  - [ ] `GET /admin/users` — list users with search (by name, email), pagination, filters (banned, verified, date range)
  - [ ] `GET /admin/users/{id}` — full user details: account info, character stats, combat history, PvP record
  - [ ] `PATCH /admin/users/{id}/ban` — set is_banned + ban_reason, or unban (clear both)
  - [ ] `POST /admin/email/blast` — accept subject, body, filter criteria (all users, by level range, by zone, by class), queue emails via email service
  - [ ] `GET /admin/stats` — return: total users, daily active (logged in last 24h), total fights today, fights all time, most popular class, avg player level, total gold in economy
  - [ ] Frontend: admin layout with sidebar nav (Dashboard, Users, Email)
  - [ ] Frontend: admin dashboard with stat cards and basic charts
  - [ ] Frontend: user management table with search, ban/unban buttons, link to user detail
  - [ ] Frontend: email blast form with recipient filters, subject, body, preview, send button
  - [ ] Guard admin routes: redirect non-admins away from /admin/*

- [ ] **Polish UI, responsive tweaks**
  - [ ] Consistent spacing, typography, and color usage across all pages
  - [ ] Loading states (spinners/skeletons) for all API calls
  - [ ] Error handling: toast notifications for failed actions, inline errors on forms
  - [ ] Empty states: no inventory, no combat history, no guild yet
  - [ ] Confirmation dialogs for destructive actions (discard item, sell item)
  - [ ] Animate combat log text (typewriter effect or progressive reveal)
  - [ ] Test all pages at tablet width (~768px), fix major layout breaks
  - [ ] Accessibility basics: semantic HTML, focus states, aria labels on buttons

- [ ] **Final balancing pass**
  - [ ] Play through Zone 1 → Zone 4 progression: verify XP curve feels right (~2-3 days per zone)
  - [ ] Verify gold economy: can players afford shop upgrades at a reasonable pace?
  - [ ] Test each class: does each passive feel impactful? (Mage gold, Rogue drops, Ranger XP, Warrior tankiness)
  - [ ] Verify monster difficulty scaling: level 1 should be easy, level 5 should require good gear
  - [ ] Test PvP: do matches between similar-power players feel fair? Is rating gain/loss balanced?
  - [ ] Check item power curve: is each zone's gear a meaningful upgrade over the previous?
  - [ ] Adjust any numbers that feel off (monster stats, item prices, XP rewards, potion costs)
  - [ ] Document final values if they differ from spec

### Future Features (Post-MVP)
- [ ] Guild system (create, join, ranks)
- [ ] Guild chat (WebSockets)
- [ ] Guild raids (cooperative boss fights, HP doesn't reset)
- [ ] Dungeons (multi-fight sequences, HP persists)
- [ ] Friend system
- [ ] World events (time-limited, special rewards)
- [ ] Legendary item acquisition (events, achievements)
- [ ] Seasons / PvP resets
- [ ] Mobile responsive polish
- [ ] Monetization (stamina refills, cosmetics)

---

## Seed Data

### Zone 1: Whispering Forest

| Monster | Base HP | ATK | DEF | XP | Gold Range |
|---------|---------|-----|-----|----|------------|
| Slime | 25 | 4 | 2 | 15 | 5-15 |
| Goblin | 40 | 7 | 3 | 30 | 10-25 |
| Wolf | 55 | 10 | 5 | 50 | 15-35 |
| Treant (Boss) | 80 | 13 | 8 | 80 | 30-60 |

### Zone 2: Darkstone Caves

| Monster | Base HP | ATK | DEF | XP | Gold Range |
|---------|---------|-----|-----|----|------------|
| Bat | 60 | 12 | 6 | 70 | 25-50 |
| Spider | 80 | 15 | 8 | 100 | 35-70 |
| Orc | 110 | 20 | 12 | 150 | 50-100 |
| Cave Troll (Boss) | 160 | 25 | 16 | 220 | 80-150 |

### Zone 3: Shattered Ruins

| Monster | Base HP | ATK | DEF | XP | Gold Range |
|---------|---------|-----|-----|----|------------|
| Skeleton | 130 | 22 | 14 | 200 | 70-130 |
| Wraith | 160 | 28 | 16 | 280 | 90-170 |
| Golem | 220 | 32 | 22 | 380 | 120-220 |
| Lich (Boss) | 300 | 40 | 28 | 500 | 180-320 |

### Zone 4: Ember Volcano

| Monster | Base HP | ATK | DEF | XP | Gold Range |
|---------|---------|-----|-----|----|------------|
| Fire Imp | 250 | 35 | 20 | 450 | 150-280 |
| Lava Serpent | 320 | 42 | 26 | 600 | 200-380 |
| Infernal Orc | 400 | 50 | 32 | 800 | 280-500 |
| Elder Dragon (Boss) | 550 | 60 | 40 | 1200 | 500-900 |

### Starter Shop Items (Zone 1)

```json
[
  {"name": "Wooden Sword", "type": "weapon", "rarity": "common", "attack_bonus": 3, "buy_price": 50},
  {"name": "Leather Vest", "type": "armor", "rarity": "common", "defense_bonus": 2, "buy_price": 60},
  {"name": "Copper Ring", "type": "accessory", "rarity": "common", "hp_bonus": 10, "buy_price": 40},
  {"name": "Iron Sword", "type": "weapon", "rarity": "uncommon", "attack_bonus": 7, "buy_price": 200},
  {"name": "Chain Mail", "type": "armor", "rarity": "uncommon", "defense_bonus": 5, "buy_price": 250},
  {"name": "Silver Amulet", "type": "accessory", "rarity": "uncommon", "hp_bonus": 25, "buy_price": 180}
]
```

---

## Technical Notes

- Use database transactions for combat to prevent gold/item duplication exploits
- Cache leaderboards in Redis, recalculate every 5 minutes
- Stamina calculated on-read from `stamina_updated_at`, not a background job
- Rate limit combat endpoints to prevent botting (e.g., max 1 fight per 2 seconds)
- Store combat logs as JSON for the turn-by-turn text, structured data for stats
- Item sell price = 40% of buy price
- All monster/item/potion data is static seed data, loaded via migrations
