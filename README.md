# Webhook Delivery Service

A robust webhook delivery service built with FastAPI and React, featuring reliable delivery, retries, and comprehensive logging.

## Features

- **Subscription Management**: CRUD operations for webhook subscriptions
- **Webhook Ingestion**: Fast acknowledgment and async processing
- **Reliable Delivery**: Automatic retries with exponential backoff
- **Comprehensive Logging**: Track all delivery attempts and their outcomes
- **Security**: Payload signature verification
- **Event Type Filtering**: Subscribe to specific event types
- **Performance Optimized**: Redis caching and efficient queuing
- **Modern UI**: React-based dashboard for management and monitoring

## Tech Stack

### Backend
- FastAPI (API framework)
- PostgreSQL (primary database)
- Redis (caching and queuing)
- Celery (background tasks)
- SQLAlchemy (ORM)

### Frontend
- React
- TanStack Router
- TanStack Query
- Tailwind CSS
- Axios

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+
- Python 3.9+

### Local Development Setup

1. Start the infrastructure:
   ```bash
   docker-compose up -d
   ```

2. Install backend dependencies:
   ```bash
   cd api
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   npm install
   ```

4. Start the development servers:
   ```bash
   # Terminal 1: Frontend
   npm run dev

   # Terminal 2: Backend
   npm run api

   # Terminal 3: Celery Worker
   npm run worker
   ```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example API Usage

1. Create a subscription:
```bash
curl -X POST http://localhost:8000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Webhook",
    "target_url": "https://example.com/webhook",
    "secret_key": "your-secret",
    "event_types": ["order.created", "user.updated"]
  }'
```

2. Send a webhook:
```bash
curl -X POST http://localhost:8000/api/webhooks/ingest/1 \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=computed-signature" \
  -H "X-Event-Type: order.created" \
  -d '{"event": "order.created", "data": {"id": 123}}'
```

3. Check webhook status:
```bash
curl http://localhost:8000/api/webhooks/status/webhook-id
```

4. Get subscription logs:
```bash
curl http://localhost:8000/api/webhooks/subscription/1/logs
```

## Performance Considerations

- Redis caching for subscription details
- Async task processing with Celery
- Efficient database queries with proper indexing
- Connection pooling for database and Redis

## Cost Estimation

### Free Tier Resources
- Heroku Hobby Dyno: $0/month
- Heroku Postgres Hobby: $0/month
- Heroku Redis Hobby: $0/month

### Production Estimates (5000 webhooks/day)
- Application Hosting: $25-50/month
- Database: $50/month
- Redis: $15/month
- Total: $90-115/month

## Security

- Payload signature verification
- Rate limiting
- Input validation
- Secure headers
- CORS configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Credits

- FastAPI: https://fastapi.tiangolo.com/
- React: https://reactjs.org/
- TanStack: https://tanstack.com/
- Tailwind CSS: https://tailwindcss.com/
- Celery: https://docs.celeryq.dev/