from fastapi import FastAPI #this is the framework for the API. fastapi is a python framework for building APIs. its
# used for builidng the API

from .routes.users import router as users_router
from .routes.chores import router as chores_router
from .routes.assignments import router as assignments_router
from .routes.logs import router as logs_router
from .routes.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from .settings import get_settings

app = FastAPI() #this is the instance of the FastAPI class. it is the main entry point for the API.

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/") #this is a decorator. it is used to define a route for the API.
def read_root():
    return {"message": "Hello, World!"} #this is the response that will be returned when the root route is accessed.

# Include CRUD routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(chores_router)
app.include_router(assignments_router)
app.include_router(logs_router)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)