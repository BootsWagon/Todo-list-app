# Todo List Application

A full-stack Todo List application built with Vue 3, Element Plus, Django, and Docker.

## Features

- Create, read, update, and delete tasks
- Mark tasks as completed
- Responsive design with Element Plus UI
- RESTful API backend
- PostgreSQL database
- Docker containerization

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:
```bash
git clone <repository-url>
cd todo-list
```

2. Build and start the containers:
```bash
docker-compose up --build
```

3. Access the application:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000/api/tasks/
- Django Admin: http://localhost:8000/admin/

## Development

The application is containerized using Docker Compose with three services:
- Frontend (Vue 3 + Element Plus)
- Backend (Django + DRF)
- Database (PostgreSQL)

### Project Structure

```
.
├── frontend/           # Vue 3 frontend
│   ├── src/
│   │   ├── components/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── Dockerfile
├── backend/           # Django backend
│   ├── todo/
│   ├── tasks/
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
```

## API Endpoints

- GET /api/tasks/ - List all tasks
- POST /api/tasks/ - Create a new task
- GET /api/tasks/{id}/ - Retrieve a specific task
- PUT /api/tasks/{id}/ - Update a task
- DELETE /api/tasks/{id}/ - Delete a task 