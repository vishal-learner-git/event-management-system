from dotenv import load_dotenv
load_dotenv() # Load variables from .env file

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)