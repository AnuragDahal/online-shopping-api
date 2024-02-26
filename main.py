from fastapi import FastAPI
from settings.database import  engine
from models import models
from routes import orders, users, admin, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Shopping Cart Api",
)


@app.on_event("startup")
async def startup():
    print("Server is running")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(admin.router)
