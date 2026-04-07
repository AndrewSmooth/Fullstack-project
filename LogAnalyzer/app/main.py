from fastapi import FastAPI, Request, HTTPException, Header
from pydantic import BaseModel, Field
from datetime import datetime
import logging
import json

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gitea Alert Receiver", version="1.0")


# Модель входящего алерта (гибкая, принимает любые поля)
class GiteaAlert(BaseModel):
    source: str = Field(..., description="Источник: gitea-actions")
    event: str = Field(..., description="Тип события: workflow_failure")
    repository: str
    workflow: str
    run_id: str
    run_url: str
    message: str
    timestamp: str

    # Все остальные поля — в extra
    class Config:
        extra = "allow"


@app.get("/health")
async def health():
    """Проверка работоспособности"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/alerts", status_code=202)
async def receive_alert(
        request: Request,
        x_gitea_event: str | None = Header(None, alias="X-Gitea-Event"),
        x_api_key: str | None = Header(None, alias="X-Api-Key")
):
    """
    Принимает алерты от Gitea Actions.

    Пример запроса:
    POST /api/alerts
    Headers:
      Content-Type: application/json
      X-Gitea-Event: workflow_failure
      X-Api-Key: your-secret-key (опционально)
    Body: { "source": "gitea-actions", "event": "workflow_failure", ... }
    """

    # 🔐 Опциональная проверка токена (раскомментируйте, если нужно)
    # EXPECTED_KEY = "your-super-secret-key"
    # if x_api_key != EXPECTED_KEY:
    #     raise HTTPException(status_code=403, detail="Invalid API key")

    try:
        body = await request.json()
        alert = GiteaAlert(**body)

        # 📝 Логируем ключевые поля
        logger.warning(
            f"🚨 ALERT RECEIVED: {alert.event} in {alert.repository} "
            f"(run #{alert.run_id}) — {alert.message}"
        )

        # 🔍 Логируем всё для отладки (в продакшене можно убрать или отправить в файл)
        logger.debug(f"Full payload: {json.dumps(body, ensure_ascii=False)}")

        # 🎯 Здесь можно добавить:
        # - Сохранение в БД (PostgreSQL, SQLite)
        # - Отправку в Telegram/Slack
        # - Агрегацию статистики
        # - Триггер на повторный запуск пайплайна

        return {
            "status": "accepted",
            "run_id": alert.run_id,
            "received_at": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Failed to process alert: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid payload: {str(e)}")


@app.get("/api/alerts")
async def list_alerts(limit: int = 10):
    """Заглушка для будущего API получения алертов"""
    return {
        "alerts": [],
        "note": "Эндпоинт в разработке. Используйте POST /api/alerts для отправки."
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)