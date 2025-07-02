from pydantic import BaseModel,Field
from typing import List, Dict
from pydantic import BaseModel, Field

class Questions(BaseModel):
    question_type:str = Field(default=None,description="The type of question related career development")
    question:str = Field(description="questions related to career")
    answer:str = Field(description="Answer of the asked question")
    insight:str = Field(default=None,description="what is the insight of the answer for question with 10 words",max_length=200)

class InterviewDetail(BaseModel):
    candidate_id:str = Field(description="candidate id")
    candidate_session_id:str = Field(description="session of candidate ")
    questions_answers:list[Questions]



class DocumentSummary(BaseModel):
    """A high-level summary of the document."""
    overall_description: str = Field(
        ...,
        description="A high-level summary explaining the document's purpose, main argument, and overall significance in one or two sentences."
    )

class IdealReaderPersona(BaseModel):
    """Describes the ideal reader for the document."""
    short_description: str = Field(
        ...,
        description="Describes the ideal individual who would gain the most from reading this document, detailing their professional mindset and goals."
    )
    persona_archetype: str
    core_motivations: List[str]
    professional_goals: List[str]
    common_challenges: List[str]

class CareerPathways(BaseModel):
    """A breakdown of potential job roles related to the document."""
    short_description: str = Field(
        ...,
        description="A comprehensive breakdown of potential job roles across different organizational levels and functions."
    )
    direct_application_roles: List[str]
    strategy_and_leadership_roles: List[str]
    academic_and_research_roles: List[str]
    adjacent_and_support_roles: List[str]

class CareerRelevance(BaseModel):
    """Outlines professional applications and career pathways."""
    short_description: str = Field(
        ...,
        description="Outlines the specific professional applications and career pathways related to the document's content."
    )
    primary_career_group_focus: str
    career_pathways: CareerPathways
    professional_standards_alignment: str

class CognitiveProfile(BaseModel):
    """Analyzes the thinking style needed to understand the document."""
    short_description: str = Field(
        ...,
        description="Analyzes the type of thinking and mental frameworks needed to understand and apply the document's concepts."
    )
    cognitive_style: List[str]
    required_mental_models: List[str]
    level_of_abstraction: str

class PersonalitySkillFocus(BaseModel):
    """Details the skills and attributes developed by engaging with the document."""
    short_description: str = Field(
        ...,
        description="Details the cognitive capacities, skills, and personal attributes that are developed or required to fully engage with the document."
    )
    key_skills_and_competencies_developed: List[str]
    cognitive_profile: CognitiveProfile
    personality_traits_benefited: List[str]
    practical_application_of_skills: str

class TargetReader(BaseModel):
    """Defines the specific audience for the document."""
    short_description: str = Field(
        ...,
        description="Defines the specific audience for the document, including their professional and demographic characteristics."
    )
    primary_audience: str
    level_of_expertise_assumed: str
    age_group: str
    gender: str
    prerequisites_for_optimal_comprehension: str
    call_to_action_for_audience: str

class EnhancedDocumentInsights(BaseModel):
    """Provides a deep and comprehensive analysis of the document."""
    short_description: str = Field(
        ...,
        description="Provides a deep and comprehensive analysis of the document's content, methodology, and implications."
    )
    comprehensive_summary_of_key_arguments: str
    central_concepts_explained: Dict[str, str] = Field(
        ...,
        description="An explanation of the core ideas, theories, or frameworks presented in the document."
    )
    methodology_critical_analysis: str
    practical_implications: str
    theoretical_contributions: str
    future_research_directions: str
    ethical_considerations: str

class CareerAnalysisReport(BaseModel):
    """The root model for a complete analysis of a document."""
    document_title: str
    document_summary: DocumentSummary
    ideal_reader_persona: IdealReaderPersona
    career_relevance: CareerRelevance
    personality_skill_focus: PersonalitySkillFocus
    target_reader: TargetReader
    enhanced_document_insights: EnhancedDocumentInsights




    
    