#FastAPI Imports
from fastapi import FastAPI, Response,status
from fastapi.middleware.cors import CORSMiddleware
from src.urls.v1 import users

#Local Imports
# from src.urls.v1 import (
#     users
# )

def init_app():
    app = FastAPI(
        title="Softedge AI",
        description="Softedge AI",
        version="1.0.0",
        contact={
            "name": "Softedge",
            # "url": "",
            # "email": "",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        terms_of_service="https://www.example.com/terms",
        docs_url='/docs',
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT","DELETE"],
        allow_headers=["Content-Type", "Authorization"],
    )

    app.include_router(users.router,tags=["Users"])

    return app


app = init_app()

@app.router.get("/")
def result():
    return Response(
        status_code = status.HTTP_200_OK
    )
