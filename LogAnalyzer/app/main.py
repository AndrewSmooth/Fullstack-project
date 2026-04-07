from fastapi import FastAPI, Request, HTTPException, Header, Path, Query
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import List, Optional
import logging
import json
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="CI-AI Backend", version="1.0")


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    success: bool
    message: str
    user: Optional[dict] = None


@app.post("/api/auth/login", response_model=AuthResponse)
async def login(data: LoginRequest):
    if data.email == "email@example.com" and data.password == "password":
        return AuthResponse(
            success=True,
            message="Успешный вход",
            user={"id": 1, "email": data.email}
        )
    raise HTTPException(status_code=401, detail="Неверный email или пароль")


@app.post("/api/auth/register", response_model=AuthResponse)
async def register(data: LoginRequest):
    return AuthResponse(
        success=True,
        message="Пользователь зарегистрирован",
        user={"id": random.randint(2, 100), "email": data.email}
    )


class AnalysisItem(BaseModel):
    id: int
    dateTime: str
    pipeline: str
    status: str  # "process" | "analyzed"
    errorType: str


class CatalogResponse(BaseModel):
    items: List[AnalysisItem]
    total: int


@app.get("/api/catalog", response_model=CatalogResponse)
async def get_catalog(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        search: Optional[str] = None,
        status: Optional[str] = None,
        error_type: Optional[str] = None
):
    mock_items = [
        AnalysisItem(id=i, dateTime=f"2026-04-0{i} 14:32",
                     pipeline=f"main/abc123{i}",
                     status=random.choice(["process", "analyzed"]),
                     errorType=random.choice(["Timeout", "Permission", "Dependency"]))
        for i in range(1, 21)
    ]

    # filtration
    if search:
        mock_items = [i for i in mock_items if search.lower() in i.pipeline.lower()]
    if status:
        mock_items = [i for i in mock_items if i.status == status]
    if error_type:
        mock_items = [i for i in mock_items if i.error_type == error_type]

    # pagination
    start = (page - 1) * limit
    end = start + limit

    return CatalogResponse(
        items=mock_items[start:end],
        total=len(mock_items)
    )


class UploadRequest(BaseModel):
    log_content: Optional[str] = None
    file_name: Optional[str] = None
    project_name: str = "my-project"
    branch: str = "main"
    commit_hash: str = "abc123def"
    auto_parse: bool = False


class UploadResponse(BaseModel):
    success: bool
    analysis_id: int
    message: str
    estimated_time_sec: float


@app.post("/api/upload", response_model=UploadResponse)
async def upload_log(data: UploadRequest):
    # В реальности: сохранение лога, запуск Celery-задачи
    return UploadResponse(
        success=True,
        analysis_id=random.randint(1000, 9999),
        message="Анализ запущен",
        estimated_time_sec=random.uniform(2.0, 5.0)
    )


class AIRecommendation(BaseModel):
    reason: str
    steps: List[str]
    similar_cases: int


class AnalysisDetail(BaseModel):
    id: int
    pipeline: str
    status: str
    classification: str
    confidence: float
    analysisTime: float
    logFragment: str
    aiRecommendation: AIRecommendation


@app.get("/api/analysis/{analysis_id}", response_model=AnalysisDetail)
async def get_analysis(analysis_id: int = Path(..., ge=1)):
    return AnalysisDetail(
        id=analysis_id,
        pipeline="main-pipeline-build",
        status="Ошибка найдена",
        classification="Dependency Conflict",
        confidence=0.92,
        analysisTime=3.2,
        logFragment="""[INFO] Installing dependencies...
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
npm ERR! While resolving: project@1.0.0
npm ERR! Found: react@18.2.0""",
        aiRecommendation=AIRecommendation(
            reason="Конфликт версий зависимостей между react@18.2.0 и требуемой версией",
            steps=[
                "Обновить package.json",
                "Запустить npm install --legacy-peer-deps",
                "Пересобрать проект"
            ],
            similar_cases=3
        )
    )


class KPIMetric(BaseModel):
    label: str
    value: str


class CategoryDistribution(BaseModel):
    category: str
    percentage: float


class DailyTrend(BaseModel):
    day: str
    count: int


class TopProblem(BaseModel):
    error: str
    count: int
    recommendation: str


class AnalyticsResponse(BaseModel):
    kpi: List[KPIMetric]
    categories: List[CategoryDistribution]
    daily_trend: List[DailyTrend]
    top_problems: List[TopProblem]
    period: str


@app.get("/api/analytics", response_model=AnalyticsResponse)
async def get_analytics(
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
):
    return AnalyticsResponse(
        kpi=[
            KPIMetric(label="Всего сбоев", value="47"),
            KPIMetric(label="Доминирующий тип", value="Permission"),
            KPIMetric(label="Среднее время исправления", value="2.4ч"),
            KPIMetric(label="% успешных фиксов", value="87%"),
        ],
        categories=[
            CategoryDistribution(category="Permission", percentage=40.0),
            CategoryDistribution(category="Dependency", percentage=25.0),
            CategoryDistribution(category="Timeout", percentage=20.0),
            CategoryDistribution(category="Syntax", percentage=10.0),
            CategoryDistribution(category="Other", percentage=5.0),
        ],
        daily_trend=[
            DailyTrend(day="Пн", count=5),
            DailyTrend(day="Вт", count=8),
            DailyTrend(day="Ср", count=4),
            DailyTrend(day="Чт", count=12),
            DailyTrend(day="Пт", count=7),
            DailyTrend(day="Сб", count=6),
            DailyTrend(day="Вс", count=5),
        ],
        top_problems=[
            TopProblem(error="Permission denied", count=19, recommendation="Провести аудит Docker-образов"),
            TopProblem(error="Dependency conflict", count=12, recommendation="Обновить package.json"),
            TopProblem(error="Timeout after 300s", count=9, recommendation="Оптимизировать скрипты"),
        ],
        period="1-7 апреля 2026"
    )


class GiteaAlert(BaseModel):
    source: str
    event: str
    repository: str
    workflow: str
    run_id: str
    run_url: str
    message: str
    timestamp: str

    class Config:
        extra = "allow"


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/alerts", status_code=202)
async def receive_alert(
        request: Request,
        x_gitea_event: str | None = Header(None, alias="X-Gitea-Event"),
        x_api_key: str | None = Header(None, alias="X-Api-Key")
):
    try:
        body = await request.json()
        alert = GiteaAlert(**body)
        logger.warning(f"ALERT RECEIVED: {alert.event} in {alert.repository} (run #{alert.run_id})")
        return {"status": "accepted", "run_id": alert.run_id, "received_at": datetime.utcnow().isoformat()}
    except Exception as e:
        logger.error(f"Failed to process alert: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")


@app.get("/api/alerts")
async def list_alerts(limit: int = Query(10, le=100)):
    return {"alerts": [], "note": "Endpoint in development"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)