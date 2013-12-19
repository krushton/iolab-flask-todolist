import os,json
from flask import Flask,render_template,g,request,Response
from sqlite3 import dbapi2 as sqlite3

''' ------------------------------- setup and initialize app ------------------------------- '''

app = Flask(__name__)
app.config.update(dict(
    DATABASE='todos.db',
    DEBUG=True,
    USERNAME='admin',
    PASSWORD='default'
))


''' ------------------------------- your routes go here ------------------------------- '''

@app.route('/')
def index():
    todos = get_all()
    return render_template('index.html')

@app.route('/todos', methods=['GET'])
def all():
    todos = get_all()
    resp = Response(response=json.dumps(todos), status=200, mimetype="application/json")
    return resp

@app.route('/todos', methods=['POST'])
def add():
    todo = request.form
    new_id = add_new(todo)
    resp = Response(response=json.dumps({ 'id': new_id}), status=200, mimetype="application/json")
    return resp
 
@app.route('/todos/<id>', methods=['POST'])
def update_todo(id):
    new_todo = request.form
    todo = update(id, new_todo)
    resp = Response(response=json.dumps({'message': 'success'}), status=200, mimetype="application/json")
    return resp

@app.route('/todos/<id>', methods=['DELETE'])
def remove(id):
    delete(id)
    resp = Response(response=json.dumps({'message': 'success'}), status=200, mimetype="application/json")
    return resp
    
''' ------------------------------- helper functions for accessing database ------------------------------- '''
def get_by_id(todo_id):
    ''' returns a dictionary representation of the todo with the id todo_id '''
    db = get_db()
    cur = db.execute('SELECT * FROM todos WHERE rowid = ?', [todo_id])
    return cur.fetchone()

def get_all():
    '''returns an array of todos'''
    db = get_db()
    cur = db.execute('SELECT * FROM todos ORDER BY id DESC')
    return cur.fetchall()

def add_new(item):
    '''create todo with the values in item (a dictionary). returns the id of the newly added todo '''
    db = get_db()
    placeholders = ', '.join(['?'] * len(item))
    columns = ', '.join(item.keys())

    query = 'INSERT INTO todos (%s) VALUES (%s)' % (columns, placeholders)
    cur = db.execute(query, item.values())
    new_item_id  = cur.lastrowid
    db.commit()
    return new_item_id

def update(todo_id, item):
    '''update todo with the id todo_id with the values in item (a dictionary)'''
    db = get_db()
    for key,val in item.iteritems():
        query = 'UPDATE todos SET %s = ? WHERE rowid = ?' % (key)
        db.execute(query, [val, todo_id])
        db.commit()

def delete(todo_id):
    '''delete todo with the id todo_id''' 
    db = get_db()
    cur = db.cursor().execute('DELETE FROM todos WHERE rowid = ?', [int(todo_id)])
    db.commit()

def dict_factory(cursor, row):
    """ Makes sqlite3 return dictionaries instead of row objects."""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    """Connects to the specific database."""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = dict_factory
    return conn

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)  


