from __future__ import annotations

import json

from app.domain.entities.page_analysis import PageSummary
from app.infrastructure.repositories.base import HistoryRepositoryBase
from app.infrastructure.storage.sqlite import SQLiteDatabase


class HistoryRepository(HistoryRepositoryBase):
    def __init__(self, database: SQLiteDatabase) -> None:
        self.database = database

    def add(self, summary: PageSummary) -> None:
        self.database.execute(
            """
            INSERT INTO page_history(url, title, status, safety_score, summary_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                summary.url,
                summary.title,
                summary.status.value,
                summary.safety_score,
                summary.model_dump_json(),
                summary.created_at.isoformat(),
            ),
        )

    def list(self, limit: int = 50) -> list[dict]:
        rows = self.database.fetchall(
            "SELECT id, url, title, status, safety_score, summary_json, created_at "
            "FROM page_history ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [
            {
                "id": row["id"],
                "url": row["url"],
                "title": row["title"],
                "status": row["status"],
                "safety_score": row["safety_score"],
                "summary": json.loads(row["summary_json"]),
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def clear(self) -> None:
        self.database.execute("DELETE FROM page_history")
