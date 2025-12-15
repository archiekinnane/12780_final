# Whither the Weather?

### (Whither means "to what place or state")

This repository contains a Django web application for exploring **local climate change signals** by comparing recent weather metrics against historical baselines. Currently this is done by comparing two metrics to an observed baseline -- days above 90F and days below 32F. For example, how did the number of days over 90F in Atlanta in 2024 compare to the average baseline period of 1990-2020? 

The application allows users to submit queries, submit observed data, visualize results through an interactive dashboard, and export the dataset for further analysis.

The project is containerized with Docker and includes automated testing and continuous integration to ensure portability and reproducibility.

---

## Project Overview

The application is built around two core workflows:

1. **Query Definition**  
   Users submit queries that define which climate signal should be analyzed (location, metric, target year, and baseline period). In the current version, submitting a query stores it but does not automatically compute results, but future versions could with Open-Meteo API implementation. The database is seeded with 10 years of data for the 15 largest cities in the US.

2. **Data Submission & Analysis**  
   Users submit observed data (target value and baseline average). The application automatically computes the change relative to baseline and marks the query as **Completed**.

A central dashboard aggregates all queries and results, presenting summaries and charts that highlight local climate trends.

---

## Key Features

- Django web application with admin interface
- Two core models: `Location` and `WeatherQuery`
- Forms for query submission and data submission
- Interactive dashboard 
- Full dataset preview and Excel (xlsx) export
- Dockerized for portability
- Automated testing with `pytest` and `pytest-django`
- GitHub Actions pipeline (tests + Docker build)

---

## Application Pages / Endpoints

- `/` — Home page 
- `/dashboard/` — Main dashboard
- `/submit/` — Submit a new climate query (stored but not yet completed)  
- `/submit-data/` — Submit observed data and compute results  
- `/export/` — View the full dataset and download as Excel  
- `/admin/` — Django admin interface  

---

## Styling

- The application uses the NES.css framework for a retro, 8-bit inspired visual style, applied via a global stylesheet.
- NES.css project: https://github.com/nostalgic-css/NES.css

---

## Project Structure
```
└── 12780_final/
    ├── .gitignore
    ├── Dockerfile
    ├── pytest.ini
    ├── README.md
    ├── requirements.txt
    ├── weather_tracker/
    │   ├── db.sqlite3
    │   ├── load_demo_once.py
    │   ├── manage.py
    │   ├── weather - Shortcut.lnk
    │   ├── weather_tracker/
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── wsgi.py
    │   │   ├── __init__.py
    │   │   └── __pycache__/
    │   │       ├── settings.cpython-312.pyc
    │   │       ├── urls.cpython-312.pyc
    │   │       ├── wsgi.cpython-312.pyc
    │   │       └── __init__.cpython-312.pyc
    │   ├── weather/
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── forms.py
    │   │   ├── models.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   ├── views.py
    │   │   ├── __init__.py
    │   │   ├── tests/
    │   │   │   ├── test_app.py
    │   │   ├── static/
    │   │   │   ├── app.js
    │   │   │   ├── styles.css
    │   │   │   └── weather/
    │   │   │       └── dashboard.js
    │   │   ├── services/
    │   │   │   └── open-meteo.py
    │   │   ├── seed/
    │   │   │   └── demo_weather_data_v3.csv
    │   │   └── migrations/
    │   │       ├── 0001_initial.py
    │   │       ├── 0002_seed_demo_data_v3.py
    │   │       ├── __init__.py
    │   ├── templates/
    │   │   ├── home.html
    │   │   └── weather/
    │   │       ├── dashboard.html
    │   │       ├── export.html
    │   │       ├── submit.html
    │   │       ├── submit_data.html
    │   │       └── submit_success.html
    │   └── .devcontainer/
    │       └── devcontainer.json
```
## Database Model

### Location
- name
- latitude
- longitude

### WeatherQuery
- location (foreign key)
- metric
- target_year
- baseline_start_year
- baseline_end_year
- target_value
- baseline_avg_value
- delta_value
- status

## Running with Docker

### Clone Repository
git clone https://github.com/archiekinnane/12780_final.git  
cd 12780_final

### Build Image
docker build -t 12780_final .

### Run Container
docker run -p 8000:8000 12780_final

## Running Locally
pip install -r requirements.txt  
cd weather_tracker  
python manage.py migrate  
python manage.py runserver  

## Data Export
- Endpoint: /export/
- Displays full dataset
- Allows download as .xlsx

## Testing
- Framework: pytest, pytest-django
- Run with: pytest -q

## Continuous Integration
- GitHub Actions runs tests on every push
- Docker image builds only if tests pass

## Versioning
- Final graded version tagged as GitHub Release (e.g. v1.0.0)