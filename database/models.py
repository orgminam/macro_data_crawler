from sqlalchemy import Column, Integer, String, Float, Index, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from database.manager import Base


class Master(Base):
    """비마켓 수집 항목에 대한 테이블 메타데이터"""

    __tablename__ = "gksc_s_macro_master_00"

    id = Column("id", String, primary_key=True)  # 국가코드_영문약자 kr_cpi
    name = Column("name", String)  # 한글명
    source = Column("source", String)
    unit = Column("unit", String)
    first_date = Column("first_date", String)
    last_date = Column("last_date", String)
    frequency = Column("frequency", String)
    precision = Column("precision", Integer)
    country = Column("country", String)
    main_category = Column("main_category", String)
    sub_category = Column("sub_category", String)
    params = Column("params", JSONB)

    __table_args__ = (
        {"extend_existing": True}
    )

class JobHist(Base):
    """작업 성공 히스토리 로그"""

    __tablename__ = "gksc_s_macro_job_hist_00"

    id = Column("id", String, primary_key=True)
    time_created = Column("time_created", DateTime(timezone=True), server_default=func.now(), primary_key=True)
    params = Column("params", String)

    __table_args__ = (
        {"extend_existing": True}
    )

class ErrorHist(Base):
    """작업 실패 히스토리 로그"""

    __tablename__ = "gksc_s_macro_error_hist_00"

    id = Column("id", String, primary_key=True)
    time_created = Column("time_created", DateTime(timezone=True), server_default=func.now(), primary_key=True)
    reason = Column("reason", String)
    params = Column("params", String)
    trace = Column("trace", String)

    __table_args__ = (
        {"extend_existing": True}
    )

class MacroData(Base):
    """모은 데이터를 저장하는 테이블"""

    __tablename__ = "gksc_s_macro_data_00"

    id = Column("id", String, primary_key=True)
    date = Column("date", String(8), primary_key=True)
    value = Column("value", Float)

    __table_args__ = (
        {"extend_existing": True}
    )