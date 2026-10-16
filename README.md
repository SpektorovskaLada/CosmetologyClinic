Cosmetology Clinic Management System
A web application for a cosmetology clinic, built with Django and PostgreSQL. It combines a public-facing clinic website with database-backed content management and an administrative analytics dashboard.
Features
- Clinic website: homepage, specialist information, cosmetology service pages, and a product catalogue.
- Database-backed content: services, service categories, products, product categories, specialists, clients, appointments, callback requests, and reviews are accessed through Django models.
- Review submission: the application checks that a client exists and has a completed appointment before creating a review.
- Administration: Django Admin is configured to manage clinic records, including clients, specialists, services, products, appointments, reviews, callback requests, and used products.
- Analytics dashboard: charts summarise completed appointments, monthly income, popular services and categories, client visit frequency by gender and age group.
- Time-series forecasting: SARIMAX/SARIMA models are used to forecast appointment counts and income when enough historical monthly data is available.
Technology Stack
- Python
- Django
- PostgreSQL
- Django ORM
- HTML and Django Templates
- CSS and JavaScript
- Chart.js for dashboard charts
- pandas and statsmodels for time-series analysis
How It Works
The Django project is located in backend/.
1. A browser requests a page through a URL configured in backend/config/urls.py.
2. Django routes the request to a view in backend/main/views.py.
3. Views query or update PostgreSQL through Django's ORM and the models in backend/main/models.py.
4. The view passes the resulting data to a Django template in backend/main/templates/.
5. The template renders the page and loads static CSS, JavaScript, and images from backend/main/static/.
The application uses an existing PostgreSQL schema. The clinic models in main/models.py are marked managed = False, so Django migrations do not create or manage those application tables. The database schema must be created separately, for example by restoring the SQL dump maintained in the companion database repository. Django migrations are still needed for Django's own framework tables.
Analytics
The dashboard is restricted to authenticated staff users. It uses Django ORM queries to aggregate completed appointments and related data from PostgreSQL. pandas prepares monthly time series, and SARIMAX models generate forecasts when at least 24 monthly observations are available. Chart data is passed from Django to the template and visualised in the browser.
Project Structure
Diploma/
├── backend/
│   ├── config/                 # Django project settings and URL routing
│   ├── main/
│   │   ├── migrations/         # Django migration package
│   │   ├── models.py           # ORM mappings to database tables
│   │   ├── views.py             # Page logic, database queries, analytics
│   │   ├── admin.py             # Django Admin configuration
│   │   ├── templates/           # Django HTML templates
│   │   └── static/              # CSS, JavaScript, and images
│   ├── manage.py
│   ├── requirements.txt
│   ├── prepare_clients.py       # Client-data preparation script
│   ├── generate_records.py      # Record-generation script
│   └── sarima_analysis.ipynb    # Time-series analysis notebook
├── index.html                   # Legacy static-site version
├── partials/                    # Legacy static HTML fragments
├── scripts/                     # Legacy JavaScript files
└── stylecss/                    # Legacy CSS files
The top-level index.html, partials/, scripts/, and stylecss/ appear to belong to an earlier static version. The Django application is configured to use templates and static assets under backend/main/; the top-level legacy files are not part of the configured Django template/static directories.
Setup
Requirements
- Python compatible with the installed Django version
- PostgreSQL
- The database schema and any required reference data
1. Create and activate a virtual environment
From the project directory:
cd backend
python -m venv venv
On Windows:
venv\Scripts\activate
2. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
The dashboard imports statsmodels, so make sure statsmodels is included in requirements.txt before setting up the project from a clean environment.
3. Configure PostgreSQL
Create the PostgreSQL database and restore the schema using the SQL dump from the companion database repository. Configure the database name, username, password, host, and port for your local PostgreSQL instance in the Django settings. Do not commit real passwords or secret keys to version control; use environment variables or a local, untracked settings file for secrets.
4. Apply Django migrations
python manage.py migrate
This applies Django's framework migrations. It does not create the clinic application tables because those models are marked managed = False.
5. Create an administrator account
python manage.py createsuperuser
6. Run the development server
python manage.py runserver
Open http://127.0.0.1:8000/ in your browser. The Django administration interface is available at http://127.0.0.1:8000/admin/.
Important Notes
- This repository contains the Django application code; the PostgreSQL schema is maintained separately.
- The analytics dashboard requires sufficient historical appointment data to produce forecasts.
- Review submission depends on an existing client record and a completed appointment.
- The included venv/ directory is a local environment and should not be committed. Install dependencies from requirements.txt instead.
- Before publishing or deploying the project, move credentials and Django's secret key out of source code, restrict ALLOWED_HOSTS, and disable debug mode for production.
