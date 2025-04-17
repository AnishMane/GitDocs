from flask import Flask, request, jsonify
from flask_cors import CORS
from github_utils import clone_and_parse_repo
from ai_writer import generate_blog

app = Flask(__name__)
CORS(app)

@app.route('/generate-blog', methods=['POST'])
def generate_blog_route():
    try:
        data = request.json
        repo_url = data.get('repo_url')
        if not repo_url:
            return jsonify({"error": "Repo URL not provided"}), 400

        metadata = clone_and_parse_repo(repo_url)
        blog_md = generate_blog(metadata)

        return jsonify({"blog": blog_md})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
