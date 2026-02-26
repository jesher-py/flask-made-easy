from flask import Flask, g
import sqlite3

DATABASE = 'database.db'

# initializing the app
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def home():
    #home page
    
    sql = """
            select cars.carID, cars.model, makers.name, cars.imgURL
            from cars
            join makers on cars.makerID = makers.makerID;"""
    
    results = query_db(sql)
    return str(results)

@app.route('/car/<int:carID>')
def car(carID):
    # just on car based on id
    sql = """ SELECT * FROM cars join makers on makers.makerID = cars.makerID
            WHERE cars.carID = ?;"""
    result = query_db(sql,(carID,),True)
    return str(result)



if __name__ == '__main__':
    app.run(debug=True)
