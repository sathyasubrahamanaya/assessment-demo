import streamlit as st
import requests
import json
import pandas as pd
from typing import Dict, Any, List, Optional
import time

# Page configuration
st.set_page_config(
    page_title="AI Career Assessment",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1f77b4;
    }
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .upload-area {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    .status-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .status-info {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pdf_analyses' not in st.session_state:
    st.session_state.pdf_analyses = []

if 'interview_session' not in st.session_state:
    st.session_state.interview_session = {
        'current_phase': 'profile_collection',
        'profile_completed': False,
        'current_question': None,
        'question_history': [],
        'user_profile': {},
        'career_report': None
    }

# API base URL
API_BASE_URL = "http://localhost:8000"

def call_api(endpoint: str, method: str = "GET", data: Optional[Dict] = None, files: Optional[Dict] = None):
    """Generic function to call the FastAPI endpoints"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        
        if method == "GET":
            if data:
                response = requests.get(url, params=data)
            else:
                response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def render_pdf_analysis():
    """Render the PDF analysis section"""
    st.markdown('<h2 class="section-header">📄 PDF Document Analysis</h2>', unsafe_allow_html=True)
    
    # Remove custom upload area, only use Streamlit's file uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'], key="pdf_uploader")
    
    if uploaded_file is not None:
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔍 Analyze PDF", key="analyze_pdf", type="primary"):
                with st.spinner("Analyzing your PDF document..."):
                    # Prepare the file for upload
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    
                    # Call the PDF analysis API
                    response = call_api("/pdfAnalysis/analyze", method="POST", files=files)
                    
                    if response:
                        # Add to session state
                        analysis_data = {
                            'filename': uploaded_file.name,
                            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                            'analysis': response
                        }
                        st.session_state.pdf_analyses.append(analysis_data)
                        st.success("✅ PDF analysis completed successfully!")
                        st.rerun()
    
    # Display recent analyses
    if st.session_state.pdf_analyses:
        st.markdown("### 📊 Recent Analyses")
        
        for i, analysis in enumerate(reversed(st.session_state.pdf_analyses[-5:])):  # Show last 5
            with st.expander(f"📄 {analysis['filename']} - {analysis['timestamp']}"):
                analysis_result = analysis['analysis']
                
                # Document Summary
                if 'document_summary' in analysis_result:
                    st.markdown("**📝 Document Summary:**")
                    st.markdown(f"*{analysis_result['document_summary']['overall_description']}*")
                
                # Ideal Reader Persona
                if 'ideal_reader_persona' in analysis_result:
                    st.markdown("**👥 Ideal Reader:**")
                    persona = analysis_result['ideal_reader_persona']
                    st.markdown(f"**Archetype:** {persona['persona_archetype']}")
                    st.markdown(f"**Description:** {persona['short_description']}")
                
                # Career Relevance
                if 'career_relevance' in analysis_result:
                    st.markdown("**🎯 Career Focus:**")
                    career_rel = analysis_result['career_relevance']
                    st.markdown(f"**Primary Focus:** {career_rel['primary_career_group_focus']}")
                    
                    if 'career_pathways' in career_rel:
                        pathways = career_rel['career_pathways']
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Direct Application:**")
                            for role in pathways.get('direct_application_roles', [])[:3]:
                                st.markdown(f"• {role}")
                        with col2:
                            st.markdown("**Strategy & Leadership:**")
                            for role in pathways.get('strategy_and_leadership_roles', [])[:3]:
                                st.markdown(f"• {role}")

def extract_mcq_options(question_text: str) -> List[str]:
    """Extract MCQ options from question text using regex patterns"""
    import re
    
    # Common MCQ patterns
    patterns = [
        r'[A-D]\)\s*([^A-D)]+)',  # A) option text
        r'[A-D]\.\s*([^A-D.]+)',  # A. option text
        r'Option [A-D]:\s*([^A-D]+)',  # Option A: text
        r'[A-D]\s*[-\-]\s*([^A-D]+)',  # A - option text
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, question_text, re.IGNORECASE)
        if matches:
            return [match.strip() for match in matches]
    
    # Fallback: look for "or" patterns
    if " or " in question_text.lower():
        parts = question_text.split(" or ")
        return [part.strip() for part in parts if part.strip()]
    
    return []

def render_interview():
    """Render the interview section"""
    # If interview is completed, show only recommendations or upload prompt
    if st.session_state.interview_session['current_phase'] == 'completed':
        st.markdown("### 🎉 Interview Completed!")
        st.markdown("**📚 Raw JSON Response from matchCaseStudies:**")
        
        # Call matchCaseStudies API
        match_response = call_api("/interview/matchCaseStudies")
        
        if match_response:
            # Display the raw JSON response
            st.json(match_response)
        else:
            st.warning("No response received from matchCaseStudies API.")
        return
    st.markdown('<h2 class="section-header">🎯 Career Assessment Interview</h2>', unsafe_allow_html=True)
    
    # Initialize chat history, input key, and question key if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chat_input_key' not in st.session_state:
        st.session_state.chat_input_key = 0
    if 'question_key' not in st.session_state:
        st.session_state.question_key = 0
    
    # Phase indicator
    if not st.session_state.interview_session['profile_completed']:
        st.markdown("**📝 Phase 1: Profile Collection**")
        
        # If chat is empty, have AI start the conversation
        if len(st.session_state.chat_history) == 0:
            response = call_api("/interview/interact", data={"input_text": "Hi let's start"})
            if response and 'response' in response:
                response_data = response['response']
                ai_response = response_data.get('response', '')
                st.session_state.chat_history.append({
                    'type': 'ai',
                    'content': ai_response
                })
                st.session_state.chat_input_key += 1
                st.rerun()
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['type'] == 'ai':
                st.markdown(f"🤖 **AI:** {message['content']}")
            else:
                st.markdown(f"👤 **You:** {message['content']}")
        
        # Chat input using form for better handling
        with st.form("chat_form"):
            user_input = st.text_input("Type your response:", key=f"chat_input_{st.session_state.chat_input_key}")
            submit_button = st.form_submit_button("Send")
            
            if submit_button and user_input.strip():
                # Add user message to chat
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': user_input
                })
                
                # Call the interview API
                response = call_api("/interview/interact", data={"input_text": user_input})
                
                if response and 'response' in response:
                    response_data = response['response']
                    
                    if response_data.get('status') == 'profile_completed':
                        # Profile collection completed
                        st.session_state.interview_session['profile_completed'] = True
                        st.session_state.interview_session['current_phase'] = 'interview'
                        st.session_state.chat_input_key += 1
                        st.success("✅ Profile collection completed! Moving to interview phase.")
                        st.rerun()
                    else:
                        # Add AI response to chat
                        ai_response = response_data.get('response', '')
                        st.session_state.chat_history.append({
                            'type': 'ai',
                            'content': ai_response
                        })
                        st.session_state.chat_input_key += 1
                        st.rerun()
    else:
        # Interview Phase
        st.markdown("**🎯 Phase 2: Career Assessment Interview**")
        
        # Check if we have a current question
        if st.session_state.interview_session['current_question'] is None:
            # Get the first question
            response = call_api("/interview/interact", data={"input_text": "start interview"})
            
            if response and 'response' in response:
                response_data = response['response']
                
                if response_data.get('input_type') == 'scale/mcq':
                    # The question data is in response_data['response']
                    st.session_state.interview_session['current_question'] = response_data.get('response', response_data)
                    st.session_state.question_key += 1
                    st.rerun()
                elif response_data.get('input_type') == 'user_input':
                    st.markdown("**🤖 AI:** " + response_data.get('response', ''))
                    st.rerun()
        
        # Render current question
        if st.session_state.interview_session['current_question']:
            question_data = st.session_state.interview_session['current_question']
            question_text = question_data.get('question', '')
            question_type = question_data.get('question_type', '')
            question_number = question_data.get('question_number', '')
            
            # Display the question with number
            if question_number:
                st.markdown(f"**🤔 Question {question_number}: {question_text}**")
            else:
                st.markdown(f"**🤔 {question_text}**")
            
            if question_type == 'scale':
                # Scale question - show rating slider
                st.markdown("**Rate your response (1-5):**")
                scale_answer = st.slider("", 1, 5, 3, key=f"scale_slider_{st.session_state.question_key}")
                
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Submit Rating", key=f"submit_scale_{st.session_state.question_key}"):
                        # Submit the answer
                        response = call_api("/interview/interact", data={"input_text": str(scale_answer)})
                        
                        if response and 'response' in response:
                            response_data = response['response']
                            
                            if response_data.get('input_type') == 'scale/mcq':
                                # Add to question history
                                st.session_state.interview_session['question_history'].append({
                                    'question': question_text,
                                    'answer': str(scale_answer),
                                    'question_type': question_type
                                })
                                
                                # Check if interview is completed
                                process_completed = False
                                next_question = response_data.get('response', response_data)
                                if isinstance(next_question, dict):
                                    process_completed = next_question.get('process_completed', False)
                                if process_completed:
                                    st.session_state.interview_session['current_phase'] = 'completed'
                                    st.success("✅ Interview completed!")
                                    st.session_state.question_key += 1
                                    st.rerun()
                                else:
                                    # Interview not completed, update to next question
                                    next_question = response_data.get('response', response_data)
                                    st.session_state.interview_session['current_question'] = next_question
                                    st.session_state.question_key += 1
                                    st.rerun()
                            else:
                                st.error("Unexpected response format")
                                st.rerun()
            elif question_type == 'mcq':
                # Use options from API if available and valid
                options = question_data.get('options', None)
                valid_options = []
                if options and isinstance(options, list):
                    valid_options = [opt for opt in options if opt and opt.strip() and opt.strip() != "."]
                if valid_options:
                    st.markdown("**Select your answer:**")
                    selected_option = st.radio("", valid_options, key=f"mcq_radio_{st.session_state.question_key}")
                    if st.button("Submit Answer", key=f"submit_mcq_{st.session_state.question_key}"):
                        if selected_option:
                            # Submit the answer
                            response = call_api("/interview/interact", data={"input_text": selected_option})
                            if response and 'response' in response:
                                response_data = response['response']
                                if response_data.get('input_type') == 'scale/mcq':
                                    st.session_state.interview_session['question_history'].append({
                                        'question': question_text,
                                        'answer': selected_option,
                                        'question_type': question_type
                                    })
                                    if response_data.get('status') == True:
                                        # Check process_completed inside response
                                        process_completed = False
                                        next_question = response_data.get('response', response_data)
                                        if isinstance(next_question, dict):
                                            process_completed = next_question.get('process_completed', False)
                                        if process_completed:
                                            st.session_state.interview_session['current_phase'] = 'completed'
                                            st.success("✅ Interview completed!")
                                            st.session_state.question_key += 1
                                            st.rerun()
                                    else:
                                        # Interview not completed, update to next question
                                        next_question = response_data.get('response', response_data)
                                        st.session_state.interview_session['current_question'] = next_question
                                        st.session_state.question_key += 1
                                        st.rerun()
                else:
                    # Fallback to text input if options are not valid
                    st.markdown("**Please provide your answer:**")
                    mcq_answer = st.text_input("Your answer:", key=f"mcq_text_{st.session_state.question_key}")
                    if st.button("Submit", key=f"submit_mcq_text_{st.session_state.question_key}"):
                        if mcq_answer.strip():
                            response = call_api("/interview/interact", data={"input_text": mcq_answer})
                            if response and 'response' in response:
                                response_data = response['response']
                                if response_data.get('input_type') == 'scale/mcq':
                                    st.session_state.interview_session['question_history'].append({
                                        'question': question_text,
                                        'answer': mcq_answer,
                                        'question_type': question_type
                                    })
                                    if response_data.get('status') == True:
                                        # Check process_completed inside response
                                        process_completed = False
                                        next_question = response_data.get('response', response_data)
                                        if isinstance(next_question, dict):
                                            process_completed = next_question.get('process_completed', False)
                                        if process_completed:
                                            st.session_state.interview_session['current_phase'] = 'completed'
                                            st.success("✅ Interview completed!")
                                            st.session_state.question_key += 1
                                            st.rerun()
                                    else:
                                        # Interview not completed, update to next question
                                        next_question = response_data.get('response', response_data)
                                        st.session_state.interview_session['current_question'] = next_question
                                        st.session_state.question_key += 1
                                        st.rerun()

def render_doc_summaries():
    """Render the document summaries section"""
    st.markdown('<h2 class="section-header">📚 Document Summaries</h2>', unsafe_allow_html=True)
    
    # Get document list from API
    doc_response = call_api("/pdfAnalysis/getDocList")
    
    if doc_response and 'documents' in doc_response and doc_response['documents']:
        st.markdown("### 📊 Analyzed Documents")
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">Total Documents</div>
            </div>
            """.format(len(doc_response['documents'])), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">{}</div>
                <div class="metric-label">This Session</div>
            </div>
            """.format(len(st.session_state.pdf_analyses)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">📄</div>
                <div class="metric-label">PDF Files</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Display document summaries
        for i, doc in enumerate(doc_response['documents']):
            with st.expander(f"📄 Document {i+1} - {doc.get('document_title', 'Untitled')}"):
                # Document Summary
                if 'document_summary' in doc:
                    st.markdown("**📝 Summary:**")
                    st.markdown(f"*{doc['document_summary']['overall_description']}*")
                
                # Ideal Reader
                if 'ideal_reader_persona' in doc:
                    st.markdown("**👥 Ideal Reader:**")
                    persona = doc['ideal_reader_persona']
                    st.markdown(f"**Archetype:** {persona['persona_archetype']}")
                    st.markdown(f"**Description:** {persona['short_description']}")
                
                # Career Pathways
                if 'career_relevance' in doc and 'career_pathways' in doc['career_relevance']:
                    st.markdown("**🎯 Career Pathways:**")
                    pathways = doc['career_relevance']['career_pathways']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Direct Application:**")
                        for role in pathways.get('direct_application_roles', [])[:5]:
                            st.markdown(f"• {role}")
                    
                    with col2:
                        st.markdown("**Strategy & Leadership:**")
                        for role in pathways.get('strategy_and_leadership_roles', [])[:5]:
                            st.markdown(f"• {role}")
                
                # Skills and Competencies
                if 'personality_skill_focus' in doc:
                    st.markdown("**🛠️ Key Skills:**")
                    skills = doc['personality_skill_focus']
                    skill_list = skills.get('key_skills_and_competencies_developed', [])
                    for skill in skill_list[:5]:
                        st.markdown(f"• {skill}")
    
    else:
        st.markdown("""
        <div class="card">
            <h3>📚 No Documents Analyzed Yet</h3>
            <p>Start by uploading and analyzing a PDF document in the PDF Analysis section.</p>
        </div>
        """, unsafe_allow_html=True)

def render_introduction():
    st.markdown('<h2 class="section-header">👋 Introduction</h2>', unsafe_allow_html=True)
    st.markdown('''
**Welcome to the AI Career Assessment Demo!**

This demo showcases a full-stack flow with both client and server side logic:

- **PDF Upload & PDF List:** These features are handled on the server side. You can upload your case study PDFs and view the list of analyzed documents.
- **Interview:** This interactive career assessment interview is handled on the client side, providing a chat-like experience.

### How to use this demo
1. **Upload and analyze your case studies** in the PDF Analysis section.
2. **Start the interview** in the Interview section to receive personalized recommendations.

Enjoy exploring the platform!
''')

def render_sidebar():
    """Render the sidebar navigation"""
    st.sidebar.title("🎯 AI Career Assessment")
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.markdown("### 📋 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["👋 Introduction", "📄 PDF Analysis", "🎯 Interview", "📚 Document Summaries"]
    )
    
    # Session status
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Session Status")
    
    # PDF Analysis status
    if st.session_state.pdf_analyses:
        st.sidebar.success(f"✅ {len(st.session_state.pdf_analyses)} PDF(s) analyzed")
    else:
        st.sidebar.info("⏳ No PDFs analyzed yet")
    
    # Interview status
    if st.session_state.interview_session['profile_completed']:
        st.sidebar.success("✅ Profile completed")
    else:
        st.sidebar.info("⏳ Profile collection")
    
    # Clear session button
    st.sidebar.markdown("---")
    if st.sidebar.button("🗑️ Clear Session", type="secondary"):
        st.session_state.pdf_analyses = []
        st.session_state.interview_session = {
            'current_phase': 'profile_collection',
            'profile_completed': False,
            'current_question': None,
            'question_history': [],
            'user_profile': {},
            'career_report': None
        }
        st.rerun()
    
    return page

# Main application
def main():
    st.markdown('<h1 class="main-header">🎯 AI Career Assessment Platform</h1>', unsafe_allow_html=True)
    
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Render main content based on selection
    if "👋 Introduction" in selected_page:
        render_introduction()
    elif "📄 PDF Analysis" in selected_page:
        render_pdf_analysis()
    elif "🎯 Interview" in selected_page:
        render_interview()
    elif "📚 Document Summaries" in selected_page:
        render_doc_summaries()

if __name__ == "__main__":
    main()
