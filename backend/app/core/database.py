from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()
url = os.getenv("DATABASE_URL")
if not url:
   raise RuntimeError("DATABASE_URL is not set")

engine = create_async_engine(url)

async def ping_db():
   async with engine.connect() as conn:
      result = await conn.execute(text("SELECT 1"))
      return {"result": result.all()[0][0]}



