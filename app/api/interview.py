from fastapi import APIRouter
from app.agents.career_guide import interview_workflow
from app.agents.career_guide import career_compass_workflow
from typing import Dict, Any,List
from app.agents.librarian import match_case_studies

interview_router = APIRouter(prefix="/interview")

@interview_router.get("/interact")
def interact_with_agent(input_text: str):
    """
    Interact with the interview agent using the provided input text.
    """
    response = interview_workflow(input_text)
    return {"response": response}

@interview_router.get("/getCareerReport")
def get_career_report(user_profile: Dict[str, Any], question_history: List[Dict[str, Any]]):
    """
    Get a career report for the user based on their profile.
    """
    # Convert user_profile dict to string representation
    profile_summary = str(user_profile)
    response = career_compass_workflow(profile_summary, question_history)
    return {"response": response}

@interview_router.get("/matchCaseStudies")
def match_case_studies_endpoint(user_profile: Dict[str, Any], case_studies: List[Dict[str, Any]]):
    """
    Match case studies to the user's profile and return relevant recommendations.
    """
    response = match_case_studies(user_profile, case_studies)
    return {"response": response}