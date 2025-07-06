from fastapi import FastAPI
from config.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from controller import student_controller ,course_controller, result_controller, stats_controller
# from middleware.auth_middleware import CustomMiddleware
# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your fronte nd URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    "logs/app.log",
    rotation="30 MB",           # Rotate logs when they reach 30 MB
    retention="30 days",        # Keep logs for 30 days
    compression="zip",          # Compress old log files
    level="INFO",               # Minimum log level
    format="{time} -  {level} - {message}"  # Log format    
)


@app.get("/api")
def read_root():
    logger.info("Welcome to the API")
    return {"message": "Welcome to the API"}

# app.add_middleware(CustomMiddleware)


# Register routers
app.include_router(student_controller.student_router, prefix="/api/students", tags=["students"])
app.include_router(course_controller.course_router, prefix="/api/courses", tags=["courses"])
app.include_router(result_controller.result_router, prefix="/api/results", tags=["results"])
app.include_router(stats_controller.stats_router, prefix="/api/stats", tags=["stats"])


@app.on_event("startup")
async def startup_event():
    print("App is starting.")

@app.on_event("shutdown")
async def shutdown_event():
    print("App is shutting down.")
