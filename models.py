# TODO: Logs table with logs from app (history of app activities (like login, inserting , deletein etc)
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship



class Base(DeclarativeBase):
    pass

class Log(Enum):
    pass


class Projects(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    project_owner: Mapped[str] = mapped_column(String, default="unknown", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    beginning: Mapped[str] = mapped_column(String, nullable=False)
    end: Mapped[str | None]= mapped_column(String, nullable=True)
    # RELATIONSHIP
    project_details: Mapped[list["ProjectDetails"]] = relationship("ProjectDetails",
                                                                                back_populates="project",
                                                                                cascade="all, delete-orphan",)

    # For annotations because pycharm cant see Mapped[]
    def __init__(
            self,
            name: str,
            description: str,
            project_owner: str = "unknown",
            is_active: bool | None = True,
            beginning: str | None = None,
            end: str | None = None
    ):
        self.name = name
        self.description = description
        self.project_owner = project_owner
        self.beginning = beginning
        self.end = end

class ProjectDetails(Base):
    __tablename__ = 'project_details'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    activity: Mapped[str | None] = mapped_column(String, nullable=True)
    item: Mapped[str | None] = mapped_column(String, nullable=True)
    item_code: Mapped[str] = mapped_column(String)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    # relationship
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), nullable=False)
    project = relationship("Projects", back_populates="project_details")




