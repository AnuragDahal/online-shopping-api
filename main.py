from fastapi import FastAPI
from settings import database
from models import models
from routes import orders, users, admin, auth
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Your routes and other application code go here

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

models.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(admin.router)
