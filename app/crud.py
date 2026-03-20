from sqlalchemy.orm import Session
from . import models, schemas


# -------------------------
# TEAM CRUD
# -------------------------

def create_team(db: Session, team: schemas.TeamCreate):
    existing_team = db.query(models.Team).filter(models.Team.name == team.name).first()
    if existing_team:
        return None

    db_team = models.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_teams(db: Session):
    return db.query(models.Team).all()


def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def update_team(db: Session, team_id: int, team: schemas.TeamCreate):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        for key, value in team.model_dump().items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
    return db_team


def delete_team(db: Session, team_id: int):
    db_team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
    return db_team


# -------------------------
# PLAYER CRUD
# -------------------------

def create_player(db: Session, player: schemas.PlayerCreate):
    team = db.query(models.Team).filter(models.Team.id == player.team_id).first()
    if not team:
        return None

    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_players(db: Session):
    return db.query(models.Player).all()


def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def update_player(db: Session, player_id: int, player: schemas.PlayerCreate):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        for key, value in player.model_dump().items():
            setattr(db_player, key, value)
        db.commit()
        db.refresh(db_player)
    return db_player


def delete_player(db: Session, player_id: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if db_player:
        db.delete(db_player)
        db.commit()
    return db_player


# -------------------------
# MATCH CRUD
# -------------------------

def create_match(db: Session, match: schemas.MatchCreate):
    if match.home_team_id == match.away_team_id:
        return "same_team"

    home_team = db.query(models.Team).filter(models.Team.id == match.home_team_id).first()
    away_team = db.query(models.Team).filter(models.Team.id == match.away_team_id).first()

    if not home_team or not away_team:
        return None

    db_match = models.Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def get_matches(db: Session):
    return db.query(models.Match).all()


def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()


def update_match(db: Session, match_id: int, match: schemas.MatchCreate):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match:
        for key, value in match.model_dump().items():
            setattr(db_match, key, value)
        db.commit()
        db.refresh(db_match)
    return db_match


def delete_match(db: Session, match_id: int):
    db_match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if db_match:
        db.delete(db_match)
        db.commit()
    return db_match


# -------------------------
# ANALYTICS
# -------------------------

def get_leaderboard(db: Session):
    teams = db.query(models.Team).all()
    matches = db.query(models.Match).filter(models.Match.status == "finished").all()

    table = {}

    for team in teams:
        table[team.id] = {
            "team_id": team.id,
            "team_name": team.name,
            "played": 0,
            "won": 0,
            "drawn": 0,
            "lost": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }

    for match in matches:
        home = table.get(match.home_team_id)
        away = table.get(match.away_team_id)

        if not home or not away:
            continue

        home["played"] += 1
        away["played"] += 1

        home["goals_for"] += match.home_score
        home["goals_against"] += match.away_score

        away["goals_for"] += match.away_score
        away["goals_against"] += match.home_score

        if match.home_score > match.away_score:
            home["won"] += 1
            home["points"] += 3
            away["lost"] += 1
        elif match.home_score < match.away_score:
            away["won"] += 1
            away["points"] += 3
            home["lost"] += 1
        else:
            home["drawn"] += 1
            away["drawn"] += 1
            home["points"] += 1
            away["points"] += 1

    for team in table.values():
        team["goal_difference"] = team["goals_for"] - team["goals_against"]

    leaderboard = sorted(
        table.values(),
        key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]),
        reverse=True,
    )

    return leaderboard

def get_team_stats(db: Session, team_id: int):
    team = db.query(models.Team).filter(models.Team.id == team_id).first()
    if not team:
        return None

    matches = db.query(models.Match).filter(
        (models.Match.home_team_id == team_id) |
        (models.Match.away_team_id == team_id)
    ).all()

    stats = {
        "team_id": team.id,
        "team_name": team.name,
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_difference": 0,
        "points": 0
    }

    for match in matches:
        stats["played"] += 1

        if match.home_team_id == team_id:
            gf = match.home_score
            ga = match.away_score
        else:
            gf = match.away_score
            ga = match.home_score

        stats["goals_for"] += gf
        stats["goals_against"] += ga

        if gf > ga:
            stats["won"] += 1
            stats["points"] += 3
        elif gf < ga:
            stats["lost"] += 1
        else:
            stats["drawn"] += 1
            stats["points"] += 1

    stats["goal_difference"] = stats["goals_for"] - stats["goals_against"]

    return stats

def get_player_stats(db: Session, player_id: int):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()
    if not player:
        return None

    appearances = player.appearances if player.appearances > 0 else 0

    goals_per_game = player.goals / appearances if appearances > 0 else 0
    assists_per_game = player.assists / appearances if appearances > 0 else 0

    return {
        "player_id": player.id,
        "full_name": player.full_name,
        "team_id": player.team_id,
        "goals": player.goals,
        "assists": player.assists,
        "appearances": player.appearances,
        "goals_per_game": round(goals_per_game, 2),
        "assists_per_game": round(assists_per_game, 2),
    }
    
def get_top_scorers(db: Session, limit: int = 10):
    players = (
        db.query(models.Player)
        .order_by(models.Player.goals.desc(), models.Player.assists.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "player_id": player.id,
            "full_name": player.full_name,
            "team_id": player.team_id,
            "goals": player.goals,
            "assists": player.assists,
            "appearances": player.appearances,
        }
        for player in players
    ]