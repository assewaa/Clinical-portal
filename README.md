# Clinical Systems Portal

A lightweight Django portal providing a central welcome page for independent clinical applications.

The portal is intentionally independent from the clinical applications themselves. It does not use their databases, authentication systems, or Django application code.

## Current Applications

The portal currently provides links to:

- Neurology Emergency Department
- Breast Cancer Registry
- Radiology

Applications are defined in:

    portal/projects.py

Future applications can be added to the central registry without redesigning the portal.

## Project Structure

    Clinical-portal/
    ├── config/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── portal/
    │   ├── __init__.py
    │   ├── projects.py
    │   ├── views.py
    │   ├── templates/
    │   │   └── portal/
    │   │       └── home.html
    │   └── static/
    │       └── portal/
    │           └── images/
    ├── manage.py
    ├── requirements.txt
    ├── .env.example
    └── .gitignore

## Local Setup

Create a virtual environment:

    python3 -m venv .venv

Activate it:

    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

For local development:

    export DJANGO_DEBUG=true
    export DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

Run Django checks:

    python manage.py check

Start the development server:

    python manage.py runserver 127.0.0.1:8000

Open:

    http://127.0.0.1:8000/

## Static Files

For deployment, collect static files with:

    python manage.py collectstatic --noinput

Static files are collected into:

    staticfiles/

The generated staticfiles/ directory is excluded from Git.

## Configuration

Environment variables are documented in:

    .env.example

Important settings include:

- DJANGO_SECRET_KEY
- DJANGO_DEBUG
- DJANGO_ALLOWED_HOSTS
- PORTAL_ENABLED_PROJECTS
- NEUROLOGY_URL
- BREAST_REGISTRY_URL
- RADIOLOGY_URL

The portal reads these values from its process environment. For a systemd
deployment, configure them in the service's EnvironmentFile.

Do not commit production secrets or a real environment file.

### Choosing which applications appear

Set PORTAL_ENABLED_PROJECTS to a comma-separated list of application keys:

    PORTAL_ENABLED_PROJECTS=neurology,radiology

Available keys:

- neurology
- breast-registry
- radiology

If PORTAL_ENABLED_PROJECTS is omitted, all registered applications appear.

### Configuring application addresses

Each application URL can be configured independently.

For applications served on the same HTTPS domain as the portal, use a
relative path, for example:

    NEUROLOGY_URL=/neurology/accounts/login/

For applications hosted on another server, use its complete HTTPS address,
for example:

    NEUROLOGY_URL=https://neurology.example.com/login/

The portal does not proxy application traffic or manage remote application
authentication. The user's browser opens the configured destination directly.

## Architecture

The Clinical Systems Portal is a presentation and routing layer only.

Each clinical application remains an independent project with its own:

- Django application
- database
- authentication
- deployment
- security configuration

The portal does not require the clinical applications to be installed in the same Django project.

A VPS can therefore host:

- all clinical applications,
- only selected applications,
- or the portal with applications hosted on other servers.

Application URLs are configured in:

    portal/projects.py

The portal can be extended with additional applications without redesigning the welcome page.
