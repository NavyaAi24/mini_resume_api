# Mini Resume Management API

## Objective
A REST API built with FastAPI to upload, manage, and search candidate resumes efficiently.

## Features
- Upload resumes in PDF, DOC, or DOCX formats
- Store candidate details including name, DOB, contact info, education, experience, and skills
- Categorize candidates by technology and years of experience
- List, search, and delete candidates via API
- **Store collected resume data in a database (any relational or NoSQL database of your choice)**
- **Ensure the application can successfully save the submitted data and retrieve it when required**

## API Endpoints

### 1. Upload Resume
**POST /candidates/**  
Request body includes:
- Full Name
- DOB
- Contact Number
- Address
- Education Qualification
- Graduation Year
- Years of Experience
- Skill Set
- Resume file (PDF/DOC/DOCX)

### 2. List Candidates
**GET /candidates/**  
Filter by:
- Skill  
- Years of Experience  
- Graduation Year  

### 3. Get Candidate by ID
**GET /candidates/{id}**

### 4. Delete Candidate
**DELETE /candidates/{id}**

## Installation
```bash
git clone <your-repo-url>
cd resume-management-api
pip install -r requirements.txt
uvicorn main:app --reload