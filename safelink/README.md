# SafeLink Full-Stack Web App

A scalable, modern web application to connect vulnerable populations with resources, support, and emergency help.

## Project Structure

```
safelink/
├── backend/                      # Flask backend API
│   ├── app/
│   │   ├── __init__.py           # Flask app factory
│   │   ├── config.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── ai.py
│   │   │   ├── resources.py
│   │   │   ├── users.py
│   │   │   └── cases.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── help_request.py
│   │   ├── services/
│   │   │   ├── supabase.py
│   │   │   ├── claude_api.py
│   │   │   ├── mapbox.py
│   │   │   └── sms.py
│   │   └── utils/
│   │       ├── auth_utils.py
│   │       └── geo_utils.py
│   ├── migrations/
│   ├── tests/
│   ├── run.py
│   └── requirements.txt
│
├── frontend/                     # React frontend
│   ├── public/
│   ├── src/
│   │   ├── assets/               # Static assets like icons, images
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Page-level views (Home, Map, Login)
│   │   ├── layouts/              # Page layouts
│   │   ├── hooks/                # Custom React hooks
│   │   ├── context/              # Global context providers
│   │   ├── services/             # Frontend API clients
│   │   │   ├── apiClient.js
│   │   │   ├── supabaseClient.js
│   │   │   └── aiClient.js
│   │   └── App.jsx
│   ├── .env
│   ├── index.html
│   ├── vite.config.js            # or next.config.js if using Next.js
│   └── package.json
│
├── shared/                       # Shared data, schemas, or types
│   └── constants/
│       ├── userRoles.js
│       └── serviceTypes.js
│
├── .env                          # Root-level config
├── README.md
├── docker-compose.yml            # Optional: run frontend/backend/db locally
└── Makefile                      # Optional: setup commands
```

## Dev Workflow

| Layer        | Framework      | Runs At          | Dev Command                  |
| ------------ | -------------- | ---------------- | ---------------------------- |
| **Backend**  | Flask API      | `localhost:5000` | `flask run` or `make dev`    |
| **Frontend** | React/Vite     | `localhost:5173` | `npm run dev`                |
| **DB/Auth**  | Supabase Cloud | Supabase Studio  | auto-deployed                |
| **AI**       | Claude API     | External         | via `services/claude_api.py` |

## Features
- Map-based resource search (Mapbox)
- AI-powered help and triage (Claude API)
- Secure authentication (Supabase)
- SMS alerts (Twilio)
- Volunteer and social worker dashboards
- Modern, responsive React UI

## Deployment
- Frontend: Vercel
- Backend: Render or Railway
- Database/Auth: Supabase

---

For setup, see the README files in `backend/` and `frontend/`. 