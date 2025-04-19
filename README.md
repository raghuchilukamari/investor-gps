# Investor GPS 🧭

A comprehensive financial analytics platform that provides macroeconomic insights, sentiment analysis, and market reaction tracking.

## 🌟 Features

- **Macrometer Dashboard**: Real-time macroeconomic indicators with sentiment signals
- **Sentiment Scanner**: Social media and news sentiment analysis
- **Market Reaction Tracker**: Asset class response analysis
- **Earnings Sentiment**: AI-powered earnings call transcript analysis
- **Admin Panel**: Content management and signal override capabilities

## 🏗️ Tech Stack

### Frontend
- Next.js 14 with TypeScript
- Tailwind CSS for styling
- Recharts for data visualization
- React Query for data fetching
- Zustand for state management

### Backend
- FastAPI (Python)
- PostgreSQL for data storage
- SQLAlchemy for ORM
- Pydantic for data validation
- TextBlob/VADER for sentiment analysis
- Celery for background tasks

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.9+
- PostgreSQL 14+
- Docker (optional)

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/investor-gps.git
cd investor-gps
```

2. Frontend Setup:
```bash
cd frontend
npm install
# Create .env file
cp .env.example .env  # If .env.example exists
# Start the development server
npm run dev
```

3. Backend Setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
# Create .env file
cp .env.example .env  # If .env.example exists
# Start the development server
uvicorn main:app --reload
```

4. Database Setup:
```bash
# Create PostgreSQL database
createdb investor_gps
# Run migrations
cd backend
alembic upgrade head
```

### Environment Variables

Create `.env` files in both frontend and backend directories:

Frontend (.env):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Backend (.env):
```
DATABASE_URL=postgresql://user:password@localhost:5432/investor_gps
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
FRED_API_KEY=your_fred_api_key
```

### Troubleshooting

1. Port Conflicts:
   - If port 3000 is in use for frontend: `npm run dev -- -p 3001`
   - If port 8000 is in use for backend: `uvicorn main:app --reload --port 8001`

2. Database Connection Issues:
   - Ensure PostgreSQL is running: `sudo service postgresql status`
   - Check database credentials in .env file
   - Verify database exists: `psql -l | grep investor_gps`

3. Frontend Build Issues:
   - Clear Next.js cache: `rm -rf frontend/.next`
   - Reinstall dependencies: `cd frontend && rm -rf node_modules && npm install`

4. Backend Issues:
   - Activate virtual environment: `source backend/venv/bin/activate`
   - Update dependencies: `pip install -r requirements.txt`
   - Check logs: `tail -f backend/logs/app.log`

## 📁 Project Structure

```
investor-gps/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── store/          # Zustand store
│   │   └── types/          # TypeScript types
│   ├── public/             # Static assets
│   └── package.json        # Frontend dependencies
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── models/        # Database models
│   │   └── services/      # Business logic
│   ├── alembic/           # Database migrations
│   └── requirements.txt    # Backend dependencies
└── README.md              # Project documentation
```

## 📈 Roadmap

- [ ] User authentication and authorization
- [ ] Personalized dashboards
- [ ] Real-time data updates
- [ ] Advanced sentiment analysis
- [ ] Mobile app version
- [ ] API rate limiting and caching
- [ ] Automated deployment pipeline

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 