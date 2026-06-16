# SECTION 1: Imports
from app.database.session import Base, SessionLocal, engine
from app.services.roster_service import RosterService


# SECTION 2: Main Build Function
def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        service = RosterService(db)
        result = service.sync_teams_and_rosters(season=2026)
        print(result)
    finally:
        db.close()


# SECTION 3: Script Entrypoint
if __name__ == "__main__":
    main()
