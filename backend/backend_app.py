from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = []


@app.errorhandler(400)
def missing_fields(_e):
    """Doesn't allow missing fields."""
    return jsonify({"Bad Request: Missing fields"}), 400


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """Shows all posts and can add a new one."""
    if request.method == 'POST':
        body = request.get_json()

        # Don't allow missing required fields
        if not body["title"] or not body["content"]:
            return 'Missing fields!', 400

        new_posts = {
            "id": POSTS[-1]["id"] + 1 if len(POSTS) > 0 else 1,
            "title": body["title"],
            "content": body["content"]
        }
        # Adds new post to the posts list
        POSTS.append(new_posts)
        return jsonify(new_posts), 201
    # GET request returns a list of posts
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
