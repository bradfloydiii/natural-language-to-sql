## AI SPECIALIST DEMO


## To run the application (FastAPI)
```
uvicorn app.main:app --reload
```

## Seed the database
```
sqlite3 clemis_demo.db < data/seed.sql
```

## Test
```
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"q":"Show me incidents involving John Red Smith in the last 30 days and include plates"}'
```