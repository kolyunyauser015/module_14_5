import sqlite3


def initiate_db():
    connection = sqlite3.connect('products_data.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,        
        description TEXT,    
        price INTEGER NOT NULL    
        );    
        ''')
    connection.commit()
    connection.close()

    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,        
            email TEXT NOT NULL,
            age INTEGER NOT NULL,    
            balance INTEGER NOT NULL    
            );    
            ''')
    connection.commit()
    connection.close()


def add_products(title_product, description, price):
    connection = sqlite3.connect('products_data.db')
    cursor = connection.cursor()
    check_product = cursor.execute(
        "SELECT * FROM Products WHERE title=?",
        (title_product,)
    )
    if check_product.fetchone() is None:
        cursor.execute(f'''
            INSERT INTO Products(title, description, price) VALUES(
            '{title_product}',
            '{description}',
            '{price}'
            )
        ''')
    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    cursor.execute(f'''
                INSERT INTO Users(username, email, age, balance) VALUES(
                '{username}',
                '{email}',
                '{age}',
                '{1000}'
                )
        ''')
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('users_data.db')
    cursor = connection.cursor()
    check_user = cursor.execute(
        "SELECT * FROM Users WHERE username=?",
        (username,)
    )
    result = bool(check_user.fetchone())
    connection.commit()
    connection.close()
    return result


def get_all_products():
    connection_product = sqlite3.connect('products_data.db')
    cursor_product = connection_product.cursor()
    cursor_product.execute("SELECT * FROM Products")
    all_products = cursor_product.fetchall()
    connection_product.commit()
    connection_product.close()
    return all_products


initiate_db()
