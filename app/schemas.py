from pydantic import BaseModel, Field


class TeamBase(BaseModel):
    name: str
    country: str
    city: str
    founded_year: int
    stadium: str
    coach_name: str


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        from_attributes = True


class PlayerBase(BaseModel):
    full_name: str
    age: int
    nationality: str
    position: str
    shirt_number: int
    team_id: int
    goals: int = Field(0, ge=0)
    assists: int = Field(0, ge=0)
    appearances: int = Field(0, ge=0)


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int

    class Config:
        from_attributes = True


class MatchBase(BaseModel):
    home_team_id: int
    away_team_id: int
    match_date: str
    competition: str
    home_score: int = Field(0, ge=0)
    away_score: int = Field(0, ge=0)
    venue: str
    status: str


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    team_id: int
    team_name: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int


class TeamStats(BaseModel):
    team_id: int
    team_name: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int


class PlayerStats(BaseModel):
    player_id: int
    full_name: str
    team_id: int
    goals: int
    assists: int
    appearances: int
    goals_per_game: float
    assists_per_game: float


class TopScorerEntry(BaseModel):
    player_id: int
    full_name: str
    team_id: int
    goals: int
    assists: int
    appearances: int