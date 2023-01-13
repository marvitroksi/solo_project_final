from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Book:
    db_name = 'books'
    def __init__(self,data):
        self.id = data['id'],
        self.title = data['tittle'],
        self.description = data['description'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    
    @classmethod
    def addBook(cls,data):
        query = 'INSERT INTO books ( tittle, description, user_id ) VALUES ( %(tittle)s, %(description)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    
    @classmethod
    def getBookByID(cls,data):
        query = 'SELECT * FROM books LEFT JOIN users ON books.user_id = users.id WHERE books.id = %(book_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    @classmethod
    def getAllBooks(cls,data):
        query = 'SELECT books.tittle, books.description, books.id, users.first_name, users.last_name, users.id as creator_id FROM books LEFT JOIN users on books.user_id = users.id;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        books = []
        for row in result:
            books.append(row)
        return books

    @classmethod
    def getFavsCount(cls,data):
        query = 'SELECT count(favorites.id) as number FROM favorites LEFT JOIN books ON favorites.book_id = books.id WHERE books.id = %(book_id)s GROUP BY book.id;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    @classmethod
    def favoriteBook(cls,data):
        query = 'INSERT INTO favorites ( book_id, user_id ) VALUES ( %(book_id)s, %(user_id)s ); '
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def unfavoriteBook(cls,data):
        query = 'DELETE FROM favorites WHERE book_id = %(book_id)s AND user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)
    

    @classmethod
    def updateBook(cls,data):
        query = 'UPDATE books SET tittle = %(tittle)s, description = %(description)s WHERE books.id = %(book_id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def favUnfav(cls,data):
        query = 'SELECT book_id as ID FROM favorites left join users on favorites.user_id = users.id  where user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query,data)
        favorites = []
        for row in results:
            favorites.append(row['ID'])
        return favorites
        

    @classmethod
    def getSavedCount(cls,data):

        query = 'SELECT count(books.id) AS number FROM books LEFT JOIN favorites ON books.favorite_id = favorites.id LEFT JOIN users on books.user_id = users.id WHERE books.user_id = %(user_id)s GROUP BY favorites.id;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return 0


    @classmethod 
    def getFavs(cls,data):
        query = 'SELECT users.first_name FROM favorites LEFT JOIN users ON favorites.user_id = users.id WHERE book_id = %(book_id)s GROUP BY users.id;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        books = []
        
        for row in result:
            books.append(row)
        return books
    
    @classmethod
    def deleteFaves (cls,data):
        query = "DELETE FROM favorites WHERE book_id = %(book_id)s;"
        result1 = connectToMySQL(cls.db_name).query_db(query,data)
        print("KTU TE QIFSHA ROPT")
        query2 = "DELETE FROM books WHERE books.id = %(book_id)s"
        result2 = connectToMySQL(cls.db_name).query_db(query2,data)
        print(" O KURVE ZAGREBIIIIIIIIIIIIIIIII")
        return connectToMySQL(cls.db_name).query_db(query,data)



    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book['tittle']) < 2:
            flash("Tittle should be at least 2 characters long", 'tittle')
            is_valid = False
        if len(book['description']) < 10:
            flash("Description should be at least 10 characters  long", 'description')
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_updated_book(book):
        is_valid = True
        if len(book['tittle']) < 3:
            flash("Tittle must have at least 3 characters", 'tittle')
            is_valid = False
        if len(book['description']) < 10:
            flash("Description must have at least 10 characters", 'description') 
            is_valid = False
        return is_valid