from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from app import models, schemas


def get_analysis(db: Session, analysis_id: int):
    """Get analysis by ID"""
    return db.execute(
        select(models.Analysis).where(models.Analysis.id == analysis_id)
    ).scalar_one_or_none()


def get_analyses(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: str = None,
        error_type: str = None,
        search: str = None
):
    """Get analysis list with filtration"""
    query = select(models.Analysis)

    if status:
        query = query.where(models.Analysis.status == status)
    if error_type:
        query = query.where(models.Analysis.error_type == error_type)
    if search:
        query = query.where(
            (models.Analysis.project_name.ilike(f"%{search}%")) |
            (models.Analysis.commit_hash.ilike(f"%{search}%"))
        )

    query = query.offset(skip).limit(limit)
    return db.execute(query).scalars().all()


def create_analysis(db: Session, analysis: schemas.AnalysisCreate):
    """Create new analysis"""
    db_analysis = models.Analysis(**analysis.model_dump())
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis


def update_analysis(db: Session, analysis_id: int, analysis_update: schemas.AnalysisUpdate):
    """Update analysis by ID"""
    update_data = analysis_update.model_dump(exclude_unset=True)
    if not update_data:
        return None

    result = db.execute(
        update(models.Analysis)
        .where(models.Analysis.id == analysis_id)
        .values(**update_data)
        .returning(models.Analysis)
    )
    db.commit()
    return result.scalar_one_or_none()


def delete_analysis(db: Session, analysis_id: int):
    """Delete anlysis by ID (CASCADE delete notes)"""
    result = db.execute(
        delete(models.Analysis).where(models.Analysis.id == analysis_id)
    )
    db.commit()
    return result.rowcount > 0


def create_note(db: Session, analysis_id: int, note: schemas.NoteCreate):
    """Add note to analysis"""
    db_note = models.AnalysisNote(analysis_id=analysis_id, **note.model_dump())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_analysis_notes(db: Session, analysis_id: int):
    """Get all analysis notes"""
    return db.execute(
        select(models.AnalysisNote)
        .where(models.AnalysisNote.analysis_id == analysis_id)
        .order_by(models.AnalysisNote.created_at.desc())
    ).scalars().all()