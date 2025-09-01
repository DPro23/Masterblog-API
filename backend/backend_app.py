"""Serve a RESTful API"""
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

    # GET request returns a sorted posts list
    # sorted by id ASC by default
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    allowed_sorts = {'title', 'content'}
    allowed_directions = {'asc', 'desc'}

    # Return original Posts list if
    # one or both allowed params are missing
    if sort is None and direction is None:
        return jsonify(POSTS)

    # Return custom BadRequest for not allowed values
    if str(sort) not in allowed_sorts:
        return f'Sorting by {sort} is not allowed', 400

    if str(direction) not in allowed_directions:
        return f'Direction {direction} is not allowed', 400

    # Returns a new list sorted via query params
    sorted_posts = sorted(POSTS, key=lambda x: x[sort], reverse=direction == 'desc')
    return jsonify(sorted_posts)


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


@app.route('/api/posts/search')
def search_post():
    """Returns all post matching the research"""
    title = request.args.get('title')
    content = request.args.get('content')
    unique_filtered_posts = {}

    # Use idx to avoid duplicated
    for idx, post in enumerate(POSTS):
        if title is not None and str(title).lower() in post["title"].lower():
            unique_filtered_posts[idx] = post
        if content is not None and str(content).lower() in post["content"].lower():
            unique_filtered_posts[idx] = post

    # Create a list of unique posts from a dictionary
    filtered_posts = list(unique_filtered_posts.values())
    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
