# Python-based Habit Tracker

## Goals
- Track tasks, date completed
- User interface
    - Log in, simple account handling
    - See a list of tracked tasks/habits
    - CRUD for habits/tasks
    - Daily habit logging (option to enter a date)
    - Visualization options: TBD

## Stretch Features
- Streak counting
- Point scoring
    - Allow habits/tasks to be given a "reward value" -> Excercise gives 5 points
    - Allow users to enter reward info and "cost" -> Dine out somewhere nice for 50 points
- Categories or tagging
- Export as CSV

## Tech Stack
- Backend: FastAPI
- Database: SQLite + SQLAlchemy ORM.
- Frontend: FastAPI → JSON API + small frontend (HTMX, Vue, or just HTML/JS).
- Auth: FastAPI Users
- Visualization: Chart.js