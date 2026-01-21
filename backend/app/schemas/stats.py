from pydantic import BaseModel


class GlobalStatsResponse(BaseModel):
    total_users: int
    total_articles: int
    total_quizzes_generated: int
    total_downloads: int
