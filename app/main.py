from fastapi import FastAPI
from app.api.doc_handler import doc_router
from app.api.interview import interview_router



app = FastAPI(title="AI Assessment")



app.include_router(doc_router)
app.include_router(interview_router)













