from django.test import TestCase
from .utils import ( calculate_overall_score, find_skills, extract_text_from_pdf, calculate_semantic_score, generate_ai_analysis )


class OverallScoreTest(TestCase):

    def test_overall_score(self):
        result = calculate_overall_score(80, 60)
        self.assertEqual(result, 72)

        result = calculate_overall_score(100, 100)
        self.assertEqual(result, 100)

        result = calculate_overall_score(0, 0)
        self.assertEqual(result, 0)

class FindSkillsTest(TestCase):

    def test_find_skills(self):
        resume = "I have experience with Python, Django and MySQL."
        job = "Looking for a Python Django developer with MySQL and AWS."

        matched, missing = find_skills(resume, job)

        self.assertIn("python", matched)
        self.assertIn("django", matched)
        self.assertIn("mysql", matched)
        self.assertIn("aws", missing)

    def test_missing_skill(self):
        resume = "I have experience with Python and Django."
        job = "Looking for Python Django and AWS experience."

        matched, missing = find_skills(resume, job)

        self.assertIn("python", matched)
        self.assertIn("django", matched)
        self.assertIn("aws", missing)

class ExtractTextTest(TestCase):

    def test_extract_text_from_pdf(self):
        from unittest.mock import patch, MagicMock

        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Python Django Developer"

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]

        with patch("analyzer.utils.PdfReader", return_value=mock_reader):
            result = extract_text_from_pdf("dummy.pdf")

        self.assertIn("Python Django Developer", result)

class SemanticScoreTest(TestCase):

    def test_semantic_score(self):
        resume = "Python Django developer with experience building web applications."
        job = "Looking for a Python Django developer to build web applications."

        score = calculate_semantic_score(resume, job)

        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)

class AIAnalysisTest(TestCase):

    def test_ai_analysis_with_missing_skills(self):
        matched = ["python", "django"]
        missing = ["aws", "docker"]

        result = generate_ai_analysis(
            "Python Django developer",
            "Looking for Python Django AWS Docker developer",
            matched,
            missing
        )

        self.assertIn("python", result["strengths"])
        self.assertIn("aws", result["skill_gaps"])
        self.assertIn("docker", result["skill_gaps"])
        self.assertGreater(len(result["recommendations"]), 0)