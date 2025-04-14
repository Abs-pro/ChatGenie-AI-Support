# ChatGenie-AI-Support

ChatGenie-AI-Support is a conversational AI application designed to revolutionize customer support using advanced natural language processing (NLP) and deep learning techniques. This project provides a robust, session-based chatbot API built with Flask and the Hugging Face Transformers library. It enables real-time conversational interactions and session management for seamless customer service automation.

## Project Overview

This application offers a suite of endpoints to start new conversation sessions, process chat messages with context, retrieve conversation history, and reset sessions as needed. Built on a pretrained model (DialoGPT-medium), it generates responses that handle user inquiries promptly and effectively. Key features include:
- **Session-Based Conversations:** Each conversation has a unique session ID for maintaining context.
- **Context Management:** Maintains conversation history for personalized, context-aware responses.
- **Robust API Endpoints:** Endpoints for initiating sessions, chatting, and managing conversation state.
- **Logging and Error Handling:** Built-in logging to monitor interactions and aid debugging.

## Project Structure

    ChatGenie-AI-Support/
    ├── src/
    │   └── chatbot_app.py       # Main Flask application with chatbot API endpoints
    ├── requirements.txt         # List of required Python packages
    ├── README.md                # Project overview and setup instructions
    └── .gitignore               # Specifies files/directories for Git to ignore

## Requirements

- Python 3.x
- Flask
- Transformers
- Torch
- SentencePiece
- Gunicorn (optional for production)
- Additional utility libraries as listed in `requirements.txt`

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/ChatGenie-AI-Support.git
    ```
2. **Navigate to the project folder:**
    ```bash
    cd ChatGenie-AI-Support
    ```
3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Application:**
    Launch the chatbot service by running:
    ```bash
    python src/chatbot_app.py
    ```
2. **Interact with the API:**
    - **Start a New Session:**  
      Send a POST request to `/start` to create a new session and receive a unique session ID.
    - **Chat:**  
      Use the session ID along with your message at the `/chat` endpoint to receive a response.
    - **Reset a Session:**  
      Reset conversation history by sending a POST request to `/reset`.

## Contributing

Contributions, bug fixes, and enhancements are welcome. Please open an issue or submit a pull request with your improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
