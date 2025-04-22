from datetime import date

from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Vacation(Base):
    __tablename__ = "vacation"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[int] = mapped_column(index=True)
    start_date: Mapped[date] = mapped_column()
    end_date: Mapped[date] = mapped_column()
