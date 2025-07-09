# AI Travel Planner 🌍✈️

An intelligent travel planning assistant powered by Google's Gemini AI that helps you create personalized travel itineraries. Simply input your destination and duration, and let the AI create a detailed, well-researched travel plan for you.

## Features

- 🔍 Intelligent destination research using SerpAPI
- 📝 Detailed itinerary generation
- 🎯 Personalized recommendations
- 🌐 Real-time web data integration
- 📊 User-friendly Streamlit interface

## Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver
- API Keys:
  - Google API Key (for Gemini)
  - SerpAPI Key (for web search)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-travel-agent.git
cd ai-travel-agent
```

2. Create a `.env` file in the project root with your API keys:

```
GOOGLE_API_KEY='your_google_api_key'
SERPAPI_API_KEY='your_serpapi_key'
```

3. Install the package using uv:

```bash
uv sync
```

## Usage

Running directly with uv:

```bash
uv run streamlit run agent.py
```

The web interface will open in your default browser. Enter your desired destination and number of days for your trip, and click "Generate Itinerary" to get your personalized travel plan.

## Development

To format the code:

```bash
uv pip install black
black .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Using [SerpAPI](https://serpapi.com/) for web search
- Built with [Agno](https://github.com/agno-agi/agno) framework
