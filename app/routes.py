from fastapi import APIRouter
from fastapi import APIRouter, Depends
from security.auth import get_current_active_user
from app.utils.autogenerate.generate import generate_router
from . routers.notification import notification_router
import glob

ActiveUser = Depends(get_current_active_user)
app_routers = APIRouter()

app_routers.include_router(generate_router)
app_routers.include_router(notification_router, prefix="/ws")

app_routers.dependencies = [ActiveUser]


routers = glob.glob("app/routers/*.py")


for router_file in routers:
    router_name = router_file.split(".py")[0].split("app/routers/")[1]
    router = __import__(f"app.routers.{router_name}", globals(), locals(), [f"{router_name}_router"], 0)
    app_routers.include_router(getattr(router, f"{router_name}_router"))
