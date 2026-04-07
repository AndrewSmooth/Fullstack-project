from fastapi import FastAPI, Depends, HTTPException, status, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app import models, schemas, crud
from app.database import engine, get_db, Base

# Create tables at start
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CI-AI Backend", version="1.0", docs_url="/docs", redoc_url=None)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/analyses", response_model=schemas.AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def create_analysis(
        analysis: schemas.AnalysisCreate,
        db: Session = Depends(get_db)
):
    """Create new analysis"""
    try:
        return crud.create_analysis(db, analysis)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Не удалось создать анализ: {str(e)}"
        )


@app.get("/api/analyses", response_model=schemas.AnalysisListResponse)
async def list_analyses(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        status: Optional[str] = None,
        error_type: Optional[str] = None,
        search: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Get analysis list with filtration and pagination"""
    skip = (page - 1) * limit
    items = crud.get_analyses(db, skip=skip, limit=limit, status=status, error_type=error_type, search=search)
    total = db.query(models.Analysis.id).count()

    return schemas.AnalysisListResponse(
        items=items,
        total=total,
        page=page,
        limit=limit
    )


@app.get("/api/analyses/{analysis_id}", response_model=schemas.AnalysisResponse)
async def get_analysis(
        analysis_id: int = Path(..., ge=1),
        db: Session = Depends(get_db)
):
    """Get analysis bi ID"""
    analysis = crud.get_analysis(db, analysis_id)
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Анализ #{analysis_id} не найден"
        )
    return analysis


@app.put("/api/analyses/{analysis_id}", response_model=schemas.AnalysisResponse)
async def update_analysis(
        analysis_id: int = Path(..., ge=1),
        analysis_update: schemas.AnalysisUpdate = None,
        db: Session = Depends(get_db)
):
    """Update analysis bi ID"""
    existing = crud.get_analysis(db, analysis_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Анализ #{analysis_id} не найден"
        )

    updated = crud.update_analysis(db, analysis_id, analysis_update)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Не удалось обновить анализ"
        )
    return updated


@app.delete("/api/analyses/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
        analysis_id: int = Path(..., ge=1),
        db: Session = Depends(get_db)
):
    """Delete analysis by ID"""
    existing = crud.get_analysis(db, analysis_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Анализ #{analysis_id} не найден"
        )

    crud.delete_analysis(db, analysis_id)
    return None


@app.post("/api/analyses/{analysis_id}/notes", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
        analysis_id: int = Path(..., ge=1),
        note: schemas.NoteCreate = None,
        db: Session = Depends(get_db)
):
    """Add note to analysis"""
    # Проверка, что анализ существует
    if not crud.get_analysis(db, analysis_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Анализ #{analysis_id} не найден"
        )

    return crud.create_note(db, analysis_id, note)


@app.get("/api/analyses/{analysis_id}/notes", response_model=List[schemas.NoteResponse])
async def list_notes(
        analysis_id: int = Path(..., ge=1),
        db: Session = Depends(get_db)
):
    """Get analysis notes"""
    if not crud.get_analysis(db, analysis_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Анализ #{analysis_id} не найден"
        )

    return crud.get_analysis_notes(db, analysis_id)


# Gitea alert webhook
@app.post("/api/alerts", status_code=status.HTTP_202_ACCEPTED)
async def receive_gitea_alert(request: dict, db: Session = Depends(get_db)):
    """Receive gitea alert and create analysis"""
    try:
        # Простая валидация
        required = ["source", "event", "repository", "run_id"]
        if not all(k in request for k in required):
            raise ValueError("Missing required fields")

        # Создаём анализ из вебхука
        analysis = schemas.AnalysisCreate(
            project_name=request.get("repository", "unknown"),
            commit_hash=request.get("commit", "webhook-triggered"),
            pipeline_name=request.get("workflow", "gitea-actions"),
            log_fragment=request.get("log", ""),
            status="failed" if request.get("event") == "workflow_failure" else "success",
            error_type=request.get("error_type", "Unknown"),
        )
        created = crud.create_analysis(db, analysis)

        return {
            "status": "accepted",
            "analysis_id": created.id,
            "received_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid webhook payload: {str(e)}"
        )