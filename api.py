from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Database connection
DB_CONFIG = {
    'dbname': 'TTS',
    'user': 'postgres',  # Replace with your PostgreSQL username
    'password': '1234',  # Replace with your PostgreSQL password
    'host': 'localhost',
    'port': '5432'
}

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


# Default route
@app.route('/', methods=['GET'])
def home():
    print("Default route '/' was accessed.")
    return "Welcome to the TTS API! Use /voices, /voice, or /tts for API operations."


# API: Get all voices
@app.route('/voices', methods=['GET'])
def get_all_voices():
    print("GET /voices was accessed.")
    try:
        conn = get_db_connection()
        print("Database connection established.")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM voice")
        rows = cursor.fetchall()
        conn.close()
        print(f"Fetched {len(rows)} voices from the database.")

        voices = []
        for row in rows:
            voices.append({
                "id": row[0],
                "voice_name": row[1],
                "voice_description": row[2],
                "languages": row[3],
                "voice_features": row[4],
                "voicemail_id": row[5],
                "created_at": row[6],
                "updated_at": row[7],
                "valid_at": row[8],
                "deleted_at": row[9]
            })

        return jsonify(voices)
    except Exception as e:
        print(f"Error fetching voices: {e}")
        return jsonify({"error": str(e)}), 500


# API: Create a voice
@app.route('/voice', methods=['POST'])
def create_voice():
    print("POST /voice was accessed.")
    try:
        data = request.json
        print(f"Request data: {data}")
        
        voice_name = data['voice_name']
        voice_description = data.get('voice_description', '')
        languages = ','.join(data.get('languages', []))
        voice_features = data.get('voice_features', '')
        voicemail_id = data.get('voicemail_id', '')

        conn = get_db_connection()
        print("Database connection established for creating voice.")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO voice (voice_name, voice_description, languages, voice_features, voicemail_id)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """, (voice_name, voice_description, languages, voice_features, voicemail_id))
        voice_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        print(f"Voice created with ID: {voice_id}")

        return jsonify({"id": voice_id, "message": "Voice created successfully"}), 201
    except Exception as e:
        print(f"Error creating voice: {e}")
        return jsonify({"error": str(e)}), 500


# API: Generate TTS
@app.route('/tts', methods=['POST'])
def generate_tts():
    print("POST /tts was accessed.")
    try:
        data = request.json
        print(f"Request data: {data}")
        
        voice_id = data['voice_id']
        model_id = data['model_id']
        text = data['text']
        output_format = data['format']
        speed = data.get('speed', 1.0)
        encoding = data.get('encoding', 'UTF-8')

        # Simulate TTS generation
        response = {
            "voice_id": voice_id,
            "model_id": model_id,
            "text": text,
            "format": output_format,
            "speed": speed,
            "encoding": encoding,
            "audio_url": "https://example.com/generated_audio.mp3"
        }
        print(f"TTS generated: {response}")

        return jsonify(response), 200
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("Starting the Flask application...")
    app.run(debug=True)