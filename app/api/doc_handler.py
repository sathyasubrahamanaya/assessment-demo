from fastapi import APIRouter,UploadFile
from app.agents.doc_agent import deepdive_career_analyst
from agno.media import File
import base64
from app.agents.models.datamodels import CareerAnalysisReport


doc_router = APIRouter(prefix="/pdfAnalysis")

doc_list = []
@doc_router.post("/analyze")
async def get_pdf_analysis(file:UploadFile):
  tmp_file = await file.read()
  pdf_report:CareerAnalysisReport = deepdive_career_analyst.run("Read and Examine the Document "
                           "Carefully and do the summary in accordance of career building",files=[File(content=tmp_file,mime_type="application/pdf")]).content
  doc_list.append(pdf_report)
  return pdf_report.model_dump()






