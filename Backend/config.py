class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"                  # ✔ Good for local testing
    SQLALCHEMY_TRACK_MODIFICATIONS = False                         # ✔ Correctly disabled

    SECRET_KEY = "super-secret-key"                                # ⚠️ Use a secure random value in production

    CALDERA_URL = "http://localhost:8888"                          # ✔ Assumes Caldera is running locally
    API_KEY = 'ADMIN123'                                           # ✔ Not needed in --insecure mode

    BACKEND_URL = "http://localhost:5000/"                          # ✔ Matches Flask's default dev port


# This is a temporary database with sql , later will be changed to postgresql when connected to the server 
#SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@server-ip:5432/dbname"


## CHANGE HERE 31 JULY 