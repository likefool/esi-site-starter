# ESI Site Starter

這是一個結合 GitHub Pages、Tailwind CSS、Python async FastAPI 組頁與 Vanilla ESI 的靜態網站起手架構。

## Test the Endpoint

```
PYTHONPATH=./public uvicorn public.app:app --reload
```

## How to Run the Script
Save the script as convert_markdown.py in the root of your project.
Run the script using Python:
```
python convert_markdown.py
```

## deploy
```
docker build -t esi-site .
docker run -p 127.0.0.1:18000:18000 esi-site
```

## flow
- inside container
- a script
1. checkout md from another repo
1. cp to content
1. run convert
- 5min cron 



