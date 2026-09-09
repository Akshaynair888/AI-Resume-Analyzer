# AI Resume Analyzer & Job Matcher

An AI-powered web application that analyzes resumes against job descriptions and provides skill matching, semantic similarity, skill gaps, relevant experience, and recommendations.

## Features

- Upload resume in PDF format
- Extract resume text automatically
- Detect technical skills using pattern matching
- Identify matched and missing skills
- Calculate skill-match score
- Calculate semantic similarity between resume and job description
- Generate an overall compatibility score
- Identify relevant resume experience
- Provide AI-based recommendations using local NLP logic
- Store analysis results in MySQL
- View previous analyses through analysis history
- REST API for analysis data
- Input validation for file type, file size, and job description

## Technology Stack

### Backend
- Python
- Django
- Django REST Framework

### Database
- MySQL

### AI / NLP
- Sentence Transformers
- `all-MiniLM-L6-v2`
- Semantic similarity
- Pattern-based skill extraction

### Frontend
- HTML
- CSS
- JavaScript

### Tools
- Git
- GitHub
- VS Code

## How It Works

1. User uploads a resume PDF.
2. The application extracts the resume text.
3. User provides a job description.
4. Required technical skills are identified.
5. Resume skills are compared with the job requirements.
6. Semantic similarity is calculated using sentence embeddings.
7. Relevant experience is identified from the resume.
8. Skill gaps and recommendations are generated.
9. The analysis is stored in MySQL.
10. Previous analyses can be viewed through the history section.

## Scoring

The application combines two signals:

- Skill Match: 60%
- Semantic Similarity: 40%

The final score is calculated from these two components to provide an overall resume-job compatibility score.

> Note: The scoring system is a project-specific heuristic and is not intended to represent an actual hiring decision.

## Project Structure

```text
AI_RESUME_ANALYZER/
├── analyzer/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── uploads/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── .gitignore
├── manage.py
└── README.md