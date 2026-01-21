from sqlalchemy.orm import Session

from app.models.article import Article
from app.models.quiz_attempt import QuizAttempt
from app.models.user import User


def get_global_stats(db: Session) -> dict:
    total_users = db.query(User).count()
    total_articles = db.query(Article).count()
    total_quizzes_generated = db.query(QuizAttempt).count()  # proxy
    total_downloads = 0  # to be tracked when export feature is implemented

    return {
        "total_users": total_users,
        "total_articles": total_articles,
        "total_quizzes_generated": total_quizzes_generated,
        "total_downloads": total_downloads,
    }
