from flask import Flask

from routes.main_routes import main_bp
from routes.resume_routes import resume_bp
from routes.history_routes import history_bp
from routes.dashboard_routes import dashboard_bp
from routes.auth_routes import auth_bp

from models.database import init_db

app = Flask(__name__)

# SECRET KEY (SESSION)
app.secret_key = "resume_analyzer_secret_key_123"

# INITIALIZE DATABASE
init_db()

# REGISTER BLUEPRINTS
app.register_blueprint(main_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(history_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp)

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)