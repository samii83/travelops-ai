
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from backend.services.travel_parser import parse_travel_request
from backend.agents.langgraph_agent import run_travel_agent_graph
from backend.services.quotation_builder import build_quotation


app = FastAPI(
    title="TravelOps AI",
    description=(
        "Agentic travel quotation system using Groq, LangGraph, "
        "FAISS RAG and Python tools."
    ),
    version="1.0.0"
)


class ParseRequest(BaseModel):
    message: str = Field(min_length=5, max_length=5000)


class GenerateQuotationRequest(BaseModel):
    message: str = Field(min_length=5, max_length=5000)


@app.get("/")
def root():
    return {
        "application": "TravelOps AI",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/parse-travel-request")
def parse_request(request: ParseRequest):

    try:
        parsed = parse_travel_request(request.message)

        missing_fields = [
            field for field in [
                "destination",
                "duration_days",
                "travelers",
                "budget",
                "origin"
            ]
            if getattr(parsed, field) is None
        ]

        return {
            "success": True,
            "travel_request": parsed.model_dump(),
            "missing_fields": missing_fields
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Travel request parsing failed: {str(error)}"
        )


@app.post("/api/generate-quotation")
def generate_quotation(request: GenerateQuotationRequest):

    try:
        # Step 1: Extract structured requirements
        parsed = parse_travel_request(request.message)

        missing_fields = [
            field for field in [
                "destination",
                "duration_days",
                "travelers",
                "budget",
                "origin"
            ]
            if getattr(parsed, field) is None
        ]

        if missing_fields:
            return {
                "success": False,
                "ready_for_quotation": False,
                "missing_fields": missing_fields,
                "message": (
                    "Please provide the missing travel information."
                )
            }

        travel_request = parsed.model_dump()

        # Step 2: Run LangGraph agent
        agent_result = run_travel_agent_graph(travel_request)

        if not agent_result.get("success"):
            raise ValueError("Travel agent did not complete successfully.")

        # Step 3: Build validated quotation
        quotation = build_quotation(
            travel_request,
            agent_result["execution_log"]
        )

        # Step 4: Return structured output
        return {
            "success": True,
            "ready_for_quotation": True,
            "quotation": quotation.model_dump(),
            "agent_execution_log": agent_result["execution_log"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Quotation generation failed: {str(error)}"
        )
