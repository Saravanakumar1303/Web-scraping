# WebScrap – Django Web Scraping & Website Audit System

WebScrap is a Django-based web scraping system built to handle website scraping as background jobs instead of processing everything inside a normal web request.

The main idea behind this project is simple:

A user submits a website URL → the URL becomes a scraping job → the job is assigned a priority based on the user's subscription → a background worker picks the job → the scraper crawls the website's internal links → basic website and SEO-related information is extracted and stored in PostgreSQL.

I built this project to understand how a backend application can handle long-running tasks, background processing, browser-based scraping, database relationships, and Docker-based development.

---

## Project Overview

Web scraping can become difficult when a website contains many internal pages or when the pages depend on JavaScript to load their content.

Instead of making the user wait for the entire scraping process to finish, WebScrap separates the web application from the scraping process.

The Django application is responsible for:

- User authentication
- Subscription management
- Creating scraping jobs
- Assigning job priorities
- Storing scraping results

A separate background worker is responsible for:

- Picking pending jobs
- Running the scraping process
- Discovering internal links
- Extracting page information
- Saving the results

This separation was one of the main design decisions in the project.

---

## What Problem Does It Solve?

Imagine a user submits:

    https://example.com

The website may contain:

    https://example.com/about
    https://example.com/contact
    https://example.com/products
    https://example.com/blog
    ...

Scraping all these pages inside a normal Django request would keep the request running for a long time.

Instead, WebScrap creates a job and processes it in the background.

The flow becomes:

    User
      ↓
    Submit URL
      ↓
    Create Scraping Job
      ↓
    Assign Priority
      ↓
    Background Worker
      ↓
    Playwright
      ↓
    Extract HTML
      ↓
    BeautifulSoup
      ↓
    Discover Internal Links
      ↓
    Perform Basic Website Audit
      ↓
    Store Results in PostgreSQL

---

# Key Features

## 1. User Authentication

The application provides user authentication using Django's authentication system.

Users can:

- Register an account
- Validate email input
- Validate passwords
- Login
- Logout
- Access their scraping-related data

Authentication is session-based.

---

## 2. Subscription-Based Job Priority

The application supports different subscription levels.

| Plan | Priority |
|------|----------|
| PRO | Highest |
| BASIC | Medium |
| FREE | Lowest |

The subscription level is used to determine the priority of a scraping job.

For example, if the queue contains:

    FREE Job
    PRO Job
    BASIC Job

the worker will process the higher-priority job first.

This helped me understand how business rules can be connected to background job processing.

---

## 3. Scraping Job Management

An authenticated user can create a scraping job by providing a target URL.

Each job stores information such as:

- User
- Target URL
- Priority
- Job status

A job moves through different states during its lifecycle.

    NEW
     ↓
    IN_PROGRESS
     ↓
    COMPLETED

The job status allows the application to keep track of the scraping process.

---

## 4. Background Job Processing

Web scraping can be a long-running operation, so the scraping process is not handled directly inside the normal request-response cycle.

A separate background worker continuously checks for new jobs.

The worker:

1. Checks for pending jobs
2. Selects the job based on priority
3. Starts the scraping process
4. Passes the job ID to the scraping script
5. Allows the scraping process to update the job status

The worker is implemented using:

- Django Extensions `runscript`
- Python subprocess
- Async Python code

This approach helped me understand how background processing can be separated from the main Django application.

---

# Web Scraping Engine

The scraping engine is implemented using **Playwright** and **BeautifulSoup**.

Both tools have different responsibilities.

### Playwright

Playwright is used to load the webpage using a real browser environment.

This is useful for websites where content may depend on JavaScript.

The basic process is:

    URL
     ↓
    Playwright
     ↓
    Chromium
     ↓
    Page Load
     ↓
    HTTP Response + Rendered HTML

The scraper also records the HTTP status code returned by the page.

---

### BeautifulSoup

After Playwright loads the page, the generated HTML is passed to BeautifulSoup.

BeautifulSoup is then used to:

- Find anchor tags
- Extract links
- Find H1 tags
- Find title tags
- Find meta tags
- Find images
- Check image alt attributes

This gives the application structured information from the page.

---

# Internal Link Crawling

The scraper does not blindly follow every URL found on a page.

It focuses on internal links belonging to the target website.

For example, if the target website is:

    https://example.com

links such as:

    https://example.com/about
    https://example.com/contact
    https://example.com/products

can be added to the scraping queue.

External links such as:

    https://google.com
    https://youtube.com

are not treated as part of the same website crawl.

The discovered links are stored in the database and processed later.

---

# Website / SEO Audit

One of the additional features of this project is a basic page-level website audit.

For every scraped page, the application checks several HTML elements.

## H1 Analysis

The scraper checks:

- Whether an H1 tag exists
- Number of H1 tags
- The actual H1 elements found

Example:

    Missing H1 → Yes / No
    H1 Count → 1

This can help identify pages that do not have a clear H1 heading or contain multiple H1 elements.

---

## Title Analysis

The scraper checks:

- Whether a `<title>` tag exists
- Number of title tags
- The title elements found

---

## Meta Description Analysis

The scraper checks whether the page contains a meta description.

For example:

    <meta name="description" content="...">

If a description is not found, the page is marked accordingly.

---

## Image Alt Text Analysis

The scraper also checks image elements.

For example:

    <img src="image.jpg" alt="Product image">

If an image does not have an `alt` attribute or the attribute is empty, it is recorded as a missing-alt issue.

This information can later be used for basic accessibility and SEO analysis.

---

# Database Design

The project uses PostgreSQL as the primary database.

The main relationships are:

    User
      │
      ├── Subscription
      │
      └── Job
            │
            ├── Job Queue
            │
            └── Links
                  │
                  └── Site Audit

### Job

Stores information about a scraping request.

Main fields include:

- User
- URL
- Priority
- Status

### Links

Stores discovered website URLs and their scraping information.

Main fields include:

- Job
- URL
- HTTP status code
- Validity
- Processing status

### SiteAuditModel

Stores the audit information collected from each scraped page.

Examples include:

- Missing H1
- H1 count
- H1 tags
- Missing title
- Title count
- Title tags
- Missing meta description
- Missing image alt attributes

---

# Technology Stack

### Backend

- Python
- Django

### Web Scraping

- Playwright
- BeautifulSoup4
- Asyncio

### Database

- PostgreSQL

### Background Processing

- Django Extensions
- Python subprocess
- Custom background worker

### Containerization

- Docker
- Docker Compose

### Database Management

- pgAdmin

---

# Docker Architecture

The project is containerized using Docker Compose.

The main services are:

    ┌───────────────────────────┐
    │       Docker Compose      │
    ├───────────────────────────┤
    │                           │
    │  Django Application       │
    │                           │
    │  Scraping Worker          │
    │                           │
    │  PostgreSQL               │
    │                           │
    │  pgAdmin                  │
    │                           │
    └───────────────────────────┘

The Django application handles user-facing operations while the scraping worker runs the long-running scraping tasks.

PostgreSQL stores users, jobs, discovered links, and audit information.

---

# Project Structure

The project is organized into separate Django applications and scripts.

    Webscrapp/
    │
    ├── Accounts/
    │   ├── models.py
    │   └── ...
    │
    ├── Scrap_App/
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    │   ├── utils.py
    │   ├── templates/
    │   └── ...
    │
    ├── scripts/
    │   ├── run.py
    │   └── scrap.py
    │
    ├── manage.py
    ├── requirements.txt
    ├── docker-compose.yaml
    └── Dockerfile

---

# How the Scraping Process Works

The complete scraping workflow is:

### Step 1 – User submits a URL

The authenticated user creates a scraping job.

### Step 2 – Job is stored

The job is stored in PostgreSQL with its user, URL, priority and status.

### Step 3 – Background worker checks the queue

The worker continuously looks for new jobs.

### Step 4 – Highest priority job is selected

Jobs are ordered according to their priority.

### Step 5 – Scraping process starts

The selected job ID is passed to the scraping script.

### Step 6 – Playwright loads the webpage

Playwright launches Chromium and loads the target URL.

### Step 7 – HTML is extracted

The rendered page content is collected.

### Step 8 – BeautifulSoup parses the HTML

The scraper extracts:

- Internal links
- H1 tags
- Title tags
- Meta tags
- Images

### Step 9 – New internal links are added

Discovered internal links are stored as pending links.

### Step 10 – Pages are processed

Pending links are processed until the configured scraping limit is reached.

### Step 11 – Audit information is stored

The page-level audit information is saved in PostgreSQL.

### Step 12 – Job is completed

After the scraping process finishes, the job status is updated.

---

# Why I Used Playwright Instead of Only Requests

A simple scraper can use:

    requests + BeautifulSoup

However, some modern websites depend heavily on JavaScript.

In such cases, the initial HTML response may not contain all the content visible in the browser.

I used Playwright because it provides a browser-based environment and can handle pages that require JavaScript execution.

The general approach is:

    Playwright
        ↓
    Render webpage
        ↓
    Get page content
        ↓
    BeautifulSoup
        ↓
    Extract structured data

---

# Why Background Processing Is Important

One of the main things I wanted to understand while building this project was how to handle long-running operations in a backend application.

If scraping was performed directly inside a Django request, the user would have to wait until the scraping process finished.

For example:

    Browser opens
        ↓
    Page loads
        ↓
    Links are discovered
        ↓
    More pages are scraped
        ↓
    Audit is performed
        ↓
    Response is returned

This can take a significant amount of time.

Instead, the application creates a job and processes it separately.

That gives us:

    HTTP Request
         ↓
    Create Job
         ↓
    Return control to application
         ↓
    Background Worker
         ↓
    Scraping

This was an important backend design concept I learned from this project.

---

# Challenges I Worked On

While developing this project, some of the main challenges were:

### 1. Handling long-running scraping operations

Scraping multiple pages should not block the main Django application.

### 2. Processing jobs based on priority

Different subscription plans needed different processing priorities.

### 3. Combining asynchronous scraping with Django

Playwright uses asynchronous APIs, so the scraping workflow had to be integrated carefully with Django's synchronous ORM.

### 4. Crawling internal links

The scraper needed to discover new pages without continuously processing the same URL.

### 5. Storing page-level audit results

The extracted HTML information needed to be converted into structured database records.

### 6. Running the system with Docker

The Django application, PostgreSQL database and background worker needed to work together inside containers.

---

# What I Learned From This Project

This project helped me move beyond basic Django CRUD development.

Some of the main concepts I worked with were:

- Django application architecture
- Relational database design
- Foreign key relationships
- Background job processing
- Priority-based task execution
- Async programming
- Browser automation
- HTML parsing
- Recursive/internal link crawling
- Docker Compose
- PostgreSQL
- Database-driven application workflows
- Handling long-running backend operations

More importantly, I learned that a backend feature is not only about creating an API or database model. The way a long-running task is scheduled, processed, monitored and stored is equally important.

---

# Current Limitations

This project is a learning-focused implementation and there are still areas that can be improved before treating it as a production-grade scraping platform.

Some of the planned improvements are:

- More robust job locking and concurrent job handling
- Retry mechanism for failed scraping jobs
- Better URL normalization
- Handling relative URLs
- Better timeout and network error handling
- More detailed logging
- Better scraping status tracking
- Stronger URL validation and SSRF protection
- Automated tests
- Reusing browser instances instead of launching a browser for every page
- Better monitoring of background workers

These improvements would make the system more reliable for larger workloads.

---

# Future Improvements

The project can be extended with:

- Celery + Redis for distributed task processing
- Multiple scraping workers
- Retry and backoff strategies
- Scheduled website audits
- Crawl history
- Detailed SEO reports
- Export reports as CSV/PDF
- Dashboard with crawl statistics
- Authentication improvements
- Rate limiting
- Robots.txt handling
- Better URL canonicalization
- Monitoring and logging
- Automated CI/CD deployment

---

# Running the Project Locally

## 1. Clone the repository

    git clone https://github.com/Saravanakumar1303/Web-scraping.git

    cd Web-scraping

## 2. Create environment variables

Create a `.env` file and configure the required database and application settings.

Do not commit `.env` to GitHub.

An example configuration can be provided through `.env.example`.

## 3. Build and start the containers

    docker compose up --build

## 4. Run migrations

    docker compose exec web python manage.py migrate

## 5. Create a superuser

    docker compose exec web python manage.py createsuperuser

## 6. Access the application

The application can then be accessed through the configured Django port.

---

# Project Status

The core scraping workflow is implemented, including:

- User authentication
- Subscription-based priorities
- Job creation
- Background processing
- Playwright-based scraping
- Internal link extraction
- Basic website auditing
- PostgreSQL storage
- Docker-based setup

The project is still open for improvements around reliability, concurrency, security, testing and production-level task management.

---

# Author

**Saravanakumar V**

Python / Django Developer

GitHub:  
https://github.com/Saravanakumar1303

LinkedIn:  
https://www.linkedin.com/in/saravanakumar-varadarajan/
