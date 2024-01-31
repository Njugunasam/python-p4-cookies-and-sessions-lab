#!/usr/bin/env python3

from flask import Flask, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Set initial page_views value to 0 if this is the first request
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views for every request
    session['page_views'] += 1
    
    # Retrieve the article by ID
    article = Article.query.get(id)

    if session['page_views'] <= 3:
        # Render JSON response with article data
        return jsonify({
            'article_id': article.id,
            'title': article.title,
            'content': article.content,
            'author': article.author,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date.isoformat(),
            'user_id': article.user_id
        })
    else:
        # Render JSON response with an error message and status code 401
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
