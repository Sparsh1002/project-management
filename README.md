# Jira-like Project Management Backend

A production-style backend system inspired by Jira, built using FastAPI, PostgreSQL, SQLAlchemy, WebSockets, and Docker.

This project supports:

* Authentication & Authorization
* Projects & Sprints
* Issues / Epics / Stories / Subtasks
* Workflow Transitions
* Activity Logs
* Notifications
* Watchers
* Comments & Threaded Comments
* Full-text Search
* Realtime WebSocket Events
* Optimistic Locking
* Seed Data
* Dockerized Deployment

---

# Tech Stack

| Technology | Purpose               |
| ---------- | --------------------- |
| FastAPI    | Backend API framework |
| PostgreSQL | Relational database   |
| SQLAlchemy | ORM                   |
| Alembic    | Database migrations   |
| JWT        | Authentication        |
| WebSockets | Realtime updates      |
| Docker     | Containerization      |
| Vercel     | Deployment            |

---

# Features

## Authentication

* User registration
* User login
* JWT access tokens
* Password hashing
* Authentication middleware
* Protected routes

---

## Projects

* Create projects
* Project-specific issue keys
* Sprint management per project
* Board state API
* Activity feed API

---

## Issues

Supports:

* Epic
* Story
* Task
* Bug
* Sub-task

Features:

* Create issue
* Update issue fields
* Workflow transitions
* Parent-child hierarchy
* Assignee & reporter support
* Story points
* Labels
* Optimistic locking
* Activity logging

---

## Workflow Engine

Supported workflow:

```txt
To Do
   ↓
In Progress
   ↓
In Review
   ↓
Done
```

Features:

* Transition validation
* Workflow rules
* Validation hooks
* Automatic workflow actions
* Version conflict handling

---

## Sprints

* Create sprint
* Start sprint
* Complete sprint
* Move issue to sprint
* Sprint velocity tracking
* Carry-over issue support
* Date range support

---

## Comments

* Add comments
* Threaded comments
* Fetch issue comments
* Mention parsing (`@username`)

---

## Notifications

Notifications generated for:

* Mentions
* Assignments
* Workflow events

Features:

* Fetch notifications
* Mark notifications as read

---

## Watchers

* Watch issues
* Unwatch issues
* Track subscribed users

---

## Search

Supports:

* Full-text issue search
* Search in titles
* Search in descriptions
* Search in comments
* Structured filtering
* Pagination

Filters:

* status
* priority
* assignee

---

## Realtime Features

WebSocket-based realtime updates:

* issue_created
* issue_transitioned
* comment_added
* sprint_updated

---

# Folder Structure

```txt
app/
├── api/
│   └── routes/
│       ├── auth.py
│       ├── comments.py
│       ├── issues.py
│       ├── notifications.py
│       ├── projects.py
│       ├── search.py
│       ├── sprints.py
│       └── watchers.py
│
├── db/
│   ├── database.py
│   └── seed.py
│
├── middleware/
│   └── auth_middleware.py
│
├── models/
│   ├── activity_log.py
│   ├── comment.py
│   ├── issue.py
│   ├── notification.py
│   ├── project.py
│   ├── sprint.py
│   ├── user.py
│   └── watcher.py
│
├── schemas/
│   ├── auth.py
│   ├── comment.py
│   ├── issue.py
│   ├── project.py
│   ├── search.py
│   └── sprint.py
│
├── utils/
│   ├── mentions.py
│   └── security.py
│
├── websocket/
│   └── manager.py
│
└── main.py
```

---

# Database Design

## Core Relationships

```txt
Project
   ├── Sprints
   └── Issues

Issue
   ├── Comments
   ├── Activity Logs
   ├── Watchers
   ├── Reporter(User)
   ├── Assignee(User)
   └── Parent Issue
```

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd project
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env`

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/jira_db
SECRET_KEY=swiggy
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# Database Setup

## Run Migrations

```bash
alembic upgrade head
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

Application:

```txt
http://localhost:8000
```

Swagger Docs:

```txt
http://localhost:8000/docs
```

---

# Docker Setup

## Start Containers

```bash
docker-compose up --build
```

Starts:

* FastAPI backend
* PostgreSQL database

---

# Seed Data

Seed data automatically runs on startup.

Includes:

* Users
* Projects
* Sprints
* Issues
* Comments
* Notifications
* Watchers
* Activity logs

The demo data is based on a Swiggy delivery management domain.

---

# API Endpoints

# Authentication

| Method | Endpoint         |
| ------ | ---------------- |
| POST   | `/auth/register` |
| POST   | `/auth/login`    |

---

# Projects

| Method | Endpoint                  |
| ------ | ------------------------- |
| POST   | `/projects`               |
| GET    | `/projects`               |
| GET    | `/projects/{id}/board`    |
| GET    | `/projects/{id}/activity` |
| GET    | `/projects/{id}/sprints`  |

---

# Issues

| Method | Endpoint                         |
| ------ | -------------------------------- |
| POST   | `/issues/{project_id}`           |
| PATCH  | `/issues/{issue_id}`             |
| POST   | `/issues/{issue_id}/transitions` |

---

# Comments

| Method | Endpoint                      |
| ------ | ----------------------------- |
| GET    | `/issues/{issue_id}/comments` |
| POST   | `/issues/{issue_id}/comments` |

---

# Sprints

| Method | Endpoint                                 |
| ------ | ---------------------------------------- |
| POST   | `/sprints`                               |
| POST   | `/sprints/{id}/start`                    |
| POST   | `/sprints/{id}/complete`                 |
| POST   | `/sprints/{sprint_id}/issues/{issue_id}` |

---

# Search

| Method | Endpoint  |
| ------ | --------- |
| GET    | `/search` |

Example:

```txt
/search?q=delivery&status=In Progress
```

---

# Watchers

| Method | Endpoint             |
| ------ | -------------------- |
| POST   | `/issues/{id}/watch` |
| DELETE | `/issues/{id}/watch` |

---

# Notifications

| Method | Endpoint                   |
| ------ | -------------------------- |
| GET    | `/notifications`           |
| PATCH  | `/notifications/{id}/read` |

---

# WebSocket

| Endpoint |
| -------- |
| `/ws`    |

---

# Optimistic Locking

The system uses version-based optimistic locking to prevent concurrent update conflicts.

Example:

```json
{
  "version": 3
}
```

If another user updates the issue first:

```txt
409 Conflict
```

is returned.

---

# Workflow Validation Example

Allowed transitions:

```txt
To Do -> In Progress
In Progress -> In Review
In Review -> Done
```

Invalid transitions return:

```json
{
  "detail": "Allowed transitions: ['In Progress']"
}
```

---

# Realtime Event Examples

```json
{
  "event": "issue_created",
  "data": {
    "issue_id": 1
  }
}
```

```env
DATABASE_URL=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```

# Notes

This project was intentionally designed with:

* clean architecture
* modular structure
* production-style APIs
* scalable design principles
* clear separation of concerns

while still keeping the implementation beginner-friendly and easy to understand.
