# SafeLink App

A Flask-based web application designed to connect vulnerable populations with essential resources, support services, and emergency assistance.

## Features

- **Authentication & Authorization**: Secure user management with Supabase
- **AI-Powered Assistance**: Claude AI integration for intelligent resource matching
- **Resource Management**: Comprehensive database of shelters, food banks, legal aid, and support services
- **Emergency Alerts**: Real-time notification system for crisis situations
- **Case Management**: Track help requests and support cases
- **Multi-Role Support**: Volunteers, social workers, and service providers
- **Geolocation Services**: Mapbox integration for location-based services
- **SMS Notifications**: Twilio integration for emergency communications

## Project Structure

```
safelink-app/
├── app/                      # Flask application package
│   ├── __init__.py           # App factory, load config
│   ├── config.py             # Configuration settings
│   ├── routes/               # Flask Blueprints
│   │   ├── __init__.py
│   │   ├── auth.py           # Supabase auth endpoints
│   │   ├── ai.py             # Claude assistant endpoints
│   │   ├── resources.py      # Map data, shelter, food, legal, etc.
│   │   ├── alerts.py         # Emergency notification system
│   │   ├── users.py          # Profile, volunteer, social worker roles
│   │   └── cases.py          # Help request / case management
│   ├── services/             # API clients and integrations
│   │   ├── supabase.py       # Supabase auth and DB wrapper
│   │   ├── claude_api.py     # Claude API call wrapper
│   │   ├── mapbox.py         # Mapbox integration
│   │   ├── sms.py            # Twilio integration for SMS
│   │   └── risk_model.py     # Optional ML risk scoring logic
│   ├── models/               # ORM models (SQLAlchemy or Supabase client)
│   │   ├── user.py
│   │   ├── shelter.py
│   │   ├── help_request.py
│   │   └── case.py
│   ├── templates/            # HTML templates (optional)
│   └── static/               # Static assets (optional)
├── migrations/               # Alembic DB migrations
├── scripts/                  # Scripts for seeding, testing, CLI tools
├── tests/                    # Unit & integration tests
├── .env                      # Environment variables
├── .flaskenv                 # Flask environment settings
├── requirements.txt          # Python dependencies
├── run.py                    # App entry point
└── README.md                 # Project overview
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Supabase account
- Claude API key
- Mapbox access token
- Twilio account (for SMS features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd safelink-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys and configuration
   ```

5. **Initialize database**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile

### AI Assistant
- `POST /ai/chat` - Chat with Claude AI
- `POST /ai/analyze` - Analyze help request
- `GET /ai/suggestions` - Get resource suggestions

### Resources
- `GET /resources/shelters` - List shelters
- `GET /resources/food` - List food banks
- `GET /resources/legal` - List legal aid services
- `POST /resources/search` - Search resources by location

### Alerts
- `POST /alerts/emergency` - Send emergency alert
- `GET /alerts/active` - Get active alerts
- `PUT /alerts/<id>/resolve` - Resolve alert

### Users
- `GET /users/profile` - Get user profile
- `PUT /users/profile` - Update user profile
- `GET /users/volunteers` - List volunteers
- `GET /users/social-workers` - List social workers

### Cases
- `POST /cases/create` - Create help request
- `GET /cases/<id>` - Get case details
- `PUT /cases/<id>` - Update case
- `GET /cases/assigned` - Get assigned cases

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Deployment

### Production Setup

1. Set `FLASK_ENV=production` in environment
2. Configure production database
3. Set up proper logging
4. Use Gunicorn for WSGI server:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

### Docker Deployment

```bash
docker build -t safelink-app .
docker run -p 5000:5000 safelink-app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository. 