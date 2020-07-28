from flask import Flask,jsonify,request
import sqlite3
companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
org = [{"id": 1, "name": "TestOrg"}, {"id": 2, "name": "TestOrg2"}]
bookshelf = [{"id": 1, "name": "TestOrg"}, {"id": 2, "name": "TestOrg2"}]
books = [{"id": 1,"title": "A Fire Upon the Deep","author": "Vernor Vinge","first_sentence": "The coldsleep itself was dreamless.","published": "1992"},
         {"id": 2,
          "title": "The Ones Who Walk Away From Omelas",
          "author": "Ursula K. Le Guin",
          "first_sentence": "With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.",
          "published": "1973"},
         {"id": 4,
          "title": "Dhalgren",
          "author": "Samuel R. Delany",
          "first_sentence": "to wound the autumnal city.",
          "published": "1975"}]
api = Flask(__name__)
api.config["DEBUG"] = True
def dict_factory(cursor,row):
    d={}
    for idx,col in enumerate (cursor.description):
        d[col[0]]=row[idx]
    return d
@api.route('/api/v1/books/all',methods=['GET'])
def fromdb():
    conn = sqlite3.connect('books.db')
    conn.row_factory=dict_factory
    cur =conn.cursor()

    all_books =cur.execute('SELECT * FROM BOOKS;').fetchall()
    return jsonify(all_books)
@api.route('/api/v1/resources/books',methods=['GET'])
def fromdb_filter():
    conn = sqlite3.connect('books.db')
    conn.row_factory=dict_factory
    cur =conn.cursor()
    query_params =request.args
    id1 =query_params.get('id')
    published =query_params.get('published')
    author =query_params.get('author')
    title =query_params.get('title')
    query ="SELECT * FROM BOOKS WHERE"
    to_filter = []
    if id1 :
        query +=' id=? AND'
        to_filter.append(id1)
        print('id1 ',id1)
    if published:
        query +=' published=? AND'
        to_filter.append(published)
    if author:
        query +=' author=? AND'
        to_filter.append(author)
    if title:
        query +=' title=? AND'
        to_filter.append(title)
    if not (id1 or published or author or title):
        return page_not_found(404)
    query =query[:-4]+';'
    print('query is', query)
    print('filter is ',to_filter)
    results =cur.execute(query,to_filter).fetchall()
    return jsonify(results)
@api.route('/test', methods=['GET'])
def get_companies():
    return jsonify(companies)
@api.route('/test1', methods=['POST'])
def get_org():
    return jsonify(org),201
@api.errorhandler(404)
def page_not_found(error):
    return "This path / api  does not exist in Flask"
@api.route('/')
def index():
    return "Hello User welcome to my API - Ezhil"
@api.route('/api/books/all',methods=['GET'])
def books1():
    return jsonify(books)
@api.route('/api/books/',methods=['GET'])
def book_id():
    if 'id' in request.args:
        id =int(request.args['id'])
    else:
        return "No Book ID provided in the URL"
    results =[]
    for book in books:
        if book['id']==id:
            results.append(book)

    return jsonify(results)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=80)