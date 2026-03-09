WebScrapp – Django Web Scraping Job Queue System
📌 Project Overview
  WebScrapp is a Django-based web scraping job management system that allows users to submit URLs for scraping.
  The system manages scraping tasks using a priority-based job queue and executes them asynchronously through background scripts.
  Users can register, log in, create scraping jobs, and view extracted links once the scraping process is completed.
  The application is containerized using Docker and PostgreSQL, making it scalable and production-ready.

🚀 Key Features

1. User Authentication
  (i). User registration with email validation
  (ii). Password validation with strong regex rules
  (iii). Secure login/logout using Django authentication
  (iv). Session-based authentication

2. Subscription-Based Job Priority
Users can subscribe to different plans:
| Plan  | Priority |
| ----- | -------- |
| PRO   | Highest  |
| BASIC | Medium   |
| FREE  | Lowest   |

Higher subscription users get faster job execution in the queue.

3. Job Creation System
Authenticated users can create scraping jobs by submitting:
  (i). Target URL
  (ii) Job Status
  (iii) Each job is stored with:
      a. User
      b. URL
      c. Priority
      d. Status
  (iv) Jobs are processed according to priority order.

4. Background Job Queue

The system runs a background job processor that:
  (i) Checks for new jobs
  (ii) Selects the highest priority job
  (iii) Launches a scraping process
  (iv)  Updates job status

This is implemented using:
  (i) django-extensions runscript
  (ii) Python subprocess
  (iii) Async scraping

5. Async Web Scraping Engine
The scraping process:
  (i) Receives the job ID
  (ii) Runs an async scraping engine
  (iii) Extracts valid links
  (iv) Saves them to the database

6. Scraped Links Viewer
  Users can view extracted links after the scraping job is completed.
  Only links with status code 200 are shown.

🏗 System Architecture
User
  │
  ▼
Django Web App
  │
  ├── Authentication
  ├── Job Creation
  └── Subscription System
  │
  ▼
PostgreSQL Database
  │
  ▼
Job Queue Processor
(run.py script)
  │
  ▼
Scraping Worker
(scrap.py)
  │
  ▼
Async Scraper Engine
(ScrapPage)
  │
  ▼
Links Stored in Database


🐳 Docker Architecture
The project runs using Docker Compose with multiple services:
| Service       | Description                |
| ------------- | -------------------------- |
| `scrap_api`   | Django application server  |
| `scrap_links` | Background scraping worker |
| `db`          | PostgreSQL database        |
| `pgadmin`     | PostgreSQL UI management   |

🛠 Technology Stack
Backend:
  Python
  Django
  Django Authentication
  Asyncio

Database:
  PostgreSQL

Containerization:
  Docker
  Docker Compose

Background Processing:
  Django Extensions
  Python Subprocess
