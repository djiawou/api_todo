import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    #SECRET_KEY=os.getenv("JWT_SECRET_KEY")