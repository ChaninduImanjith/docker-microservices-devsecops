import os
from fastapi import FastAPI
import redis
import psycopg2

app = FastAPI(title="Microservice Backend API")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Docker Microservices DevSecOps Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/db-check")
def db_check():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "postgres"),
            database=os.getenv("POSTGRES_DB", "appdb"),
            user=os.getenv("POSTGRES_USER", "appuser"),
            password=os.getenv("POSTGRES_PASSWORD", "apppassword"),
            connect_timeout=3
        )
        conn.close()
        return {"database": "connected"}
    except Exception as e:
        return {"database": "disconnected", "error": str(e)}

@app.get("/cache-check")
def cache_check():
    try:
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            socket_connect_timeout=3
        )
        r.ping()
        return {"cache": "connected"}
    except Exception as e:
        return {"cache": "disconnected", "error": str(e)}
