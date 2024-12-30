from flask import Flask
from models import init_db

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

if __name__ == "__main__":
    try:
        init_db()
        print("Database and tables initialized!")
    except Exception as e:
        print(f"Error: {e}")
    app.run(debug=True)
