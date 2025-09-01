from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.json.sort_keys = False # Avoid sorting keys a-z
CORS(app)  # This will enable CORS for all routes

POSTS = []


@app.errorhandler(400)
def bad_requests(error):
    """Return a custom 400 error."""
    return jsonify(error), 400

@app.errorhandler(404)
def not_found(error):
    """Return a custom 404 error."""
    return jsonify(error), 404

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """GET returns all posts, POST add a new one."""
    if request.method == 'POST':
        try:
            body = request.get_json()

            # Check for empty fields
            for field, value in body.items():
                if str(value).strip() == "":
                    raise ValueError(f"Required '{field}' is empty.")

            # New Post ready to add with AutoIncrementing ID
            new_posts = {
                "id": POSTS[-1]["id"] + 1 if len(POSTS) > 0 else 1,
                "title": str(body["title"]),
                "content": str(body["content"])
            }

            # Adds new post to the posts list
            POSTS.append(new_posts)

        # Handle missing or empty fields
        except KeyError as key_error:
            return f'Missing field: {key_error}', 400

        except ValueError as value_error:
            return f'Empty field: {value_error}', 400

        return jsonify(new_posts), 201

    # GET request returns the posts list
    return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def delete_post(post_id):
    """DELETE or UPDATE a post by its id"""
    for post in POSTS:
        if post["id"] == post_id:
            if request.method == "DELETE":
                POSTS.remove(post)
                success_msg = f"Post with id {post_id} has been deleted successfully."

                # Deleted successfully
                return jsonify({"message": success_msg}), 200

            elif request.method == "PUT":
                body = request.get_json()

                for field in body.keys():
                    if field == 'content' or field == 'title':
                        if str(body[field]).strip() != "":
                            post[field] = str(body[field])

                # Updated successfully
                return jsonify(post), 200

    # If post_id is not found in posts list
    return f"Post with id {post_id} was not found.", 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
