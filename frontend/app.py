
import sys
from pathlib import Path

# Ensure project root is importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import streamlit as st

from backend.agents.langgraph_agent import run_travel_agent_graph
from backend.services.quotation_builder import build_quotation
from backend.services.pdf_generator import generate_quotation_pdf


st.set_page_config(
    page_title="TravelOps AI",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ TravelOps AI")
st.subheader("Your AI-powered travel quotation assistant")
st.caption(
    "Agentic travel planning using Groq, LangGraph, "
    "FAISS RAG and Python tools."
)

st.divider()

# User input
with st.form("travel_request_form"):

    st.subheader("Plan your trip")

    col1, col2 = st.columns(2)

    with col1:
        destination = st.text_input("Destination", "Goa")
        origin = st.text_input("Starting city", "Bhubaneswar")
        duration = st.number_input(
            "Duration (days)", min_value=1, max_value=60, value=5
        )

    with col2:
        travelers = st.number_input(
            "Number of travelers", min_value=1, max_value=50, value=2
        )
        budget = st.number_input(
            "Total budget (INR)", min_value=1000, value=40000, step=1000
        )
        hotel_preference = st.selectbox(
            "Hotel preference",
            ["budget", "comfortable", "luxury"]
        )

    submitted = st.form_submit_button(
        "Generate AI Travel Quotation",
        type="primary",
        use_container_width=True
    )


if submitted:

    if not destination.strip() or not origin.strip():
        st.error("Please enter both destination and starting city.")

    else:
        travel_request = {
            "destination": destination.strip().title(),
            "duration_days": int(duration),
            "travelers": int(travelers),
            "budget": float(budget),
            "currency": "INR",
            "origin": origin.strip().title(),
            "hotel_preference": hotel_preference,
            "travel_style": None
        }

        try:
            with st.spinner(
                "TravelOps AI is researching and calculating your trip..."
            ):
                result = run_travel_agent_graph(travel_request)

                if not result.get("success"):
                    raise RuntimeError("The travel agent could not complete the request.")

                quotation = build_quotation(
                    travel_request,
                    result["execution_log"]
                )

                pdf_path = generate_quotation_pdf(quotation)

            st.success("Your travel quotation is ready!")

            st.divider()
            st.header(f"Your trip to {quotation.destination}")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total estimated cost",
                f"₹{quotation.total_estimated_cost:,.0f}"
            )

            c2.metric(
                "Per traveler",
                f"₹{quotation.cost_per_person:,.0f}"
            )

            c3.metric(
                "Remaining budget",
                f"₹{quotation.remaining_budget:,.0f}"
                if quotation.remaining_budget is not None
                else "Not specified"
            )

            st.subheader("Cost breakdown")

            table_data = [
                {
                    "Category": item.category,
                    "Description": item.description,
                    "Cost (INR)": f"₹{item.amount:,.0f}"
                }
                for item in quotation.items
            ]

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Available attractions in the dataset")

            for attraction in quotation.attractions:
                st.write(f"📍 {attraction}")

            st.subheader("Assumptions and limitations")

            for assumption in quotation.assumptions:
                st.write(f"• {assumption}")

            st.divider()

            # Download PDF
            with open(pdf_path, "rb") as file:
                pdf_bytes = file.read()

            st.download_button(
                label="📄 Download Travel Quotation (PDF)",
                data=pdf_bytes,
                file_name=f"{quotation.destination}_travel_quotation.pdf",
                mime="application/pdf",
                use_container_width=True
            )

            # Agent execution trace
            with st.expander("View AI agent execution trace"):
                for entry in result["execution_log"]:
                    st.write(f"**Tool:** {entry.get('tool')}")

                    if entry.get("success"):
                        st.json(entry.get("result"))
                    else:
                        st.error(entry.get("error"))

            st.caption(
                "Demonstration estimates only. No live booking or availability "
                "confirmation is provided."
            )

        except Exception as error:
            st.error(f"Unable to generate quotation: {error}")
            st.exception(error)
