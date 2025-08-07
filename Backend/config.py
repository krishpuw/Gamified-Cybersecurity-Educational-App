class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"                  
    SQLALCHEMY_TRACK_MODIFICATIONS = False                         

    SECRET_KEY = "super-secret-key"                              

    CALDERA_URL = "http://localhost:8888"                         
    API_KEY = 'ADMIN123'                                           

    BACKEND_URL = "http://localhost:5000/"                          


# This is a temporary database with sql , later will be changed to postgresql when connected to the server 
#SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@server-ip:5432/dbname"


## CHANGE HERE 31 JULY 