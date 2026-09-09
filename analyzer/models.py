from django.db import models


class ResumeAnalysis(models.Model):
    resume_name = models.CharField(max_length=255)
    resume_text = models.TextField()
    job_description = models.TextField()

    match_score = models.FloatField(null=True, blank=True)
    semantic_score = models.FloatField(null=True, blank=True)
    overall_score = models.FloatField(null=True, blank=True)

    matched_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    ai_analysis = models.TextField(blank=True)
    relevant_experience = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resume_name