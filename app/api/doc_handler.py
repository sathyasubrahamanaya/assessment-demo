from fastapi import APIRouter, UploadFile, HTTPException
from app.agents.doc_agent import deepdive_career_analyst
from agno.media import File
import base64
from app.agents.models.datamodels import CareerAnalysisReport
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

doc_router = APIRouter(prefix="/pdfAnalysis")

doc_list = []

@doc_router.post("/analyze")
async def get_pdf_analysis(file: UploadFile):
    """
    Analyze a PDF document for career-relevant insights.
    """
    try:
        # Validate file type
        if not file.content_type == "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Read file content
        tmp_file = await file.read()
        
        if not tmp_file:
            raise HTTPException(status_code=400, detail="Empty file provided")
        
        logger.info(f"Processing PDF file: {file.filename}, size: {len(tmp_file)} bytes")
        
        # Run the analysis
        try:
            pdf_report = deepdive_career_analyst.run(
                "Read and Examine the Document Carefully and do the summary in accordance of career building",
                files=[File(content=tmp_file, mime_type="application/pdf")]
            )
            
            if pdf_report and hasattr(pdf_report, 'content'):
                result = pdf_report.content
                doc_list.append(result)
                return result.model_dump()
            else:
                raise HTTPException(status_code=500, detail="Failed to generate analysis report")
                
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in PDF analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@doc_router.get("/getDocList")
def get_doc_list():
    """
    Retrieve the list of analyzed documents.
    """
    if not doc_list:
        return {"message": "No documents have been analyzed yet."}
    
    return {"documents": [doc.model_dump() for doc in doc_list]}



