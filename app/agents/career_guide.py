from agno.agent import Agent
from agno.models.google import Gemini
from agno.memory.v2 import Memory
from agno.models.google import Gemini
from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools
from pydantic import BaseModel, Field

from typing import Dict, Any
from agno.agent import Agent
from agno.models.google import Gemini



from typing import List, Optional
from pydantic import BaseModel, Field

# Initialize the model
model = Gemini()

# Global profile state
profile_summary = ""

# Tool: update the profile with new information
def update_profile_information(new_info: str):
    print("this tool is calling")
    global profile_summary
    profile_summary += f"\n{new_info}"
    return f"updated profile summary:\n{profile_summary}"

# Tool: retrieve current collected profile info
def get_complete_profile():
    print("fetching collected profile")
    return profile_summary

# Instructions to guide the agent
instructions = """
**Persona:** You are 'PathFinder', an expert and friendly AI career counsellor. Your goal is to collect user details needed to build the following JSON profile. Use friendly and professional tone, always ask questions based on fields below.

**Your Only Goal:** Collect and maintain the following JSON structure. Never ask for anything outside this structure.


{
  "personalInfo": {
    "fullName": "...",
    "location": "..."
  },
  "education": {
    "highestLevelCompleted": "...",
    "major": "...",
    "institution": "...",
    "graduationYear": 0,
    "relevantCoursework": [] about any related courses with deegree or high school are done,
    "academicProjects": "[],ask 2-3 questions about it and add to list one by one"
  },
  "relevantExperience": [
    {
      "type": "Internship | Part-time | Volunteer | Project | None",
      "role": "...",
      "company": "...",
      "keyLearnings": "..."
    }
  ],
  "careerAspirations": {

    "targetRolesOrIndustries": [],

  },
  "selfAssessment": {

    "interests": [] interests related to subjects,hobby,

  }

}

Conversation Flow:
Start by greeting and ask for fullName.

Use get_complete_profile() before each question to recall progress.

After each user response, use update_profile_information() to store it.

One question at a time, following JSON schema order.

For experience: if user says "None", store:

{"type":"None","role":"N/A","company":"N/A","keyLearnings":"N/A"}
For list fields, ask for comma-separated values and store as list.

Once all fields are filled and confirmed, respond with PROFILE_COLLECTED.

"""



profile_collector = Agent(
model=model,
name="PathFinder",
goal="Collect complete student profile",
description="Friendly and professional AI assistant that builds a structured profile. Always get latest profile using get_complete_profile and update each new data using update_profile_information. End with PROFILE_COLLECTED.",
tools=[update_profile_information, get_complete_profile],
instructions=instructions,
add_history_to_messages=True,
num_history_responses=3
)





# Session-level variables
profile_info = profile_summary
questions_and_insights = []
question_count = 0

# Define tools

def get_question_count():
    global question_count
    print("calling get_question_count")
    return f"courrent question count is {question_count}"

def update_question_count():
    global question_count
    question_count += 1
    print("calling update_question_count")
    return f"question count updated {question_count}"

def get_profile_summary():
    global profile_info
    print("calling get_profile_summary")
    return f"the user profile info {profile_info}"

def map_and_add_tool(new_insight: dict):
    questions_and_insights.append(new_insight)
    print("calling map_and_add_tool")
    return {"status": "success", "insights_count": len(questions_and_insights)}

def get_question_history():
    global questions_and_insights
    print("calling get_question_history")
    return questions_and_insights

# Agent description
agent_description = f"""
You are **Pathfinder**, an AI-powered career guidance assistant helping students and early professionals explore career paths by understanding their interests and personality.
User profile:
{profile_summary}
"""

# Agent instructions

agent_instructions = """
You are **Pathfinder**, an expert AI career guide. Your mission is to help users discover ideal career paths by engaging them in an intelligent, structured interview.

You will conduct a conversation with a maximum of 15 questions, dynamically generated based on user responses. Each question must be either:

1. **Scale-Based (1–5)**
2. **Multiple Choice (A–D)** — You may include options like "None" or "N/A" when appropriate, especially for simpler questions with only A or B options.

Your questioning logic should:

- Blend **Big Five**, **MBTI**, and **STEM/Non-STEM/Career/Interest-based** content.
- Reference both the **user's profile** (`get_profile_summary`) and **previous questions** (`get_question_history`) before generating new ones.
- Adjust questions based on STEM or Non-STEM background.
- Assess soft skills (e.g., communication, creativity, resilience) **implicitly**, without directly stating them.

---

### 🔍 Context-Aware Strategy

- Always call `get_question_history()` to avoid repeating past questions.
- Always use `get_profile_summary()` before generating each question.
- Track progress with `get_question_count()` and increment via `update_question_count()`.

After each user response:
- Use `map_and_add_tool()` to record the answer and mapped traits.

---

### 🛠️ Tool Call Format

```python
map_and_add_tool({
  "Category": "Conscientiousness",
  "Mapped Trait/Skill": "Organization",
  "Career Hints": ["Project Manager", "Accountant"],
  "Question": "I enjoy planning tasks.",
  "Low Scale Skill": "Spontaneity",
  "Low Scale Career Hint": ["Artist"],
  "Medium Scale Skill": "Balanced Planning",
  "Medium Scale Career Hint": ["Teacher"],
  "High Scale Skill": "Meticulous Planning",
  "High Scale Career Hint": ["Data Analyst"],
  "Option A Skill": "N/A",
  "Option A Career Hint": "N/A",
  "Option B Skill": "N/A",
  "Option B Career Hint": "N/A",
  "Option C Skill": "N/A",
  "Option C Career Hint": "N/A",
  "Option D Skill": "N/A",
  "Option D Career Hint": "N/A"
})
```

---

### 🔹 Required Output Format
Respond only in this format:


{
  "question": "Question to ask",
  "question_type": "Type: scale or mcq",
  "process_completed": true or false
}


🚫 Do not add anything outside this  format.
"""


# Output structure
class CareerOutputModel(BaseModel):
    question: str = Field(description="Question to ask")
    question_type: str = Field(description="Type: scale or mcq")
    process_completed: bool = Field(description="Whether the interview is completed")

# Agent creation
interview_agent = Agent(
    model=Gemini(id= 'gemini-2.5-flash-lite-preview-06-17'),
    name="Pathfinder",
    goal="Career Advice",
    add_history_to_messages=True,
    num_history_responses=3,
    description=agent_description,
    instructions=agent_instructions,
    tools=[get_profile_summary, get_question_count, update_question_count, map_and_add_tool, get_question_history],
   
    show_tool_calls=True,
   
)




# Agent metadata
parser_description = """
You are an AI parser that converts raw user responses or agent outputs into a structured CareerOutputModel.
This format is used to represent the current state of a question and whether the process is completed.

"""

parser_instructions = """
Read the input carefully and convert it into the exact fields of CareerOutputModel:
- question: the full question text
- question_type: either 'scale' or 'mcq'
- process_completed: true if the interview process is complete, false otherwise

You must output only a valid CareerOutputModel-compatible dictionary. Do not include any explanations or extra text.
"""

# Create the parser agent
career_output_parser_agent = Agent(
    model=Gemini(),
    description=parser_description,
    instructions=parser_instructions,
    response_model=CareerOutputModel,
    structured_outputs=True
)

profile_completed = False
def interview_workflow(input_text:str):
    global profile_completed
    if not profile_completed:
        response = profile_collector.run(input_text)
        if "PROFILE_COLLECTED" in response.content:
            profile_completed = True
            return {"status": "success", "message": "Profile collection completed."}
        else:
            return {"status": "in_progress", "response": response.content, "input_type": "user_input"}
    else:
        response = interview_agent.run(input_text)
        response_json:CareerOutputModel = career_output_parser_agent.run(response.content)
        return {"status": "interview_completed", "response": response_json.model_dump(), "input_type": "scale/mcq"}


  
    



# Individual component models
class Persona(BaseModel):
    name: Optional[str] = Field(None, description="User's full name from profile, null if not provided")
    location: Optional[str] = Field(None, description="User's location from profile, null if not provided")
    education: str = Field(..., description="Combined education summary including degree, major, graduation year, and certifications")
    interests: List[str] = Field(..., description="List of user's interests from self-assessment")

class PersonalityTrait(BaseModel):
    trait: str = Field(..., description="The mapped trait/skill from the assessment question")
    inferredLevel: str = Field(..., description="Inferred level of the trait (e.g., 'Balanced', 'High', 'Low')")
    justification: str = Field(..., description="Explanation for why this level was inferred based on the assessment")
    potentialStrengths: List[str] = Field(..., description="List of potential strengths associated with this trait level")
    potentialWeaknesses: List[str] = Field(..., description="List of potential weaknesses associated with this trait level")

class CareerPaths(BaseModel):
    strongMatches: List[str] = Field(..., description="Career paths that strongly align with user's profile and education")
    otherPotentialPaths: List[str] = Field(..., description="Additional career paths that could be suitable")
    careersToPotentiallyAvoid: List[str] = Field(..., description="Careers that might pose challenges based on potential weaknesses")

class InterestsAndSubjects(BaseModel):
    interests: List[str] = Field(..., description="User's stated interests from profile")
    interestedSubjects: List[str] = Field(..., description="Academic/professional subjects inferred from user's interests")

# Main career report structure
class CareerReportContent(BaseModel):
    persona: Persona = Field(..., description="Summary of user's key characteristics and background")
    personalityProfile: List[PersonalityTrait] = Field(..., description="Detailed analysis of user's personality traits from assessment")
    careerPaths: CareerPaths = Field(..., description="Recommended career paths organized by suitability")
    strengths: List[str] = Field(..., description="User's key strengths based on profile and assessment")
    weaknesses: List[str] = Field(..., description="User's potential areas for improvement")
    interestsAndSubjects: InterestsAndSubjects = Field(..., description="User's interests and related academic subjects")
    nextSteps: List[str] = Field(..., description="Actionable recommendations for career exploration and development")

# Top-level response model
class CareerCompassResponse(BaseModel):
    careerReport: CareerReportContent = Field(..., description="Complete career analysis and recommendations")


# Create the CareerCompass agent with the detailed structured output
career_compass_agent = Agent(
    name="CareerCompass",
    model=Gemini(),
    description="""
    You are CareerCompass, a helpful AI assistant that generates comprehensive and 
    personalized career reports based on personality assessments and background information.
    """,
    instructions="""
    You are CareerCompass, designed to analyze user data and create detailed career reports.
    You provide objective, actionable insights while maintaining a professional and encouraging tone.

    **PROCESSING STEPS:**

    1. **Parse Input Data:**
       - Extract question_history (personality assessment questions)
       - Extract profile_summary (background information)

    2. **Create Persona:**
       - name: Extract from profile_summary.personalInfo.fullName (null if missing)
       - location: Extract from profile_summary.personalInfo.location (null if missing)
       - education: Combine degree, major, graduation year, certifications into descriptive string
       - interests: Extract array from profile_summary.selfAssessment.interests

    3. **Build Personality Profile:**
       For each question in question_history:
       - trait: Use "Mapped Trait/Skill" field
       - inferredLevel: Use "Medium Scale Skill" as "Balanced", "High Scale Skill" as higher level, "Low Scale Skill" as lower level
       - justification: Explain the reasoning for the inferred level
       - potentialStrengths: List strengths associated with this trait level
       - potentialWeaknesses: List potential challenges

    4. **Generate Career Recommendations:**
       - strongMatches: Careers aligned with education and strong personality traits
       - otherPotentialPaths: Additional suitable careers based on broader traits
       - careersToPotentiallyAvoid: Careers that might be challenging (use career hints from questions)

    5. **Summarize Strengths and Weaknesses:**
       - strengths: Key strengths from personality, education, and experience
       - weaknesses: Potential areas for improvement

    6. **Map Interests to Subjects:**
       - interests: Direct copy from profile
       - interestedSubjects: Infer related academic/professional subjects

    7. **Provide Next Steps:**
       Include these standard recommendations:
       - "Self-Reflection: Consider how well this profile resonates with your self-perception."
       - "Career Exploration: Research potential career paths in more detail, focusing on those that align with your strengths and interests. Network with professionals in those fields."
       - "Skill Development: Identify any skills that need further development to succeed in your desired career paths. Consider taking courses or workshops to enhance these skills."
       - "Networking: Connect with professionals in fields of interest to learn more about their experiences."

    **GUIDELINES:**
    - Be objective, use "potentially," "likely," "may suggest"
    - Provide actionable insights
    - Use concise, professional language
    - Don't invent information not in the data
    - Set name/location to null if not provided
    - Acknowledge limitations when information is missing
    - Tailor recommendations to user's specific background
    """,
    response_model=CareerCompassResponse,  # Use the structured model
    markdown=False
)



def career_compass_workflow(profile_summary: str, question_history: List[Dict[str, Any]]):
    """
    Main workflow function to generate a career report based on profile summary and question history.
    """
    # Run the CareerCompass agent with provided data
    instruction =  f"""
    Analyze the following user data and generate a comprehensive career report:
    
    profile_summary = {profile_summary}
    question_history = {questions_and_insights}
    
    Follow the step-by-step processing guidelines to create a complete career analysis.
    """
    response = career_compass_agent.run(
       instruction
    )
    return response.content.model_dump()  # Return the structured response as a dictionary