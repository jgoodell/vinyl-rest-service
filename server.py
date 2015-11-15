from flask import Flask
from flask import render_template
from flask import make_response
from flask import redirect
from flask import url_for
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///archive.db'
database = SQLAlchemy(app)

SUPPORTED_CONTENT_TYPES = []


# Models


class Album(database.Model):

    '''Album Model Definition'''
    
    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(512), unique=True)
    artist = database.Column(database.String(512), unique=False)
    year = database.Column(database.Integer, unique=False)

    def __init__(self, title, artist, year):
        self.title = title
        self.artist = artist
        self.year = year

    def __repr__(self):
        return "<Album('%s')>" % self.title


database.create_all()

try:
    database.session.add(Album(title='Pump', artist='Aerosmith', year='1989'))
    database.session.add(Album(title='Permanent Vacation', artist='Aerosmith',
                               year='1987'))
    database.session.add(Album(title='Done With Mirrors', artist='Aerosmith', year='1985'))
    database.session.commit()
except Exception, e:
    print("+="*36)
    print(e)
    print("+="*36)
    database.session.rollback()


# Helper Functions


def _content_type_subroutine(accepted_types):
    
    '''Protected method to figure out Content-Type. If
    no match is found "text/plain" is returned.'''
    
    content_type_default = "text/plain"
    
    for accepted_type in accepted_types:
        for supported_content_type in SUPPORTED_CONTENT_TYPES:
            if accepted_type == supported_content_type:
                return accepted_type
    return content_type_default


def determine_content_type(accept_string):

    '''Determines response content type based
    on Accept header. Returning the Content-Type
    as a string.'''

    return _content_type_subroutine(accept_string.split(','))


# Views


@app.route("/", methods=['GET'])
def root():

    '''View Handler for /'''

    albums = Album.query.all()
    content_type = determine_content_type(request.headers['Accept'])
    
    if request.method == 'GET':
        return render_template('index.html', albums=albums)
    else:
        return make_response(render_template('405.html', method=request.method), 405)


@app.route("/archive/<artist>/<title>/<year>/", methods=['GET', 'PUT', 'POST'])
def album(artist, title, year):

    '''View Handler for /<artist/<title>/<year>/.'''

    content_type = determine_content_type(request.headers['Accept'])
    
    if request.method == 'GET':
        try:
            album = Album.query.filter_by(title=title).one()
        except Exception, e:
            return make_response(render_template('404.html', title=title), 404)
        return render_template('album.html', album=album)
    elif request.method == 'POST':
        try:
            album = Album(artist=artis, title=title, year=int(year))
        except TypeError, e:
            return make_response(render_template('400.html', title=str(e)), 400)
        database.session.add(album)
        database.session.commit()
        return redirect(url_for('root'))
    elif request.method == 'PUT':
        try:
            album = Album.query.filter_by(title=title).one()
        except Exception, e:
            print(e)
            return make_response(render_template('404.html', title=title), 404)
        album.artist = artist
        album.title = title
        album.year = int(year)
        database.session.save(album)
        return redirect(url_for('root'))
    elif request.method == 'DELETE':
        return redirect(url_for('root'))
    else:
        print('BOOM!')
        return make_response(render_template('405.html', method=request.method), 405)
    

if __name__ == "__main__":
    app.run()
