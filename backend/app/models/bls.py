from sqlalchemy import Column, Integer, String, Float, Date, Table, MetaData
from app.db.session import Base

metadata = MetaData()

# Define the existing tables
bls_combined_data = Table(
    "bls_combined_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("series", String, index=True),
    Column("year", Integer, index=True),
    Column("M01", Float, nullable=True),
    Column("M02", Float, nullable=True),
    Column("M03", Float, nullable=True),
    Column("M04", Float, nullable=True),
    Column("M05", Float, nullable=True),
    Column("M06", Float, nullable=True),
    Column("M07", Float, nullable=True),
    Column("M08", Float, nullable=True),
    Column("M09", Float, nullable=True),
    Column("M10", Float, nullable=True),
    Column("M11", Float, nullable=True),
    Column("M12", Float, nullable=True),
    Column("yoy_change", Float, nullable=True),
    Column("last_updated", Date, nullable=True)
)

bls_summary_data = Table(
    "bls_summary_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("series", String, index=True),
    Column("year", Integer, index=True),
    Column("month", String, index=True),
    Column("value", Float, nullable=True),
    Column("yoy_change", Float, nullable=True),
    Column("mom_change", Float, nullable=True),
    Column("sentiment", String, nullable=True),
    Column("last_updated", Date, nullable=True)
)

class BlsData(Base):
    __tablename__ = "bls_combined_data"

    id = Column(Integer, primary_key=True, index=True)
    series = Column(String, index=True)
    year = Column(Integer, index=True)
    M01 = Column(Float, nullable=True)
    M02 = Column(Float, nullable=True)
    M03 = Column(Float, nullable=True)
    M04 = Column(Float, nullable=True)
    M05 = Column(Float, nullable=True)
    M06 = Column(Float, nullable=True)
    M07 = Column(Float, nullable=True)
    M08 = Column(Float, nullable=True)
    M09 = Column(Float, nullable=True)
    M10 = Column(Float, nullable=True)
    M11 = Column(Float, nullable=True)
    M12 = Column(Float, nullable=True)
    yoy_change = Column(Float, nullable=True)
    last_updated = Column(Date, nullable=True) 