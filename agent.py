import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from textwrap import dedent
from agno.tools.serpapi import SerpApiTools
import streamlit as st
import traceback

# Load environment variables from .env file
load_dotenv()

# Set up the Streamlit app
st.title("AI Travel Planner using Gemini-2.5-flash ✈️")
st.caption(
    "Plan your next adventure with AI Travel Planner by researching and planning a personalized itinerary on autopilot using local Llama-3"
)

# Get API keys and Ollama host from environment variables
serp_api_key = os.getenv("SERPAPI_API_KEY")
ollama_host = os.getenv("OLLAMA_HOST")
api_key = os.getenv(
    "GOOGLE_API_KEY"
)  # Replace with your actual API key if not using .env

model = Gemini(
    id="gemini-2.5-flash",
    api_key=api_key,
    search=True,
)

# Check for all required API keys
if not serp_api_key:
    st.error("Please set your SERPAPI_API_KEY environment variable.")
elif not api_key:
    st.error("Please set your GOOGLE_API_KEY environment variable.")
else:
    # The agno library's Ollama model should automatically use the OLLAMA_HOST environment variable if set.
    researcher = Agent(
        name="Researcher",
        role="Searches for travel destinations, activities, and accommodations based on user preferences",
        # model=Ollama(id="llama3.2:latest", host=ollama_host, client=ollama_custom_client),
        model=model,
        description=dedent(
            """
        You are a world-class travel researcher. Given a travel destination and the number of days the user wants to travel for,
        generate a list of search terms for finding relevant travel activities and accommodations.
        Then search the web for each term, analyze the results, and return the 10 most relevant results.
        """
        ),
        instructions=[
            "Given a travel destination and the number of days the user wants to travel for, first generate a list of 3 search terms related to that destination and the number of days.",
            "For each search term, `search_google` and analyze the results.",
            "From the results of all searches, return the 10 most relevant results to the user's preferences.",
            "Remember: the quality of the results is important.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    planner = Agent(
        name="Planner",
        role="Generates a draft itinerary based on user preferences and research results",
        # model=Ollama(id="llama3.2:latest", host=ollama_host, client=ollama_custom_client),
        model=model,
        description=dedent(
            """
        You are a senior travel planner. Given a travel destination, the number of days the user wants to travel for, and a list of research results,
        your goal is to generate a draft itinerary that meets the user's needs and preferences.
        """
        ),
        instructions=[
            "Given a travel destination, the number of days the user wants to travel for, and a list of research results, generate a draft itinerary that includes suggested activities and accommodations.",
            "Ensure the itinerary is well-structured, informative, and engaging.",
            "Ensure you provide a nuanced and balanced itinerary, quoting facts where possible.",
            "Remember: the quality of the itinerary is important.",
            "Focus on clarity, coherence, and overall quality.",
            "Never make up facts or plagiarize. Always provide proper attribution.",
        ],
        add_datetime_to_instructions=True,
    )

    # Input fields for the user's destination and the number of days they want to travel for
    destination = st.text_input("Where do you want to go?")
    num_days = st.number_input(
        "How many days do you want to travel for?", min_value=1, max_value=30, value=7
    )

    # Disable button if inputs are invalid
    if st.button("Generate Itinerary", disabled=not destination):
        with st.spinner("Researching your destination..."):
            try:
                research_results = researcher.run(
                    f"Research {destination} for a {num_days} day trip", stream=False
                )
                st.write("✓ Research completed")
                # Optionally display research results to the user
                # st.write(research_results.content)
            except Exception as e:
                st.error(f"Research failed: {e}")
                print(traceback.format_exc())
                research_results = None

        if research_results:
            with st.spinner("Creating your personalized itinerary..."):
                try:
                    prompt = dedent(
                        f"""
                        Destination: {destination}
                        Duration: {num_days} days
                        Research Results: {research_results.content}

                        Please create a detailed itinerary based on this research.
                    """
                    )
                    response = planner.run(prompt, stream=False)
                    st.write(response.content)
                except Exception as e:
                    st.error(f"Planner failed: {e}")
                    print(traceback.format_exc())
