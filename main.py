from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from app.routes import app_routers
from app.utils.jsonToCryllic import dict_to_nested_class
from security.auth import auth_router
# from events import events_router

app = FastAPI(
    title="Gold Center"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def home():
    return "Gold Center"


@app.post("/json_to_krill")
async def krill_konverter(data_dict: dict = Body(...)):

    return dict_to_nested_class(data_dict)


# app.include_router(events_router)
app.include_router(app_routers)
app.include_router(auth_router)
