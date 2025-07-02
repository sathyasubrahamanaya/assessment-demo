# AI Career Assessment - Streamlit UI

A modern, interactive web interface for the AI Career Assessment Platform built with Streamlit.

## 🚀 Features

### 📄 PDF Analysis
- Upload PDF documents for career-relevant analysis
- Get comprehensive insights about document content
- View ideal reader personas and career pathways
- Analyze cognitive profiles and skill requirements

### 🎯 Career Interview
- **Phase 1: Profile Collection** - Interactive AI-guided profile building
- **Phase 2: Assessment Interview** - Dynamic personality and career assessment
- Intelligent question rendering (Scale-based, MCQ, Text input)
- Real-time progress tracking

### 📊 Career Report
- Generate personalized career analysis
- View personality profiles and trait analysis
- Get career recommendations (Strong matches, Potential paths, Paths to avoid)
- Actionable next steps for career development

### 📚 Case Study Recommendations
- AI-powered case study matching
- Quantified relevance scoring
- Personalized learning recommendations

## 🛠️ Installation

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI Backend:**
   ```bash
   # From the root directory
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Run the Streamlit UI:**
   ```bash
   # From the ui directory
   streamlit run streamlit_app.py
   ```

## 🎨 UI Features

### Smart Question Rendering
- **Scale Questions**: Interactive 1-5 rating with buttons and slider
- **MCQ Questions**: Intelligent option extraction with radio buttons
- **Text Input**: Fallback for complex questions
- **Profile Collection**: Conversational AI interface

### Modern Design
- Responsive layout with sidebar navigation
- Custom CSS styling for professional appearance
- Progress indicators and status tracking
- Expandable sections for detailed information

### Session Management
- Persistent session state across page refreshes
- Progress tracking and completion status
- Easy session reset functionality

## 📱 Usage

1. **Start with PDF Analysis** (Optional)
   - Upload a PDF document
   - View career-relevant insights

2. **Begin Career Interview**
   - Complete profile collection phase
   - Answer assessment questions
   - Track your progress

3. **Generate Career Report**
   - View personalized analysis
   - Explore career recommendations
   - Review personality insights

4. **Get Case Study Recommendations**
   - Receive personalized case study suggestions
   - View relevance scores and criteria

## 🔧 Configuration

### API Configuration
- Default API URL: `http://localhost:8000`
- Modify `API_BASE_URL` in `streamlit_app.py` if needed

### Customization
- Update CSS styles in the `st.markdown()` section
- Modify question rendering logic in `render_question_ui()`
- Customize session state management

## 🎯 Key Components

### Question Intelligence
The UI intelligently extracts MCQ options using regex patterns:
- `A)`, `B)`, `C)`, `D)` format
- `A.`, `B.`, `C.`, `D.` format
- `Option A:`, `Option B:` format
- "or" pattern fallback

### Phase Management
- Automatic phase transitions
- Session state persistence
- Progress indicators
- Completion tracking

### Error Handling
- API error handling with user-friendly messages
- Graceful fallbacks for missing data
- Input validation and sanitization

## 🚀 Getting Started

1. Ensure the FastAPI backend is running on port 8000
2. Install UI dependencies: `pip install -r requirements.txt`
3. Run the Streamlit app: `streamlit run streamlit_app.py`
4. Open your browser to the provided URL (usually `http://localhost:8501`)

## 📊 Session Flow

```
PDF Analysis (Optional)
    ↓
Profile Collection (Phase 1)
    ↓
Career Interview (Phase 2)
    ↓
Career Report Generation
    ↓
Case Study Recommendations
```

## 🎨 UI Screenshots

The interface includes:
- Clean, modern design with professional styling
- Intuitive navigation with sidebar
- Interactive question components
- Progress tracking and status indicators
- Expandable sections for detailed information
- Responsive layout for different screen sizes

## 🔄 State Management

The app uses Streamlit's session state to maintain:
- Interview progress and phases
- Question history and responses
- Generated reports and analysis
- User preferences and settings

## 🛡️ Error Handling

- API connection errors with retry options
- Missing data graceful handling
- Input validation and sanitization
- User-friendly error messages

## 📈 Future Enhancements

- Export functionality for reports
- Advanced visualization of personality traits
- Interactive career pathway exploration
- Real-time collaboration features
- Mobile-responsive optimizations 