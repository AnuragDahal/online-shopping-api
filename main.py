from fastapi import FastAPI
from config import models, database
from routes import orders, users, admin

app = FastAPI(
    title="Shopping Cart Api",
)

models.Base.metadata.create_all(bind=database.engine)

app.include_router(orders.router)
app.include_router(users.router)
app.include_router(admin.router)
