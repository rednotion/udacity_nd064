import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
from datetime import datetime
import logging

# Set logging config
logging.basicConfig(filename='app.log',level=logging.DEBUG)


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    #n_connections += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()

    # log if post
    timestamp = datetime.now()
    if post:
        log = f"{timestamp}: Article '{post['Title']}' retrieved"
    else:
        log = f"{timestamp}: Article not found, 404 returned"
    logging.info(log)
    print(log)

    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      return render_template('404.html'), 404
    else:
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    timestamp = datetime.now()
    log = f"{timestamp}: 'About Us' page was retrieved"
    logging.info(log)
    print(log)

    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            timestamp = datetime.now()
            log = f"{timestamp}: New article with title '{title}' was created"
            logging.info(log)
            print(log)

            return redirect(url_for('index'))

    return render_template('create.html')

# Healthcheck endpoint
@app.route('/healthz')
def healthcheck():
    response = app.response_class(
        response=json.dumps("result: OK - healthy"),
        status=200,
        mimetype="application/json"
    )
    logging.info("Status 200 OK")

    return response


# Metrics endpoint
@app.route('/metrics')
def metrics():
    
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    metric_body = {
        "db_connection_count": n_connections,
        "post_count": len(posts), 
    }
    response = app.response_class(
        response=json.dumps(metric_body),
        status=200,
        mimetype="application/json"
    )

    return response


# start the application on port 3111
if __name__ == "__main__":
   #n_connections=0
   app.run(host='0.0.0.0', port='3111')
