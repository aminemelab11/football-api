# ⚽ Football Performance & Match Statistics API

## 📌 Overview

This project is a RESTful API built using **FastAPI** that provides football data management and analytics.
It supports full CRUD operations for teams, players, and matches, along with analytical endpoints such as leaderboards and performance statistics.

The system is designed to simulate a real-world sports analytics platform.

---

## 🚀 Features

### 🔹 Core Functionality

- Manage **Teams** (Create, Read, Update, Delete)
- Manage **Players** (Create, Read, Update, Delete)
- Manage **Matches** (Create, Read, Update, Delete)

### 🔹 Analytics Endpoints

- 📊 League leaderboard (points, goal difference, ranking)
- 🏟️ Team performance statistics
- 👤 Player performance statistics
- ⚽ Top scorers ranking

### 🔹 Data Validation & Error Handling

- Prevent duplicate teams
- Ensure players belong to valid teams
- Prevent matches with identical teams
- Reject negative values (goals, assists, scores)
- Proper HTTP error responses (400, 404, 422)

---

## 🛠️ Tech Stack

- **Backend Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **API Docs:** Swagger UI

---

## 📂 Project Structure

```
app/
│── main.py        # API routes
│── models.py      # Database models
│── schemas.py     # Data validation schemas
│── crud.py        # Database logic
│── database.py    # DB connection
```

---

## ▶️ How to Run the Project

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd project-folder
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate environment

- Windows:

```bash
venv\Scripts\activate
```

- Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

### 6. Open API docs

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

### 🔹 Teams

- `POST /teams`
- `GET /teams`
- `GET /teams/{id}`
- `PUT /teams/{id}`
- `DELETE /teams/{id}`

### 🔹 Players

- `POST /players`
- `GET /players`
- `GET /players/{id}`
- `PUT /players/{id}`
- `DELETE /players/{id}`

### 🔹 Matches

- `POST /matches`
- `GET /matches`
- `GET /matches/{id}`
- `PUT /matches/{id}`
- `DELETE /matches/{id}`

### 🔹 Analytics

- `GET /analytics/leaderboard`
- `GET /analytics/team/{team_id}`
- `GET /analytics/player/{player_id}`
- `GET /analytics/top-scorers`

---

## 🧪 Example Request

### Create a Team

```json
{
  "name": "Arsenal",
  "country": "England",
  "city": "London",
  "founded_year": 1886,
  "stadium": "Emirates Stadium",
  "coach_name": "Mikel Arteta"
}
```

---

## 📊 Example Analytics Output

### Leaderboard Entry

```json
{
  "team_id": 1,
  "team_name": "Arsenal",
  "played": 3,
  "won": 2,
  "drawn": 0,
  "lost": 1,
  "goals_for": 5,
  "goals_against": 3,
  "goal_difference": 2,
  "points": 6
}
```

---

## 📌 Key Design Decisions

- Used **modular architecture** (separating routes, logic, models)
- Implemented **data validation at schema level**
- Designed **relational database structure**
- Added **analytics endpoints for real-world relevance**

---

## ⚠️ Limitations

- Uses SQLite (not scalable for large systems)
- No authentication system
- No real-time data integration

---

## 🔮 Future Improvements

- Add authentication (JWT)
- Integrate real football datasets
- Deploy API online (Render / Railway)
- Add advanced analytics (win probability, predictions)

---

## 👨‍💻 Author

Student coursework project – COMP3011 Web Services

---
