from flask import Flask , jsonify , request

from lib_db import *

app = Flask(__name__)

@app.route("/get_books/" , methods = ['GET'])
def get_items():
    books = get_book()
    return jsonify({'data':books})

@app.route("/create_book/", methods= ['POST'])
def create_book_rq():
    data = request.get_json()
    book = BookPydantic(
        title = data.get('title', 'no title'),
        author = data.get('author', 'no author'),
        genre = data.get('genre', 'no genre'),
        created_at= data.get('created_at' , '2000-01-01')
    )
    create_book(book)
    return jsonify({'message': 'created sucsessfuly'}) 

@app.route("/retrieve_book/<int:book_id>/", methods= ['GET'])
def get_one_book(book_id):
    book = retrieve_book(book_id)
    if not book:
        return jsonify({'message': 'not found'})
    return jsonify({'data':book})

@app.route("/update_book/<int:book_id>/", methods= ['PUT'])
def update_book_rq(book_id):
    try:
        data = request.get_json()
        update_book(book_id, data)
        return 'Update Successfully'
    except:
        return 'Data was a uncoorrect'

@app.route("/delete_book/<int:book_id>/", methods= ['DELETE'])
def delete_book_fk(book_id):
    try:
        delete_book(book_id)
        return f'this item whith {book_id} was delete'
    except:
        return 'no such ID exist'

app.run(host='localhost', port=8000)

