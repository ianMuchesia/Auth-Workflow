from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.middlewares.error_handler import validation_exception_handler, integrity_error_handler
from app.routers import sendmail, auth_router,user_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)



#exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)

#database integrity error handler, not necessary but good to have
app.add_exception_handler(IntegrityError, integrity_error_handler)

app.include_router(sendmail.router)
app.include_router(auth_router.router)
app.include_router(user_router.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}