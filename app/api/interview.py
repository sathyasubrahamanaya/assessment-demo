from fastapi import APIRouter
from app.agents.career_guide import interview_workflow
from app.agents.career_guide import career_compass_workflow
from typing import Dict, Any,List
from app.agents.librarian import match_case_studies
from app.api.doc_handler import doc_list,get_doc_list
from app.agents.career_guide import profile_summary,questions_and_insights
from app.agents.career_guide import CareerCompassResponse
from typing import Optional







interview_router = APIRouter(prefix="/interview")


user_refined_profile:Optional[Dict[str, Any]] = None
intermediate_profile: str = ""
intermediate_questions_and_insights:str = ""

@interview_router.get("/interact")
def interact_with_agent(input_text: str):
    """
    Interact with the interview agent using the provided input text.
    """
    response = interview_workflow(input_text)
    print("--------------------------\n\n\n profile_summary111"+str(profile_summary))
    print("-------------------------\n\n\nquestions_and_insights111"+str(questions_and_insights))
    global intermediate_profile, intermediate_questions_and_insights
    intermediate_profile = str(profile_summary)
    intermediate_questions_and_insights = str(questions_and_insights)
    print("interviewresponse"+str(response))
    return {"response": response}

@interview_router.get("/getCareerReport")
def get_career_report(user_profile: Any = profile_summary, question_history: List[Dict[str, Any]] = questions_and_insights):
    """
    Get a career report for the user based on their profile.
    """
    # Convert user_profile dict to string representation
    profile_summary = str(user_profile)
    response = career_compass_workflow(profile_summary, question_history)
    global user_refined_profile
    user_refined_profile = response
    return response

@interview_router.get("/matchCaseStudies")
def match_case_studies_endpoint():
    """
    Match case studies to the user's profile and return relevant recommendations.
    """
    # Get the document list
    doc_response = get_doc_list()
    
    # Check if we have documents
    if not doc_response or "documents" not in doc_response or not doc_response["documents"]:
        return {"response": [], "message": "No case studies available for matching"}
    
    # Get user profile
    user_profile = get_career_report(profile_summary, questions_and_insights)

    print("user_profile222"+str(user_profile))
    print("case_studies"+str(doc_response["documents"]))
    
    # Ensure documents is a list of dictionaries
    case_studies = doc_response["documents"]
    if isinstance(case_studies, list):
        response = match_case_studies(user_profile, case_studies)
        return {"response": response}
    else:
        return {"response": [], "message": "Invalid document format"}