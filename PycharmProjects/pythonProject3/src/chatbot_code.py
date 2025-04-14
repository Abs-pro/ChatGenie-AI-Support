import uuid
import logging
from flask import Flask, request, jsonify
from transformers import pipeline, Conversation
from threading import Lock

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize the conversational pipeline with a pretrained model (DialoGPT-medium)
chatbot_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

# In-memory storage for conversation sessions
sessions = {}
sessions_lock = Lock()


@app.route('/')
def index():
    return "ChatGenie-AI-Support Chatbot Service is running!"


@app.route('/start', methods=['POST'])
def start_session():
    """
    Start a new conversation session.
    Returns a unique session ID.
    """
    session_id = str(uuid.uuid4())
    with sessions_lock:
        # Each session stores a Conversation object to track the conversation history.
        sessions[session_id] = Conversation("")
    logger.info(f"Started new session: {session_id}")
    return jsonify({"session_id": session_id, "message": "Session started. Send your message to /chat endpoint."})


@app.route('/chat', methods=['POST'])
def chat():
    """
    Process a message from a client with a session ID.
    Request should include JSON:
    {
      "session_id": "session_uuid",
      "message": "Hello, how are you?"
    }
    Response includes the generated reply and updated conversation history.
    """
    data = request.get_json()
    session_id = data.get('session_id')
    user_message = data.get('message', '')

    if not session_id or not user_message:
        return jsonify({"error": "Both session_id and message fields are required."}), 400

    # Retrieve the existing conversation for the session
    with sessions_lock:
        conversation = sessions.get(session_id)
        if conversation is None:
            return jsonify({"error": "Session not found. Please start a new session using /start."}), 404

    # Append the user message to the conversation
    conversation.add_user_input(user_message)
    logger.info(f"Session {session_id}: Received message: {user_message}")

    # Generate response using the conversational pipeline
    try:
        response_obj = chatbot_pipeline(conversation)
        # The response text is taken from the conversation object's latest generated response.
        reply = response_obj.generated_responses[
            -1] if response_obj.generated_responses else "I'm sorry, I didn't understand that."
    except Exception as e:
        logger.error(f"Session {session_id}: Error during conversation processing: {e}")
        return jsonify({"error": "Error processing the request."}), 500

    logger.info(f"Session {session_id}: Generated reply: {reply}")

    # Return the new reply and conversation history as a list of message pairs
    history = []
    # The conversation object stores history internally. (For demonstration, we simulate it by splitting raw text.)
    raw_text = conversation.past_user_inputs + conversation.generated_responses
    for idx, msg in enumerate(raw_text):
        history.append({"turn": idx + 1, "message": msg})

    return jsonify({
        "session_id": session_id,
        "reply": reply,
        "conversation_history": history
    })


@app.route('/reset', methods=['POST'])
def reset_session():
    """
    Reset the conversation for an existing session.
    Request should include JSON:
    {
      "session_id": "session_uuid"
    }
    """
    data = request.get_json()
    session_id = data.get('session_id')
    if not session_id:
        return jsonify({"error": "session_id is required."}), 400

    with sessions_lock:
        if session_id in sessions:
            sessions[session_id] = Conversation("")
            logger.info(f"Session {session_id} has been reset.")
            return jsonify({"message": f"Session {session_id} has been reset."})
        else:
            return jsonify({"error": "Session not found."}), 404


@app.route('/sessions', methods=['GET'])
def list_sessions():
    """
    List active session IDs.
    """
    with sessions_lock:
        active_sessions = list(sessions.keys())
    return jsonify({"active_sessions": active_sessions})


if __name__ == '__main__':
    # Run Flask app on port 5000 with debug mode enabled.
    app.run(debug=True)
