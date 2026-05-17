from fastapi import FastAPI
import app.core.database as database

app = FastAPI()

@app.get("/health")
def health_check():
    return {"message": "App is healthy"}

@app.get("/db_test")
async def db_test():
   result = await database.ping_db()
   return result