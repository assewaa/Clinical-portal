# Clinical Systems Portal — Deployment Guide

This guide describes deployment on Ubuntu using Django, Gunicorn, systemd
and Nginx.

The portal is independent of the clinical applications it links to.

## 1. Requirements

- Ubuntu server
- Python 3 with venv support
- Nginx
- Git access to this repository
- HTTPS for browser-facing access

The example configuration uses:

- Linux account: ubuntu
- Project: /home/ubuntu/Documents/Clinical-portal
- Gunicorn: 127.0.0.1:8002
- Environment file: /etc/clinical-portal.env
- Static files: /home/ubuntu/Documents/Clinical-portal/staticfiles/

Change these paths and values when deploying elsewhere.

## 2. Install the project

Clone the repository into the chosen project directory.

Then run:

    cd /home/ubuntu/Documents/Clinical-portal
    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt

## 3. Configure the environment

Create /etc/clinical-portal.env using .env.example as a reference.

Configure these variables:

- DJANGO_SECRET_KEY: a unique, strong production secret
- DJANGO_DEBUG=false
- DJANGO_ALLOWED_HOSTS: the actual server hostnames and addresses
- PORTAL_ENABLED_PROJECTS: application cards to display
- NEUROLOGY_URL
- BREAST_REGISTRY_URL
- RADIOLOGY_URL

Example:

    DJANGO_DEBUG=false
    DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,portal.example.com
    PORTAL_ENABLED_PROJECTS=neurology,breast-registry,radiology
    NEUROLOGY_URL=/neurology/accounts/login/
    BREAST_REGISTRY_URL=/login/?next=/app/
    RADIOLOGY_URL=/radiology/
    DJANGO_SECRET_KEY=replace-with-a-unique-secret

Replace the example secret and hostnames before deployment.

Protect the environment file:

    sudo chown root:root /etc/clinical-portal.env
    sudo chmod 600 /etc/clinical-portal.env

Never commit the production environment file or its secret key.

## 4. Prepare Django

From the project directory:

    .venv/bin/python manage.py check
    .venv/bin/python manage.py collectstatic --noinput

## 5. Install the systemd service

The service template is:

    deploy/systemd/clinical-portal.service

Install it:

    sudo install -o root -g root -m 644 deploy/systemd/clinical-portal.service /etc/systemd/system/clinical-portal.service
    sudo systemctl daemon-reload
    sudo systemctl enable --now clinical-portal.service
    sudo systemctl status clinical-portal.service --no-pager

Gunicorn listens on 127.0.0.1:8002 and should not be exposed directly
to the public internet.

If your Linux account or project directory differs, adjust the service
template before installing it.

## 6. Configure Nginx

The reusable Nginx locations are in:

    deploy/nginx/portal-locations.conf

Install the snippet:

    sudo install -d /etc/nginx/snippets
    sudo install -o root -g root -m 644 deploy/nginx/portal-locations.conf /etc/nginx/snippets/clinical-portal-locations.conf

Inside each intended Nginx server block serving the portal, add:

    include /etc/nginx/snippets/clinical-portal-locations.conf;

Use it in:
- The portal's LAN HTTPS server block.
- The Tailscale hostname server block, if Tailscale Serve terminates HTTPS
  and forwards requests to local Nginx over HTTP.

Do not include it in unrelated application server blocks, including a
separate Neurology-only HTTPS endpoint.

Preserve existing application routes, proxy settings, static files and
media locations. The exact homepage route takes precedence over the
existing catch-all location.

The static alias assumes the project is installed at the path shown above.
Adjust it if the project directory is different.

Validate before reloading:

    sudo nginx -t
    sudo systemctl reload nginx

## 7. Verify deployment

Check the services:

    sudo systemctl is-active clinical-portal.service
    sudo systemctl is-active nginx

Check the local portal response:

    curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8002/

Then test the HTTPS homepage and static files through the browser-facing
Nginx endpoint.

Test every linked clinical application separately. An unauthenticated
application may return a login redirect, which can be expected.

## 8. Updating the portal

From the project directory:

    git pull --ff-only
    .venv/bin/pip install -r requirements.txt
    .venv/bin/python manage.py check
    .venv/bin/python manage.py collectstatic --noinput
    sudo systemctl restart clinical-portal.service

If Nginx configuration changes, run nginx -t before reloading Nginx.

## 9. Backups and rollback

Before changing production configuration, create timestamped backups of
the Nginx site files and systemd service file.

For application rollback:
- Select a previously tested Git commit.
- Restore that application version.
- Install its requirements if needed.
- Run Django checks and collect static files.
- Restart the portal service.

For Nginx rollback:
- Restore the relevant Nginx backup.
- Run sudo nginx -t.
- Reload Nginx only if the test passes.

Do not delete application databases, uploaded media, environment files,
certificates or other applications when rolling back the portal.

## 10. Security

- Keep DEBUG disabled in production.
- Use a unique production Django secret key.
- Keep environment files root-readable only.
- Never commit secrets, private keys, certificates or patient data.
- Keep Gunicorn bound to loopback.
- Use HTTPS for browser-facing access.
- Keep linked clinical applications independently authenticated.
