from flask import request, Flask, render_template

from page import Page
from website import Website
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from base import Base

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about/')
def about():
    html = "I am galin the relef!"
    return html


@app.route('/search/')
def search():
    searchword = request.args.get('search_text', '')
    engine = create_engine("sqlite:///searchengine.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    pages = session.query(Page).filter(Page.title.like(
        "%" + searchword + "%")).all()

    return render_template("search.html", pages=pages)


if __name__ == '__main__':
    app.run(debug=True)
