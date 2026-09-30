import json
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Request,
    Depends,
    Form,
    File,
    UploadFile,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from .models import User, Recommendation
from .security import (
    hash_password,
    verify_password,
    create_token,
    decode_token
)
from .services import home, party, jewelry


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
UPLOADS_DIR = STATIC_DIR / "uploads"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# DATABASE / APP LIFESPAN
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class HomeRequest(BaseModel):

    budget: float = Field(gt=0)

    room_type: str

    style: str

    lights: int = Field(
        default=0,
        ge=0
    )

    fans: int = Field(
        default=0,
        ge=0
    )

    tables: int = Field(
        default=0,
        ge=0
    )

    additional_requirements: str = ""


class PartyRequest(BaseModel):

    budget: float = Field(gt=0)

    guests: int = Field(gt=0)

    event_type: str

    venue: str

    food_preference: str

    additional_requirements: str = ""


# ============================================================
# AUTHENTICATION HELPERS
# ============================================================

def current_user(
    request: Request,
    db: Session
):
    """
    Get the currently logged-in user from the access_token cookie.
    """

    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = decode_token(token)

    if not payload:
        return None

    if not payload.get("sub"):
        return None

    try:

        user_id = int(payload["sub"])

        return db.get(User, user_id)

    except (ValueError, TypeError):
        return None


def require_user(
    request: Request,
    db: Session
):
    """
    Require the user to be logged in.
    """

    user = current_user(request, db)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Please log in first."
        )

    return user


# ============================================================
# SAVE RECOMMENDATION
# ============================================================

def save(
    db: Session,
    user,
    kind,
    data,
    result
):

    row = Recommendation(
        user_id=user.id,
        planner_type=kind,
        request_json=json.dumps(data),
        response_json=json.dumps(result)
    )

    db.add(row)

    db.commit()

    db.refresh(row)

    return row


# ============================================================
# HOME / INDEX
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def index(
    request: Request,
    db: Session = Depends(get_db)
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "user": current_user(request, db)
        }
    )


# ============================================================
# REGISTER PAGE
# ============================================================

@app.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "request": request
        }
    )


# ============================================================
# REGISTER
# ============================================================

@app.post("/register")
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    email = email.strip().lower()

    if len(password) < 8:

        return RedirectResponse(
            "/register?error=Password%20must%20be%20at%20least%208%20characters.",
            status_code=303
        )

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        return RedirectResponse(
            "/register?error=Email%20already%20registered.",
            status_code=303
        )

    new_user = User(
        name=name.strip(),
        email=email,
        password_hash=hash_password(password)
    )

    db.add(new_user)

    db.commit()

    return RedirectResponse(
        "/login?registered=1",
        status_code=303
    )


# ============================================================
# LOGIN PAGE
# ============================================================

@app.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(
    request: Request
):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request
        }
    )


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email.strip().lower()
    ).first()

    if not user or not verify_password(
        password,
        user.password_hash
    ):

        return RedirectResponse(
            "/login?error=Invalid%20email%20or%20password.",
            status_code=303
        )

    response = RedirectResponse(
        "/dashboard",
        status_code=303
    )

    response.set_cookie(
        "access_token",
        create_token(user.id),
        httponly=True,
        samesite="lax",
        max_age=86400
    )

    return response


# ============================================================
# LOGOUT
# ============================================================

@app.get("/logout")
def logout():

    response = RedirectResponse(
        "/login",
        status_code=303
    )

    response.delete_cookie("access_token")

    return response


# ============================================================
# DASHBOARD
# ============================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    recent = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id
        )
        .order_by(
            Recommendation.created_at.desc()
        )
        .limit(5)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": user,
            "recent": recent
        }
    )


# ============================================================
# HOME PLANNER PAGE
# ============================================================

@app.get(
    "/home-planner",
    response_class=HTMLResponse
)
def home_page(
    request: Request,
    db: Session = Depends(get_db)
):

    return templates.TemplateResponse(
        request=request,
        name="home_planner.html",
        context={
            "request": request,
            "user": current_user(request, db)
        }
    )


# ============================================================
# PARTY PLANNER PAGE
# ============================================================

@app.get(
    "/party-planner",
    response_class=HTMLResponse
)
def party_page(
    request: Request,
    db: Session = Depends(get_db)
):

    return templates.TemplateResponse(
        request=request,
        name="party_planner.html",
        context={
            "request": request,
            "user": current_user(request, db)
        }
    )


# ============================================================
# JEWELRY PLANNER PAGE
# ============================================================

@app.get(
    "/jewelry-planner",
    response_class=HTMLResponse
)
def jewelry_page(
    request: Request,
    db: Session = Depends(get_db)
):

    return templates.TemplateResponse(
        request=request,
        name="jewelry_planner.html",
        context={
            "request": request,
            "user": current_user(request, db)
        }
    )


# ============================================================
# GENERATE HOME PLAN
# ============================================================

@app.post("/generate-home")
def generate_home(
    payload: HomeRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    data = payload.model_dump()

    result = home(data)

    row = save(
        db,
        user,
        "home",
        data,
        result
    )

    return {
        "success": True,
        "history_id": row.id,
        "result": result
    }


# ============================================================
# GENERATE PARTY PLAN
# ============================================================

@app.post("/generate-party")
def generate_party(
    payload: PartyRequest,
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    data = payload.model_dump()

    result = party(data)

    row = save(
        db,
        user,
        "party",
        data,
        result
    )

    return {
        "success": True,
        "history_id": row.id,
        "result": result
    }


# ============================================================
# GENERATE JEWELRY PLAN
# ============================================================

@app.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_color: str = Form(""),
    additional_requirements: str = Form(""),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    image_bytes = None
    mime = None

    if image and image.filename:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail="Use JPG, PNG or WEBP."
            )

        image_bytes = await image.read()

        max_size = (
            settings.MAX_UPLOAD_MB
            * 1024
            * 1024
        )

        if len(image_bytes) > max_size:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Image must be under "
                    f"{settings.MAX_UPLOAD_MB} MB."
                )
            )

        mime = image.content_type

        safe_filename = os.path.basename(
            image.filename
        ).replace(" ", "_")

        upload_path = (
            UPLOADS_DIR / safe_filename
        )

        upload_path.write_bytes(
            image_bytes
        )

    data = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "outfit_color": outfit_color,
        "additional_requirements":
            additional_requirements
    }

    result = jewelry(
        data,
        image_bytes,
        mime
    )

    row = save(
        db,
        user,
        "jewelry",
        data,
        result
    )

    return {
        "success": True,
        "history_id": row.id,
        "result": result
    }


# ============================================================
# HISTORY
# ============================================================

@app.get(
    "/history",
    response_class=HTMLResponse
)
def history(
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    rows = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id
        )
        .order_by(
            Recommendation.created_at.desc()
        )
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "request": request,
            "user": user,
            "history": rows
        }
    )


# ============================================================
# RECOMMENDATION PAGE
# ============================================================

@app.get(
    "/recommendations/{rid}",
    response_class=HTMLResponse
)
def recommendation_page(
    rid: int,
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    row = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == rid,
            Recommendation.user_id == user.id
        )
        .first()
    )

    if not row:

        return RedirectResponse(
            "/history",
            status_code=303
        )

    # Safely load the stored JSON
    try:

        result = json.loads(
            row.response_json
        )

    except (json.JSONDecodeError, TypeError):

        result = {
            "summary": "Unable to load recommendation data.",
            "budget": 0,
            "items": []
        }

    return templates.TemplateResponse(
        request=request,
        name="recommendations.html",
        context={
            "request": request,
            "user": user,
            "item": row,
            "result": result
        }
    )


# ============================================================
# SAVE / UNSAVE RECOMMENDATION
# ============================================================

@app.post(
    "/recommendations/{rid}/save"
)
def toggle_save(
    rid: int,
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    row = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == rid,
            Recommendation.user_id == user.id
        )
        .first()
    )

    if not row:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found."
        )

    row.saved = not row.saved

    db.commit()

    return {
        "saved": row.saved
    }


# ============================================================
# TOKEN
# ============================================================

@app.post("/token")
def token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == username.strip().lower()
    ).first()

    if not user or not verify_password(
        password,
        user.password_hash
    ):

        return JSONResponse(
            {
                "detail": "Invalid credentials"
            },
            status_code=401
        )

    return {
        "access_token":
            create_token(user.id),
        "token_type":
            "bearer"
    }


# ============================================================
# SESSION INFO
# ============================================================

@app.get("/session-info")
def session_info(
    request: Request,
    db: Session = Depends(get_db)
):


    user = current_user(
        request,
        db
    )

    if not user:

        return {
            "logged_in": False
        }

    return {
        "logged_in": True,
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }


# ============================================================
# SESSION DATA
# ============================================================

@app.get("/session-data")
def session_data(
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    total = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id
        )
        .count()
    )

    saved = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id,
            Recommendation.saved.is_(True)
        )
        .count()
    )

    return {
        "user_id": user.id,
        "recommendation_count": total,
        "saved_count": saved
    }


# ============================================================
# RECOMMENDATION DETAILS API
# ============================================================

@app.get(
    "/recommendations-details/{rid}"
)
def recommendation_details(
    rid: int,
    request: Request,
    db: Session = Depends(get_db)
):

    user = require_user(
        request,
        db
    )

    row = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == rid,
            Recommendation.user_id == user.id
        )
        .first()
    )

    if not row:

        raise HTTPException(
            status_code=404,
            detail="Recommendation not found."
        )

    try:

        request_data = json.loads(
            row.request_json
        )

    except (json.JSONDecodeError, TypeError):

        request_data = {}

    try:

        result_data = json.loads(
            row.response_json
        )

    except (json.JSONDecodeError, TypeError):

        result_data = {}

    return {
        "id": row.id,
        "planner_type": row.planner_type,
        "request": request_data,
        "result": result_data,
        "saved": row.saved,
        "created_at": row.created_at
    }


# ============================================================
# STARTUP CHECK
# ============================================================

@app.get("/startup")
def startup():

    return {
        "status": "ok",
        "service": settings.APP_NAME
    }


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )