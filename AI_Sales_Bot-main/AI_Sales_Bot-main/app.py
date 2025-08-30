from flask import Flask, render_template, request, jsonify
from Agents.master_agent import MasterAgent
import stripe
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
stripe.api_key = os.getenv("STRIPE_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")


def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_queries (
            id SERIAL PRIMARY KEY,
            session_id TEXT,
            user_ip TEXT,
            query TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()


init_db()

sessions = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    session_id = request.cookies.get('session_id')
    if not session_id or session_id not in sessions:
        session_id = os.urandom(24).hex()
        sessions[session_id] = MasterAgent()

    user_input = request.json['message']
    user_ip = request.remote_addr
    agent = sessions[session_id]
    response = agent.process_input(user_input)

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_queries (session_id, user_ip, query, timestamp) VALUES (%s, %s, %s, %s)",
                   (session_id, user_ip, user_input, datetime.now()))
    conn.commit()
    cursor.close()
    conn.close()

    resp = jsonify({'response': response})
    resp.set_cookie('session_id', session_id)
    return resp


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
