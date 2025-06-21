# SafeRent SF 🏠

A modern, AI-powered web application for finding safe and affordable rental properties in San Francisco with real-time crime data and neighborhood insights.

## ✨ Features

- **🔍 Smart Property Search** - Find rentals with integrated crime data
- **🗺️ Interactive Maps** - Explore neighborhoods with Mapbox integration
- **🤖 AI-Powered Insights** - Get personalized recommendations using Claude AI
- **🔐 Secure Authentication** - User accounts and saved listings with Supabase
- **📊 Real-time Crime Data** - Safety ratings and crime statistics
- **🎤 Voice Search** - Voice-to-AI interface for hands-free searching

## 🛠 Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js, React, TailwindCSS |
| **Backend** | Flask (Python) |
| **Database & Auth** | Supabase (PostgreSQL) |
| **Maps** | Mapbox |
| **AI** | Claude API |
| **Voice** | Vapi |
| **Deployment** | Vercel (Frontend), Render/Railway (Backend) |

## 📁 Project Structure

```
safelink-app/
├── frontend/                     # Next.js React frontend
│   ├── src/
│   │   ├── pages/               # Next.js pages
│   │   │   ├── index.jsx        # Home page
│   │   │   ├── login.jsx        # Authentication
│   │   │   └── test-supabase.jsx # Supabase connection test
│   │   └── lib/
│   │       └── supabaseClient.js # Supabase integration
│   ├── package.json
│   ├── next.config.js
│   └── vercel.json
│
├── backend/                      # Flask API backend
│   ├── app/
│   │   ├── routes/              # API endpoints
│   │   │   ├── ai.py            # Claude AI integration
│   │   │   ├── alerts.py        # Crime alerts
│   │   │   ├── crime.py         # Crime data API
│   │   │   └── rentals.py       # Rental listings
│   │   ├── services/            # Business logic
│   │   │   ├── claude_client.py # AI client
│   │   │   ├── crime_data.py    # Crime data service
│   │   │   ├── map_utils.py     # Map utilities
│   │   │   └── scraper.py       # Data scraping
│   │   └── utils/
│   │       └── geo.py           # Geospatial utilities
│   ├── requirements.txt
│   └── config.py
│
├── database/
│   └── schema.sql               # Database schema
│
├── workflows/                    # Automated tasks
│   ├── daily_scrape_task.py     # Daily data updates
│   └── notify_crime_alert.py    # Crime alert notifications
│
└── docs/
    └── design_doc.md            # Project documentation
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Supabase account
- Mapbox account
- Claude API key

### Frontend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/DianaTao/safelink-app.git
   cd safelink-app
   ```

2. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

3. **Set up environment variables**
   Create `frontend/.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```
   Open [http://localhost:3000](http://localhost:3000) in your browser.

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create `backend/.env`:
   ```env
   CLAUDE_API_KEY=your_claude_api_key
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your_supabase_service_key
   ```

4. **Run the Flask server**
   ```bash
   flask run
   ```
   The API will be available at `http://localhost:5000`

## 🌐 Deployment

### Frontend (Vercel)
- **Automatic deployment** from GitHub main branch
- **Environment variables** configured in Vercel dashboard
- **Live URL**: Your Vercel deployment URL

### Backend (Render/Railway)
- **Deploy from GitHub** or connect directly
- **Environment variables** set in deployment platform
- **API URL**: Your backend deployment URL

## 📱 Available Pages

- **Home** (`/`) - Landing page with feature overview
- **Login** (`/login`) - User authentication
- **Test Supabase** (`/test-supabase`) - Database connection test

## 🔧 Development

### Adding New Features
1. Create feature branch: `git checkout -b feature-name`
2. Make changes in `frontend/src/` or `backend/app/`
3. Test locally with `npm run dev` and `flask run`
4. Commit and push: `git push origin feature-name`
5. Create pull request to main

### Code Style
- **Frontend**: JavaScript with React hooks
- **Backend**: Python with Flask
- **Styling**: TailwindCSS for consistent design

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the [documentation](docs/design_doc.md)
- Open an issue on GitHub
- Contact the development team

---

**Built with ❤️ for safer housing in San Francisco** 