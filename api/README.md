# FastAPI Project

A modern API project built with FastAPI, featuring a complete setup for building production-ready APIs.

## Features

- RESTful API endpoints with automatic OpenAPI documentation
- Request validation using Pydantic models
- Database integration with SQLAlchemy ORM
- JWT authentication system
- CORS middleware for frontend integration
- Environment variable configuration
- Error handling with appropriate HTTP status codes

## Project Structure

```
api/
├── app/
│   ├── core/          # Core functionality (config, security)
│   ├── crud/          # CRUD operations
│   ├── db/            # Database models and session
│   ├── models/        # SQLAlchemy models
│   ├── routers/       # API routes
│   └── schemas/       # Pydantic schemas
├── main.py            # Application entry point
├── requirements.txt   # Dependencies
└── .env               # Environment variables
```

## Getting Started

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API server:

```bash
python main.py
```

3. Access the API documentation:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

- **Authentication**: `/api/login/access-token`
- **Users**: `/api/users/`
- **Items**: `/api/items/`
- **Health Check**: `/api/health`

## Development

The API server includes auto-reload functionality, so changes to the code will automatically restart the server.