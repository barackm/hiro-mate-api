from fastapi import FastAPI, Depends
from app.modules.users.route import router as user_router
from sqlalchemy.orm import registry
from app.modules.levels.route import router as level_router
from app.modules.promotions.route import router as promotion_router
from app.modules.programs.route import router as program_router
from app.modules.time_slots.route import router as time_slot_router
from app.modules.enrollments.route import router as enrollment_router
from app.modules.auth.route import router as auth_router
from starlette.middleware.sessions import SessionMiddleware

# from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as aioredis


async def lifespan(app: FastAPI):
    redis = await aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    await FastAPILimiter.init(redis)
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key="YOUR_SECRET_KEY")
# app.add_middleware(HTTPSRedirectMiddleware)

mapper_registry = registry()
mapper_registry.configure()

app.include_router(
    user_router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
app.include_router(
    level_router,
    prefix="/levels",
    tags=["levels"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
app.include_router(
    promotion_router,
    prefix="/promotions",
    tags=["promotions"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
app.include_router(
    program_router,
    prefix="/programs",
    tags=["programs"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
app.include_router(
    time_slot_router,
    prefix="/time-slots",
    tags=["time-slots"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
app.include_router(
    enrollment_router,
    prefix="/enrollments",
    tags=["enrollments"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(RateLimiter(times=5, seconds=60))],
)


@app.get("/", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
def read_root() -> dict:
    return {"message": "FastAPI with SQLAlchemy and Supabase"}
