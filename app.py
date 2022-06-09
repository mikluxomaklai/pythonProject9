import logging

from flask import Flask, send_from_directory

from main.views import main_blueprint
from loaders.views import loader_blueprint
import loggers


POST_PATH = "data/posts.json"
UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)

app.config["POST_PATH"] = "data/posts.json"
app.config["UPLOAD_FOLDER"] = "uploads/images"

loggers.create_logger()

logger = logging.getLogger("basic")

@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)

logger.info("Приложение запускается")

app.run(debug=True)
