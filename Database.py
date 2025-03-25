from sqlalchemy import Column, Float, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid
import os

# Define base for ORM
Base = declarative_base()

class SimulationParameters(Base):
    __tablename__ = "simulation_parameters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project_name = Column(String, nullable=False)

    ls = Column(Float)
    hs = Column(Float)
    t = Column(Float)
    gc = Column(Float)

    l1 = Column(Float)
    ed1 = Column(Float)
    id1 = Column(Float)

    l2 = Column(Float)
    ed2 = Column(Float)
    id2 = Column(Float)

    # S-parameter scalar values
    s11_freq = Column(Float)
    s11_db = Column(Float)
    s21_freq = Column(Float)
    s21_db = Column(Float)

# SQLite DB setup
db_path = os.path.join(os.path.dirname(__file__), "simulation.db")
engine = create_engine(f"sqlite:///{db_path}")
SessionLocal = sessionmaker(bind=engine)

# Initialize DB and create tables
def init_db():
    Base.metadata.create_all(bind=engine)


def save_simulation_parameters(params: dict):
    session = SessionLocal()
    try:
        sim = SimulationParameters(**params)
        session.add(sim)
        session.commit()
        print("Saved successfully!")
    except Exception as e:
        session.rollback()
        print("Error saving:", e)
    finally:
        session.close()


init_db()