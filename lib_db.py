from sqlalchemy import create_engine, Column, Integer, String , Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from config import DATABASE_CONFIG


DATABASE_URL = DATABASE_CONFIG['driver']+'://'+DATABASE_CONFIG['user']+':'+DATABASE_CONFIG['password']+'@'+DATABASE_CONFIG['host']+'/'+DATABASE_CONFIG['database']


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    created_at = Column(Date)


Base.metadata.create_all(bind=engine)

BookPydantic = sqlalchemy_to_pydantic(Book, exclude=['id'])

def create_book(db_book:BookPydantic):
    db_book = Book(**db_book.dict())
    
    with SessionLocal() as db:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    return db_book
def get_book():
    lib = []
    with SessionLocal() as db:
        books = db.query(Book).all()
        for book in books:
            lib.append({'title': book.title, 'author': book.author, 'genre': book.genre ,'data': book.created_at})
    return lib

def retrieve_book(book_id):
    with SessionLocal() as db:
        retrieved_item = db.query(Book).filter_by(id=book_id).first()
    return {'title': retrieved_item.title, 'author': retrieved_item.author, 'genre': retrieved_item.genre ,'data': retrieved_item.created_at}

def update_book(book_id,item):
    with SessionLocal() as db:
        db_item = db.query(Book).filter(Book.id ==book_id).first()
        for field,value in item.items():
            setattr(db_item,field,value)
        db.commit()
        db.refresh(db_item)
        return db_item
    
def delete_book(book_id):
    with SessionLocal() as db:
        deleted_item = db.query(Book).filter_by(id=book_id).first()
    if deleted_item:
            db.delete(deleted_item)
            db.commit()
            return {'message': f"Item with ID {book_id} deleted successfully"}
    else:
            return {'message': f"Item with ID {book_id} not found"}
    


db_book = BookPydantic(title='Book 2'
, author='author 2', genre='genre 2' , created_at = '1998-07-07')

# print(retrieve_item(2))
# print(update_item(1, {'title': 'Master', 'author': 'Mikle', 'genre': 'Ужас' ,'created_at': '1666-06-06'}))
# create_book(db_book)
# delete_book(1)
# print(get_book())


# Base.metadata.drop_all(bind=engine)