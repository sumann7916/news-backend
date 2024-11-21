This repository consists of Backend for News Aggregator & Summarizer system that scrapes news from other news articles and summarizes them.
It is written Django and uses Postgresql.

TO run this project:

Initialize database
```
cp env.example .env
docker compose up -d
```
Install Requirements
```
pip install -r requirements.txt
```
Make Migrations
```
cd app
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

```
