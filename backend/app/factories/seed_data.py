from datetime import datetime

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User, Role
from app.models.article import Article
from app.models.quiz_attempt import QuizAttempt


def seed_initial_data(db: Session) -> None:
    """Seed initial data into the database if it's empty.

    This is a simple factory-like seeder to help during development.
    """

    # Avoid reseeding if users already exist
    if db.query(User).count() > 0:
        return

    # Create users
    user1 = User(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        role=Role.ADMIN,
    )
    user2 = User(
                username="alice",
        email="alice@example.com",
        hashed_password=get_password_hash("password123"),
        role=Role.USER,
    )
    
    user3 = User(
    username="zakaria",
    email="zakaria@example.com",
    hashed_password=get_password_hash("password123"),
    role=Role.USER,
    )
        
    db.add_all([user1, user2, user3])
    db.flush()

    # Create articles
    article1 = Article(
        url="https://en.wikipedia.org/wiki/Machine_learning",
        title="Machine learning",
        action="SUMMARY",
        createdat=datetime.utcnow(),
    )

    article2 = Article(
        url="https://en.wikipedia.org/wiki/Artificial_intelligence",
        title="Artificial intelligence",
        action="QUIZ",
        createdat=datetime.utcnow(),
    )

    db.add_all([article1, article2])
    db.flush()

    # Create quiz attempts
    attempt1 = QuizAttempt(
        userid=user2.id,
        articleid=article2.id,
        score=85.5,
        submittedat=datetime.utcnow(),
    )

    db.add(attempt1)
    db.commit()
