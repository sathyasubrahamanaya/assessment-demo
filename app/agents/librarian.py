from ctypes import Structure
from textwrap import dedent
from typing import List, Dict, Any
import json
from agno.agent import Agent
from agno.models.google import Gemini


from typing import List
from pydantic import BaseModel


class CaseStudyRecommendation(BaseModel):
    case_study_topic: str
    recommendation_score: str
    scoring_criteria: str


class CaseStudyRecommendations(BaseModel):
    recommendations: List[CaseStudyRecommendation]

def create_case_study_matcher():
    """
    Creates a CaseStudyMatcher agent that analyzes user profiles and recommends 
    relevant case studies with quantified relevance scores.
    """
    
    case_study_matcher = Agent(
        name="CaseStudyMatcher",
        model=Gemini(id='gemini-2.5-flash-preview-04-17'),
        structured_outputs=True,
        response_model=CaseStudyRecommendations,

        description=dedent("""\
            You are CaseStudyMatcher, an expert career advisor and case study analyst 
            who specializes in matching professionals with the most relevant case studies 
            based on their career profiles, skills, interests, and goals.
            
            Your mission is to analyze user career profiles and recommend case studies 
            that will provide maximum learning value and career advancement opportunities.
        """),
        instructions=dedent("""\
            Follow this systematic approach for case study recommendations:

            1. Profile Analysis Phase 📊
               - Extract key information from user's career profile
               - Identify core skills, interests, and career aspirations
               - Note personality traits and learning preferences
               - Assess current career stage and goals

            2. Case Study Assessment Phase 🔍
               - Evaluate each case study's topic and content
               - Assess target audience alignment
               - Determine career relevance and skill requirements
               - Consider learning outcomes and practical applications

            3. Relevance Scoring Phase 📈
               - Calculate alignment scores based on:
                 * Career relevance (60% weight)
                 * Skills alignment (60% weight)
                 * Interest match (60% weight)
                 * Target audience fit (90% weight)
               - Quantify scores as percentages (0-100%)
               - Prioritize practical applicability

            4. Output Generation Phase 📋
               - Return results as a JSON array
               - Include case study topic and recommendation score
               - Format scores as percentages (e.g., "93.35%")
               - Order by relevance score (highest first)

            Scoring Criteria:
            - 90-100%: Exceptional match - directly relevant to career goals
            - 80-89%: Strong match - highly relevant with good skill alignment
            - 70-79%: Good match - relevant with some skill overlap
            - 60-69%: Moderate match - some relevance but limited alignment
            - Below 60%: Low match - minimal relevance or alignment

            Always provide your final response as a valid JSON array in this exact format:
            [{"case_study_topic": "<topic name>", "recommendation_score": "<percentage>%","scoring_criteria":"<classfied_scoring>"}, ...]
        """),
        markdown=False,  # Disable markdown for clean JSON output
        show_tool_calls=False,
    )
    
    return case_study_matcher

# Example usage function
def match_case_studies(user_profile: Dict[str, Any], case_studies: List[Dict[str, Any]]) -> str:

    
    matcher = create_case_study_matcher()
    
    # Format the input for the agent
    input_message = f"""
    USER PROFILE:
    {json.dumps(user_profile, indent=2)}
    
    AVAILABLE CASE STUDIES:
    {json.dumps(case_studies, indent=2)}
    
    Please analyze this user's profile and recommend the most relevant case studies 
    with quantified relevance scores. Return your response as a JSON array.
    """
    
    # Get the recommendation
    response = matcher.run(input_message)
    return response.content


