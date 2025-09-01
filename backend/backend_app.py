from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False
CORS(app)  # This will enable CORS for all routes

POSTS = []


@app.errorhandler(400)
def bad_requests(error):
    """Return a custom 400 error."""
    return jsonify(error), 400


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """GET returns all posts, POST add a new one."""
    if request.method == 'POST':
        body = request.get_json()

        # Check for missing fields
        try:
            # Check for empty values
            for field, value in body.items():
                if value.strip() == "":
                    raise ValueError(f"Required '{field}' is empty.")

            # New Post ready to add with AutoIncrementing ID
            new_posts = {
                "id": POSTS[-1]["id"] + 1 if len(POSTS) > 0 else 1,
                "title": str(body["title"]),
                "content": str(body["content"])
            }

            # Adds new post to the posts list
            POSTS.append(new_posts)

        # Handle missing fields or empty values
        except KeyError as key_error:
            return f'Missing field: {key_error}', 400

        except ValueError as value_error:
            return f'Invalid field: {value_error}', 400

        return jsonify(new_posts), 201

    # GET request returns the posts list
    return jsonify(POSTS)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
