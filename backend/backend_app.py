"""Serve a RESTful API + Swagger UI."""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from OnMasterblog.main import get_posts, add_post, delete_post, update_post

SWAGGER_URL="/api/docs"  # swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # API Schema

# Define swagger UI
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API'
    }
)

app = Flask(__name__) # Instantiate flask app
app.json.sort_keys = False # Enable custom sorting
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL) # Create Swagger UI
CORS(app)  # Enable CORS for all routes


@app.errorhandler(400)
def bad_requests(error):
    """Return a custom 400 error."""
    return jsonify(error), 400


@app.errorhandler(404)
def not_found(error):
    """Return a custom 404 error."""
    return jsonify(error), 404


@app.route('/api/posts', methods=['GET', 'POST'])
def read_or_add_posts():
    """GET returns all posts, POST add a new one."""
    try:
        if request.method == 'POST':
            posts = get_posts()
            body = request.get_json()

            # Check for empty fields
            for field, value in body.items():
                if field == 'title' or field == 'content':
                    if str(value).strip() == "":
                        raise ValueError(f"Required '{field}' is empty.")
                else:
                    raise KeyError(f"Required '{field}' is missing.")

            # New Post ready to add with AutoIncrementing ID
            new_posts = {
                "id": posts[-1]["id"] + 1 if len(posts) > 0 else 1,
                "title": str(body["title"]),
                "content": str(body["content"])
            }

            # Adds new post to the posts list
            add_post(new_posts)
            #posts.append(new_posts) # with mocked data

            return jsonify(new_posts), 201

        # GET request returns a sorted posts list
        # sorted by id ASC by default
        posts = get_posts()
        sort = request.args.get('sort')
        direction = request.args.get('direction')
        allowed_sorts = {'title', 'content'}
        allowed_directions = {'asc', 'desc'}

        # Return original Posts list if
        # one or both allowed params are missing
        if sort is None and direction is None:
            return jsonify(posts)

        # Return custom BadRequest for not allowed values
        if str(sort) not in allowed_sorts:
            return f'Sorting by {sort} is not allowed', 400

        if str(direction) not in allowed_directions:
            return f'Direction {direction} is not allowed', 400

        # Returns a new list sorted via query params
        sorted_posts = sorted(posts, key=lambda x: x[sort], reverse=direction == 'desc')
        return jsonify(sorted_posts)

    # Handle missing or empty fields
    except KeyError as key_error:
        return f'Missing field: {key_error}', 400

    except ValueError as value_error:
        return f'Empty field: {value_error}', 400

    except Exception as error:
        return f'Something went wrong: {error}', 500


@app.route('/api/posts/<int:post_id>', methods=['DELETE', 'PUT'])
def delete_or_update_post(post_id):
    """DELETE or UPDATE a post by its id"""
    try:
        posts = get_posts()
        for post in posts:
            if post["id"] == post_id:
                # Delete post
                if request.method == "DELETE":
                    delete_post(post)
                    success_msg = f"Post with id {post_id} has been deleted successfully."

                    # Deleted successfully
                    return jsonify({"message": success_msg}), 200

                # Update post
                elif request.method == "PUT":
                    body = request.get_json()

                    for field in body.keys():
                        if field == 'content' or field == 'title':
                            if str(body[field]).strip() != "":
                                post[field] = str(body[field])

                    update_post(post)
                    # Updated successfully
                    return jsonify(post), 200

        # when there isn't any post with id == post_id
        return f"Post with id {post_id} was not found.", 404

    except Exception as error:
        return f"An error occurred: {error}", 500


@app.route('/api/posts/search')
def search_post():
    """Returns all post matching the research"""
    try:
        posts = get_posts()
        title = request.args.get('title')
        content = request.args.get('content')
        unique_filtered_posts = {}

        # Use idx to avoid duplicated
        for idx, post in enumerate(posts):
            if title is not None and str(title).lower() in post["title"].lower():
                unique_filtered_posts[idx] = post
            if content is not None and str(content).lower() in post["content"].lower():
                unique_filtered_posts[idx] = post

        # Create a list of unique posts from a dictionary
        filtered_posts = list(unique_filtered_posts.values())
        return jsonify(filtered_posts), 200

    except Exception as error:
        return f"An error occurred: {error}", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
