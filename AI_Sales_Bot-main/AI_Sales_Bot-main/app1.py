from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
from Agents.master_agent import MasterAgent
import logging
import os

load_dotenv()

app = Flask(__name__)
active_calls = {}

logging.basicConfig(level=logging.DEBUG)


@app.route('/voice/incoming', methods=['POST'])
def handle_incoming_call():
    """Handle initial phone call connection"""
    call_sid = request.form.get('CallSid')
    caller_number = request.form.get('From')

    logging.info(f"📞 Incoming call from {caller_number} (CallSid: {call_sid})")
    if not call_sid:
        logging.error("❌ Missing CallSid in Twilio request")
        return error_response("Invalid request.")

    active_calls[call_sid] = MasterAgent()

    response = VoiceResponse()
    gather = Gather(
        input='speech',
        action='/voice/handle-input',
        method='POST',
        speech_timeout=5
    )
    gather.say("Welcome! How can I assist you today?")
    response.append(gather)

    logging.debug(
        f"🗣️ Prompt sent to user: 'Welcome! How can I assist you today?'")
    return Response(str(response), mimetype='text/xml')


@app.route('/voice/handle-input', methods=['POST'])
def handle_voice_input():
    """Process speech input and generate response"""
    call_sid = request.form.get('CallSid')
    speech_text = request.form.get('SpeechResult', '')

    logging.info(
        f"🎙️ Received speech input: '{speech_text}' (CallSid: {call_sid})")

    agent = active_calls.get(call_sid)
    if not agent:
        logging.warning("⚠️ Session expired or CallSid not found.")
        return error_response("Session expired. Please call back.")

    try:
        text_response = agent.process_input(speech_text)
        logging.debug(f"🤖 Agent Response: '{text_response}'")
    except Exception as e:
        logging.error(f"❌ Error processing input: {str(e)}", exc_info=True)
        return error_response("Error processing request.")

    response = VoiceResponse()
    gather = Gather(
        input='speech',
        action='/voice/handle-input',
        method='POST',
        speech_timeout=5
    )
    gather.say(text_response)
    response.append(gather)

    return Response(str(response), mimetype='text/xml')


def error_response(message):
    """Create error response"""
    response = VoiceResponse()
    response.say(message)
    response.hangup()
    logging.error(f"🚨 Error Response Sent: '{message}'")
    return Response(str(response), mimetype='text/xml')


if __name__ == '__main__':
    app.run(debug=True)
