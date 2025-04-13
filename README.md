## Overview
This project implements a chatbot capable of interacting with PDF documents using OpenRouter AI API for language processing.
- Dark/Light mode support
- Modern and responsive UI
- Voice input support

## Interface Preview

![Chat Assistant Interface](/static/image/interface.png)

## Installation
### 1. Clone the Repository
```sh
git clone https://github.com/noaft/Notebook_LLM.git
cd Notebook_LLM
```

### 2. Install Dependencies
Ensure you have Python installed, then run:
```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root and add your OpenRouter API key:
```env
API_KEY=<your_openrouter_api_key>
```

## Running the Application
To start the FastAPI server, use:
```sh
python -m uvicorn main:app --reload
```
This will launch the chatbot API locally.

## Usage
Once the server is running, you can:
- Upload PDF files for analysis.
- Interact with the chatbot via API endpoints.

## Dependencies
Ensure that `requirements.txt` is installed, containing necessary packages such as FastAPI and OpenAI API clients.

## Notes
- The API key should be kept secure and not shared.
- The chatbot utilizes OpenRouter AI to process user queries.
- Ensure your environment supports FastAPI and `uvicorn` for local execution.

## License
This project is licensed under [MIT License](LICENSE).
