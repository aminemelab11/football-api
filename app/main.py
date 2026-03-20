from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal
from . import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Football API is running ⚽"}


# -------------------------
# TEAM ENDPOINTS
# -------------------------

@app.post("/teams", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.create_team(db=db, team=team)
    if db_team is None:
        raise HTTPException(status_code=400, detail="Team with this name already exists")
    return db_team


@app.get("/teams", response_model=list[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    return crud.get_teams(db)


@app.get("/teams/{team_id}", response_model=schemas.Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@app.put("/teams/{team_id}", response_model=schemas.Team)
def update_team(team_id: int, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = crud.update_team(db, team_id, team)

    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    if db_team == "duplicate_name":
        raise HTTPException(status_code=400, detail="Another team with this name already exists")

    return db_team


@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    db_team = crud.delete_team(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team deleted successfully"}


# -------------------------
# PLAYER ENDPOINTS
# -------------------------

@app.post("/players", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.create_player(db, player)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Team not found for this player")
    return db_player


@app.get("/players", response_model=list[schemas.Player])
def read_players(db: Session = Depends(get_db)):
    return crud.get_players(db)


@app.get("/players/{player_id}", response_model=schemas.Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.get_player(db, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@app.put("/players/{player_id}", response_model=schemas.Player)
def update_player(player_id: int, player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = crud.update_player(db, player_id, player)

    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    if db_player == "team_not_found":
        raise HTTPException(status_code=404, detail="Team not found for this player")

    return db_player


@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    db_player = crud.delete_player(db, player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player deleted successfully"}


# -------------------------
# MATCH ENDPOINTS
# -------------------------

@app.post("/matches", response_model=schemas.Match)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = crud.create_match(db, match)

    if db_match == "same_team":
        raise HTTPException(status_code=400, detail="Home team and away team must be different")

    if db_match is None:
        raise HTTPException(status_code=404, detail="One or both teams not found")

    return db_match


@app.get("/matches", response_model=list[schemas.Match])
def read_matches(db: Session = Depends(get_db)):
    return crud.get_matches(db)


@app.get("/matches/{match_id}", response_model=schemas.Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = crud.get_match(db, match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@app.put("/matches/{match_id}", response_model=schemas.Match)
def update_match(match_id: int, match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = crud.update_match(db, match_id, match)

    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")

    if db_match == "same_team":
        raise HTTPException(status_code=400, detail="Home team and away team must be different")

    if db_match == "team_not_found":
        raise HTTPException(status_code=404, detail="One or both teams not found")

    return db_match


@app.delete("/matches/{match_id}")
def delete_match(match_id: int, db: Session = Depends(get_db)):
    db_match = crud.delete_match(db, match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"message": "Match deleted successfully"}


# -------------------------
# ANALYTICS ENDPOINTS
# -------------------------

@app.get("/analytics/leaderboard", response_model=list[schemas.LeaderboardEntry])
def leaderboard(db: Session = Depends(get_db)):
    return crud.get_leaderboard(db)


@app.get("/analytics/team/{team_id}", response_model=schemas.TeamStats)
def team_stats(team_id: int, db: Session = Depends(get_db)):
    stats = crud.get_team_stats(db, team_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return stats


@app.get("/analytics/player/{player_id}", response_model=schemas.PlayerStats)
def player_stats(player_id: int, db: Session = Depends(get_db)):
    stats = crud.get_player_stats(db, player_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return stats


@app.get("/analytics/top-scorers", response_model=list[schemas.TopScorerEntry])
def top_scorers(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_scorers(db, limit)