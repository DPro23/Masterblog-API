"""Masterblog Helper functions"""
import json

file_path = 'data/masterblog_posts.json'

def get_posts():
    """Read and return all posts"""
    with open(file_path, 'r', encoding="utf-8") as f_read:
        posts = json.load(f_read)
        f_read.close()
        return posts


def add_post(post):
    """Add a new post"""
    posts = get_posts()
    with open(file_path, 'w', encoding="utf-8") as f_write:
        posts.append(post)
        json.dump(posts, f_write, indent=4)
        f_write.close()


def delete_post(post):
    """Delete a post"""
    posts = get_posts()
    with open(file_path, 'w', encoding="utf-8") as f_delete:
        if post in posts:
            posts.remove(post)
        json.dump(posts, f_delete, indent=4)
        f_delete.close()
