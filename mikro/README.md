# Nova Info

Prototype Django for the Nova Info Wi‑Fi traffic monetization SaaS. The project includes a premium marketing landing page and an administrative dashboard protected by Django authentication.

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run migrations:
   `python manage.py migrate`
4. Seed demo data:
   `python manage.py seed_demo_data`
5. Start the dev server:
   `python manage.py runserver`

## Default admin access

Create a superuser manually with:

```bash
python manage.py createsuperuser
```

Then sign in at `/admin/` or use the custom login at `/painel/login/` after creating a tenant membership for your user.

## Environment variables

Use the provided `.env.example` file as reference. For PostgreSQL, set `DATABASE_URL` to a PostgreSQL DSN.
