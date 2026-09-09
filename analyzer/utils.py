import re
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text

def calculate_match_score(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    required_skills = []

    for skill in TECHNICAL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, job_description):
            required_skills.append(skill)

    if not required_skills:
        return 0

    matched_skills = []

    for skill in required_skills:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, resume_text):
            matched_skills.append(skill)

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score, 2)

TECHNICAL_SKILLS = [
    "python",
    "django",
    "django rest framework",
    "rest api",
    "sql",
    "mysql",
    "html",
    "css",
    "javascript",
    "react",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "numpy",
    "pandas",
    "scikit-learn",
    "generative ai",
    "llm",
    "prompt engineering",
    "docker",
    "aws",
    "kubernetes",
]
model = SentenceTransformer("all-MiniLM-L6-v2")

def find_skills(resume_text, job_description):
    resume_text = resume_text.lower()
    job_description = job_description.lower()

    matched_skills = []
    missing_skills = []

    for skill in TECHNICAL_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, job_description):

            if re.search(pattern, resume_text):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    return matched_skills, missing_skills


def calculate_semantic_score(resume_text, job_description):
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    job_embedding = model.encode(job_description, convert_to_tensor=True)

    similarity = util.cos_sim(resume_embedding, job_embedding)

    score = float(similarity[0][0]) * 100

    return round(score, 2)

def calculate_overall_score(skill_score, semantic_score):
    overall_score = (skill_score * 0.60) + (semantic_score * 0.40)

    return round(overall_score, 2)

def generate_ai_analysis(resume_text, job_description, matched_skills, missing_skills):
    analysis = {
        "strengths": matched_skills,
        "skill_gaps": missing_skills,
        "recommendations": []
    }

    if missing_skills:
        for skill in missing_skills:
            analysis["recommendations"].append(
                f"Consider learning or improving {skill} because it is required by the job description."
            )
    else:
        analysis["recommendations"].append(
            "Your resume contains all the technical skills identified in the job description."
        )

    return analysis

def find_relevant_experience(resume_text, job_description):
    sentences = resume_text.replace("\n", ".").split(".")

    cleaned_sentences = []

    for sentence in sentences:
        sentence = sentence.strip()

        # Remove common bullet characters extracted from PDFs
        sentence = re.sub(r'[•●▪◦\uf0b7\uf0a7]', '', sentence)

        # Remove extra spaces
        sentence = sentence.strip()

        if len(sentence) > 30:cleaned_sentences.append(sentence)

    sentences = cleaned_sentences

    if not sentences:
        return []

    resume_embeddings = model.encode(
        sentences,
        convert_to_tensor=True
    )

    job_embedding = model.encode(
        job_description,
        convert_to_tensor=True
    )

    similarities = util.cos_sim(
        resume_embeddings,
        job_embedding
    ).squeeze()

    ranked_sentences = sorted(
        zip(sentences, similarities),
        key=lambda x: float(x[1]),
        reverse=True
    )

    return [
        sentence
        for sentence, score in ranked_sentences[:5]
    ]