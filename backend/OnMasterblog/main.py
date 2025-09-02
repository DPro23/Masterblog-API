"""Masterblog Helper functions"""
import json

file_path = 'data/masterblog_posts.json'

def _save_data(posts):
    """
    Save posts to a json file
    """
    with open(file_path, 'w', encoding="utf-8") as f_write:
        json.dump(posts, f_write, indent=4)
        f_write.close()


def get_posts():
    """Read and return all posts"""
    with open(file_path, 'r', encoding="utf-8") as f_read:
        posts = json.load(f_read)
        f_read.close()
        return posts


def add_post(post):
    """Add a new post"""
    posts = get_posts()
    posts.append(post)
    _save_data(posts)


def delete_post(post):
    """Delete a post"""
    posts = get_posts()
    if post in posts:
        posts.remove(post)
    _save_data(posts)

def update_post(updated_post):
    """Update a post"""
    posts = get_posts()
    for idx, post in enumerate(posts):
        if updated_post['id'] == post['id']:
            posts[idx] = post
    _save_data(posts)
