from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import shutil

app = FastAPI()

# Store candidates in memory (simple list)
candidates = []
current_id = 1

# Create resumes folder if it does not exist
if not os.path.exists("resumes"):
    os.makedirs("resumes")


# 1️. Upload Candidate
@app.post("/upload")
def upload_candidate(
    full_name: str = Form(...),
    dob: str = Form(...),
    contact_number: str = Form(...),
    contact_address: str = Form(...),
    education: str = Form(...),
    graduation_year: int = Form(...),
    experience: int = Form(...),
    skills: str = Form(...),
    resume: UploadFile = File(...)
):
    global current_id

    file_path = f"resumes/{resume.filename}"

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    # Create candidate dictionary
    candidate = {
        "id": current_id,
        "full_name": full_name,
        "dob": dob,
        "contact_number": contact_number,
        "contact_address": contact_address,
        "education": education,
        "graduation_year": graduation_year,
        "experience": experience,
        "skills": skills,
        "resume_file": file_path
    }

    candidates.append(candidate)
    current_id += 1

    return {
        "message": "Candidate uploaded successfully",
        "candidate": candidate
    }


# 2️. List Candidates (with optional filters)
@app.get("/candidates")
def list_candidates(
    skill: str = None,
    experience: int = None,
    graduation_year: int = None
):
    results = candidates

    if skill:
        results = [c for c in results if skill.lower() in c["skills"].lower()]

    if experience:
        results = [c for c in results if c["experience"] == experience]

    if graduation_year:
        results = [c for c in results if c["graduation_year"] == graduation_year]

    return results


# 3️. Get Candidate by ID
@app.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int):
    for candidate in candidates:
        if candidate["id"] == candidate_id:
            return candidate

    raise HTTPException(status_code=404, detail="Candidate not found")


# 4️. Delete Candidate
@app.delete("/candidates/{candidate_id}")
def delete_candidate(candidate_id: int):
    global candidates

    for candidate in candidates:
        if candidate["id"] == candidate_id:
            candidates.remove(candidate)
            return {"message": "Candidate deleted successfully"}

    raise HTTPException(status_code=404, detail="Candidate not found")
