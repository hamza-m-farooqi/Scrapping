from typing import List, Optional
from sqlalchemy import ForeignKey, String, INTEGER, DATETIME, BOOLEAN, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass


class AI_Generated_Images_Platforms_Info(Base):
    __tablename__ = "AI_Generated_Images_Platforms_Info"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    primary_link: Mapped[str] = mapped_column(String)
    secondary_link: Mapped[str] = mapped_column(String)
    use_secondary_link: Mapped[bool] = mapped_column(BOOLEAN)
    total_pages: Mapped[int] = mapped_column(INTEGER)

    def __repr__(self) -> str:
        return f"AI_Generated_Images_Platforms_Info(id={self.id}, name={self.name}, primary_link={self.primary_link}, secondary_link={self.secondary_link}, use_secondary_link={self.use_secondary_link}, total_pages={self.total_pages})"


class AI_Generated_Images_Scrapping_Info(Base):
    __tablename__ = "AI_Generated_Images_Scrapping_Info"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DATETIME)
    platform_id: Mapped[int] = mapped_column(
        ForeignKey("AI_Generated_Images_Platforms_Info.id")
    )
    # platform:Mapped["AI_Generated_Images_Platforms_Info"]=relationship(back_populates="AI_Generated_Images_Platforms_Info")
    page_number: Mapped[int] = mapped_column(INTEGER)
    image_number: Mapped[int] = mapped_column(INTEGER)
    image_id: Mapped[str] = mapped_column(String)
    image_name: Mapped[str] = mapped_column(String)
    image_src: Mapped[str] = mapped_column(String)
    image_promt: Mapped[str] = mapped_column(String)
    image_download_status: Mapped[bool] = mapped_column(BOOLEAN)

    __table_args__ = (
        Index("index_platform_id_&_image_name", "platform_id", "image_name"),
    )

    def __repr__(self) -> str:
        return f"AI_Generated_Images_Scrapping_Info(id={self.id},date={self.date},platform_id={self.platform_id},page_number={self.page_number},image_number={self.image_number},image_id={self.image_id},image_name={self.image_name},image_src={self.image_src},image_promt={self.image_promt},image_download_status={self.image_download_status})"


class AI_Generated_Images_Search_Words(Base):
    __tablename__ = "AI_Generated_Images_Search_Words"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"AI_Generated_Images_Search_Words(id={self.id},keyword={self.keyword})"


class AI_Generated_Images_Search_Words_Track(Base):
    __tablename__ = "AI_Generated_Images_Search_Words_Track"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    platform_id: Mapped[int] = mapped_column(
        ForeignKey("AI_Generated_Images_Platforms_Info.id")
    )
    # platform:Mapped["AI_Generated_Images_Platforms_Info"]=relationship(back_populates="AI_Generated_Images_Platforms_Info")
    search_word_id: Mapped[int] = mapped_column(
        ForeignKey("AI_Generated_Images_Search_Words.id")
    )
    # search_word:Mapped["AI_Generated_Images_Search_Words"]=relationship(back_populates="AI_Generated_Images_Search_Words")
    search_status: Mapped[bool] = mapped_column(BOOLEAN)

    def __repr__(self) -> str:
        return f"AI_Generated_Images_Search_Words_Track(id={self.id},platform_id={self.platform_id},search_word_id={self.search_word_id},search_status={self.search_status})"
