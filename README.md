# Webhook Delivery Service

A robust webhook delivery service built with FastAPI and React, featuring reliable delivery, retries, and comprehensive logging.

## Features

- **Subscription Management**: Create and manage webhook subscriptions with target URLs
- **Secure Delivery**: HMAC signature verification for payload authenticity
- **Event Type Filtering**: Subscribe to specific event types
- **Reliable Delivery**: Automatic retries with exponential backoff
- **Comprehensive Logging**: Track all delivery attempts and their outcomes
- **Real-time Status**: Monitor webhook delivery status and history
- **Performance Optimized**: Redis caching and efficient database queries
- **Horizontally Scalable**: Designed for high availability and throughput

## Tech Stack

### Backend
- **Framework**: FastAPI - Chosen for:
  - High performance with async support
  - Automatic OpenAPI documentation
  - Type safety with Pydantic
  - Built-in dependency injection
- **Database**: PostgreSQL
  - ACID compliance for reliable tracking
  - JSON support for flexible payloads
  - Array type for event filtering
  - Efficient indexing for logs
- **Cache/Queue**: Redis
  - Fast in-memory caching
  - Reliable message broker
- **Task Queue**: Celery
  - Robust background processing
  - Automatic retries
  - Task monitoring

### Frontend
- React 18 with TypeScript
- TanStack Router for type-safe routing
- TanStack Query for data fetching
- Tailwind CSS for styling
- Lucide React for icons

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/webhook-service.git
cd webhook-service
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start services:
```bash
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## API Documentation

### Example API Usage

1. Create a subscription:
```bash
curl -X POST http://localhost:8000/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Order Updates",
    "target_url": "https://example.com/webhooks",
    "secret_key": "your-secret-key",
    "event_types": ["order.created", "order.updated"]
  }'
```

2. Send a webhook:
```bash
curl -X POST http://localhost:8000/api/webhooks/ingest/1 \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=computed-signature" \
  -H "X-Event-Type: order.created" \
  -d '{"order_id": "123", "status": "paid"}'
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

- Connection pooling for database
- Redis caching for frequently accessed data
- Async task processing with Celery
- Database indexing strategy:
  - Composite index on (subscription_id, created_at)
  - Index on webhook_id for status lookups
  - Partial index on status for active retries

## Cost Estimation

### Free Tier Resources (Render)
- Web Service (Frontend): $0/month
- Web Service (Backend): $0/month
- PostgreSQL: $0/month (Shared instance)
- Redis: $0/month (Shared instance)

### Production Estimates (5000 webhooks/day)
Based on 5000 webhooks/day with 1.2 average delivery attempts:
- Compute: $25-50/month
- Database: $50/month (Dedicated PostgreSQL)
- Redis: $15/month
- Network: $10/month
- **Total**: $100-125/month

## Security

- HMAC signature verification
- Rate limiting
- Input validation
- CORS configuration
- Environment variable management
- Database connection pooling
- Secure headers

## Testing

```bash
# Run backend tests
docker-compose exec api pytest

# Run frontend tests
npm test
```

## Deployment

The service is deployed on Render:
- **Frontend**: [https://webhook-frontend-e85x.onrender.com]
- **Backend**: [https://webhook-backend-88w7.onrender.com]
- **API Docs**: [https://webhook-backend-88w7.onrender.com/docs]

## Architecture

The service uses a microservices architecture with:
- Frontend SPA for management
- FastAPI backend for API endpoints
- PostgreSQL for persistent storage
- Redis for caching and queuing
- Celery workers for async processing

Database Schema:
```sql
-- Subscriptions
CREATE TABLE subscription (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    target_url VARCHAR NOT NULL,
    secret_key VARCHAR,
    event_types TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Delivery Logs
CREATE TABLE delivery_log (
    id SERIAL PRIMARY KEY,
    webhook_id VARCHAR NOT NULL,
    subscription_id INTEGER REFERENCES subscription(id),
    attempt_number INTEGER,
    status VARCHAR,
    status_code INTEGER,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    next_retry_at TIMESTAMPTZ
);
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://reactjs.org/)
- [TanStack](https://tanstack.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Celery](https://docs.celeryq.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Docker](https://www.docker.com/)