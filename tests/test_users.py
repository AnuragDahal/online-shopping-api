from fastapi.testclient import TestClient 
from routes import users


clent=TestClient(users.router)




