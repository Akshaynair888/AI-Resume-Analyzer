from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ResumeAnalysisSerializer
from .models import ResumeAnalysis
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import ResumeAnalysis
from .utils import (
    extract_text_from_pdf,
    calculate_match_score,
    find_skills,
    calculate_semantic_score,
    calculate_overall_score,
    generate_ai_analysis,
    find_relevant_experience,
)

def upload_resume(request):
    extracted_text = None
    job_description = None
    match_score = None
    semantic_score= None
    overall_score= None
    ai_analysis = None
    matched_skills = []
    missing_skills = []
    relevant_experience = []

    if request.method == "POST":
        resume_file = request.FILES.get("resume")
        job_description = request.POST.get("job_description")

        if resume_file and not resume_file.name.lower().endswith(".pdf"): 
            messages.error(request, "Please upload a PDF file.")
            resume_file = None

        if resume_file and resume_file.size > 5 * 1024 * 1024:
            messages.error(request, "Resume file must be smaller than 5 MB.")
            resume_file = None

        if resume_file and not job_description.strip():
            messages.error(request, "Please enter a job description.")

        if resume_file and job_description:
            extracted_text = extract_text_from_pdf(resume_file)

            match_score = calculate_match_score(
                extracted_text,
                job_description
            )
            semantic_score = calculate_semantic_score(
                extracted_text,
                job_description
            )
            overall_score = calculate_overall_score(
                match_score,
                semantic_score
            )
            matched_skills, missing_skills = find_skills(
                extracted_text,
                job_description
            )
            ai_analysis = generate_ai_analysis(
                extracted_text,
                job_description,
                matched_skills,
                missing_skills
            )
            relevant_experience = find_relevant_experience(
                extracted_text,
                job_description
            )
            ResumeAnalysis.objects.create(
            resume_name=resume_file.name,
            resume_text=extracted_text,
            job_description=job_description,
            match_score=match_score,
            semantic_score=semantic_score,
            overall_score=overall_score,
            matched_skills=", ".join(matched_skills),
            missing_skills=", ".join(missing_skills),
            ai_analysis=str(ai_analysis),
            relevant_experience="\n".join(relevant_experience),
            )

    return render(
        request,
        "analyzer/upload.html",
        {
            "extracted_text": extracted_text,
            "job_description": job_description,
            "match_score": match_score,
            "semantic_score": semantic_score,
            "overall_score": overall_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "ai_analysis": ai_analysis,
            "relevant_experience": relevant_experience,
        }
    )
def analysis_history(request):
    analyses = ResumeAnalysis.objects.all().order_by("-created_at")

    return render(
        request,
        "analyzer/history.html",
        {
            "analyses": analyses
        }
    )

def analysis_detail(request, analysis_id):
    analysis = ResumeAnalysis.objects.get(id=analysis_id)

    return render(
        request,
        "analyzer/detail.html",
        {
            "analysis": analysis
        }
    )

@api_view(["GET"])
def analysis_api(request):
    analyses = ResumeAnalysis.objects.all().order_by("-created_at")
    serializer = ResumeAnalysisSerializer(analyses, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def analysis_detail_api(request, analysis_id):
    analysis = get_object_or_404(ResumeAnalysis, id=analysis_id)
    serializer = ResumeAnalysisSerializer(analysis)

    return Response(serializer.data)