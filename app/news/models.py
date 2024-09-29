from app.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Uuid, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class NewsCreator(Base):
    __tablename__ = "news_creator"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, unique=True, index=True)
    url = Column(String, unique=True, index=True)

    news = relationship("News", back_populates="creator")


class NewsCategory(Base):
    __tablename__ = "news_category"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, unique=True, index=True)


class News(Base):
    __tablename__ = "news"

    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    title = Column(String, index=True)
    summary = Column(String)
    link = Column(String)

    creator_id = Column(UUID, ForeignKey("news_creator.id"))
    creator = relationship("NewsCreator", back_populates="news")
