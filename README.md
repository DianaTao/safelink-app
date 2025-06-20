# SafeRent SF

A modern, AI-powered web app for safe, affordable housing search in San Francisco.

## 🗂️ Project Structure

```
saferent-sf/
├── frontend/                     # React web frontend (Next.js)
│   ├── public/                   # Static assets
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── MapView.tsx       # Mapbox heatmap + rentals
│   │   │   ├── ListingCard.tsx   # Rental info card
│   │   │   ├── VoiceSearch.tsx   # Vapi integration
│   │   │   └── Header.tsx
│   │   ├── pages/
│   │   │   ├── index.tsx         # Main landing/map page
│   │   │   ├── saved.tsx         # Saved rentals
│   │   │   └── login.tsx         # Supabase auth
│   │   ├── lib/                  # Utility libraries
│   │   │   ├── supabaseClient.ts # Auth + DB connection
│   │   │   ├── apiClient.ts      # Wrapper for calling Flask backend
│   │   │   └── mapbox.ts         # Mapbox init config
│   │   ├── styles/
│   │   │   └── globals.css
│   │   └── app.tsx
│   ├── .env.local                # Mapbox, Supabase keys
│   └── next.config.js
│
├── backend/                      # Flask backend API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── rentals.py        # Craigslist scraping & parsing
│   │   │   ├── crime.py          # SF crime data API access
│   │   │   ├── ai.py             # Claude AI summaries
│   │   │   └── alerts.py         # Orkes workflow alerts
│   │   ├── services/
│   │   │   ├── scraper.py        # Craigslist scraping logic
│   │   │   ├── crime_data.py     # SFPD data fetcher
│   │   │   ├── claude_client.py  # Claude API handler
│   │   │   └── map_utils.py
│   │   ├── utils/
│   │   │   └── geo.py
│   │   └── main.py               # Flask entrypoint
│   ├── requirements.txt
│   ├── config.py
│   └── .env                      # Claude API, Supabase secrets
│
├── database/                     # SQL or Supabase schema reference
│   └── schema.sql
│
├── workflows/                    # Orkes / Lambda / cron tasks
│   ├── notify_crime_alert.py
│   └── daily_scrape_task.py
│
├── docs/
│   ├── design_doc.md
│   └── sponsor_mapping.md
│
├── README.md
├── .gitignore
└── package.json                  # Monorepo tool like Turbo or custom script
```

## 🛠 Tech Stack

| Area              | Tech/Platform                                      |
| ----------------- | -------------------------------------------------- |
| **Frontend**      | Next.js (React, TailwindCSS), Vercel               |
| **Backend**       | Flask (Python), Fly.io or Lambda                   |
| **Database/Auth** | Supabase (PostgreSQL + Auth)                       |
| **Maps**          | Mapbox                                             |
| **AI**            | Claude API                                         |
| **Voice**         | Vapi (voice-to-AI)                                 |
| **Workflows**     | Orkes (crime alert pipelines, scheduled tasks)      |

## 🧪 Dev Tools

| Tool           | Role                             |
| -------------- | -------------------------------- |
| **Vercel**     | Deploy `frontend/` (Next.js app) |
| **Fly.io**     | Deploy `backend/` (Flask API)    |
| **Supabase**   | Auth, user db, saved listings    |
| **Mapbox**     | Safety heatmap + rentals map     |
| **Claude API** | AI summaries, neighborhood tips  |
| **Vapi**       | Voice-to-AI interface            |
| **Orkes**      | Crime alert pipelines (optional) |

## 🚀 Quick Start

1. Clone the repo: `git clone ...`
2. Install frontend deps: `cd frontend && npm install`
3. Install backend deps: `cd backend && pip install -r requirements.txt`
4. Set up `.env.local` and `.env` files for secrets
5. Run frontend: `npm run dev` (in `frontend/`)
6. Run backend: `flask run` (in `backend/`)

---

For more, see `docs/design_doc.md` and the code in each subfolder. 