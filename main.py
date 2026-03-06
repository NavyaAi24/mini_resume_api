from fastapi import FastAPI, UploadFile, File, Form
import sqlite3
import os

app = FastAPI()

# create resumes folder
if not os.path.exists("resumes"):
    os.makedirs("resumes")

# connect database
conn = sqlite3.connect("candidates.db", check_same_thread=False)
cursor = conn.cursor()

# create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates(
id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT,
experience INTEGER,
skills TEXT,
resume_file TEXT
)
""")

conn.commit()


# Upload candidate
@app.post("/upload")
def upload_candidate(
    full_name: str = Form(...),
    experience: int = Form(...),
    skills: str = Form(...),
    resume: UploadFile = File(...)
):

    file_path = f"resumes/{resume.filename}"

    with open(file_path, "wb") as f:
        f.write(resume.file.read())

    cursor.execute(
        "INSERT INTO candidates(full_name,experience,skills,resume_file) VALUES(?,?,?,?)",
        (full_name, experience, skills, file_path)
    )

    conn.commit()

    return {"message": "Candidate uploaded successfully"}


# List all candidates
@app.get("/candidates")
def list_candidates():

    cursor.execute("SELECT * FROM candidates")
    rows = cursor.fetchall()

    candidates = []

    for r in rows:
        candidates.append({
            "id": r[0],
            "full_name": r[1],
            "experience": r[2],
            "skills": r[3],
            "resume_file": r[4]
        })

    return candidates


# Get candidate by ID
@app.get("/candidates/{id}")
def get_candidate(id: int):

    cursor.execute("SELECT * FROM candidates WHERE id=?", (id,))
    r = cursor.fetchone()

    if r:
        return {
            "id": r[0],
            "full_name": r[1],
            "experience": r[2],
            "skills": r[3],
            "resume_file": r[4]
        }

    return {"message": "Candidate not found"}


# Delete candidate
@app.delete("/candidates/{id}")
def delete_candidate(id: int):

    cursor.execute("DELETE FROM candidates WHERE id=?", (id,))
    conn.commit()

    return {"message": "Candidate deleted"}