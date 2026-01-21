from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base


class QuizAttempt(Base):
    __tablename__ = "quizattempts"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey("users.id"), nullable=False)
    articleid = Column(Integer, ForeignKey("articles.id"), nullable=False)
    score = Column(Float, nullable=False)
    submittedat = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")
    article = relationship("Article", back_populates="quiz_attempts")
