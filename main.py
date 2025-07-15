from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Comment-to-DM Bot is Live!"

# Add your other bot routes here

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's dynamic port
    app.run(host='0.0.0.0', port=port)        # Bind to 0.0.0.0 for external access
