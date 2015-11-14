from flask import Flask
from flask import render_template
from flask import make_response
from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__)

SUPPORTED_CONTENT_TYPES = []


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
    
    content_type = determine_content_type(request.headers['Accept'])
    
    if request.method == 'GET':
        return render_template('index.html')
    else:
        return make_response(render_template('405.html', method=request.method), 405)


@app.route("/archive/<artist>/<album>/", methods=['GET', 'PUT'])
def album(artist, album):

    '''View Handler for /<artist/<album>/.'''

    content_type = determine_content_type(request.headers['Accept'])
    
    if request.method == 'GET':
        album = {'artist': "Aerosmith", 'title': 'Done with Mirrors',
                 'year': '1985'}
        return render_template('album.html', album=album)
    elif request.method == 'POST':
        return redirect(url_for('root'))
    elif request.method == 'PUT':
        return redirect(url_for('root'))
    elif request.method == 'DELETE':
        return redirect(url_for('root'))
    else:
        return make_response(render_template('405.html'), 405)
    

if __name__ == "__main__":
    app.run()
