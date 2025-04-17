from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
from github_utils import clone_and_parse_repo
from ai_writer import generate_blog

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/generate-blog', methods=['POST'])
def generate_blog_route():
    try:
        data = request.json
        repo_url = data.get('repo_url')
        
        if not repo_url:
            logger.warning("Request received without repo_url")
            return jsonify({"error": "Repository URL not provided"}), 400
        
        logger.info(f"Processing request for repository: {repo_url}")
        
        # Clone and parse the repository
        try:
            metadata = clone_and_parse_repo(repo_url)
        except Exception as e:
            logger.error(f"Error in clone_and_parse_repo: {str(e)}")
            return jsonify({"error": f"Failed to clone or parse repository: {str(e)}"}), 500
        
        # Generate the blog post
        try:
            blog_md = generate_blog(metadata)
            return jsonify({"blog": blog_md})
        except Exception as e:
            logger.error(f"Error in generate_blog: {str(e)}")
            return jsonify({"error": f"Failed to generate blog post: {str(e)}"}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True, host='0.0.0.0')