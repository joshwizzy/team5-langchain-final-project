from fastapi import FastAPI


app = FastAPI(
    title="Github Issues PM Assistant",
    description="API Endpoints for a Github Issues PM Assistant",
)


@app.get("/healthz")
async def get_status():
    return {"status": "running"}
