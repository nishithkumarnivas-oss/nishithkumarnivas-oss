# Nike GenAI Agent

This project is a FastAPI-based AI agent for the Nike brand. It generates copywriting (using OpenAI GPT-4) and images (using Stable Diffusion API) based on text prompts, following Nike brand guidelines (colors, slogans, logo).

## Features
- Generate Nike-styled copywriting
- Generate Nike-branded images
- Follows Nike brand guidelines
- REST API endpoint for prompt-to-asset generation

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set your OpenAI and Stable Diffusion API keys in the `.env` file
3. Run the server: `uvicorn main:app --reload`

## Endpoints
- `POST /generate`: Generate copy or image asset from a prompt

## Brand Guidelines
- Colors: Black, White, Nike Red
- Slogan: Just Do It
- Logo: (add your logo file in `assets/`)
