from flask import Flask, make_response, jsonify, session
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

@app.route('/articles')
def index_articles():
    """Return all articles as JSON"""
    articles = Article.query.all()
    articles_list = [
        {
            'id': a.id,
            'author': a.author,
            'title': a.title,
            'content': a.content,
            'preview': a.preview,
            'minutes_to_read': a.minutes_to_read,
            'date': a.date
        }
        for a in articles
    ]
    return jsonify(articles_list), 200

@app.route('/articles/<int:id>')
def show_article(id):
    """Return single article, limit 3 page views per session"""
    # Initialize or increment page views
    session['page_views'] = session['page_views'] + 1 if 'page_views' in session else 1

    # Paywall: limit to 3 views
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    # Fetch article from database
    article = Article.query.get(id)
    if not article:
        return jsonify({'message': 'Article not found'}), 404

    return jsonify({
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date
    }), 200

if __name__ == '__main__':
    app.run(port=5555)
