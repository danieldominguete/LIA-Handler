from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import uvicorn
import logging

# ----------------------------------------------------------
# app logging configuration - only terminal
logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
formatter = logging.Formatter(
    "%(asctime)s: %(levelname)s - %(message)s", datefmt="%y-%m-%d %H:%M"
)
console_handler.setFormatter(formatter)
# ----------------------------------------------------------
# Start application

app = FastAPI(title="LIA Handler")

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    response = {"message": "Hello World"}
    logging.info(f"/ response: {response}")
    return response


handler = Mangum(app=app, enable_lifespan=False)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
