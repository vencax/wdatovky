'''
Created on Mar 6, 2015

@author: vencax
'''
from flask import Flask
from datoveschranky import sendmessage
from flask.globals import request
from flask import render_template
from flask import jsonify
import base64
import datetime
import os

app = Flask(__name__)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(Exception)
def handle_realy_bad_thing(error):
    return str(error)

def _do_send(recpt, uname, pwd, subj, text, attach=[]):
    attachements = []
    if text:
        attachements.append(('text/plain', 'zprava.txt', base64.standard_b64encode(text.encode('utf-8'))))
    for a in attach:
        attachements.append(a)

    res = sendmessage.send(recpt, uname, pwd, subj, attachements)
    try:
        if(int(res.status.dmStatusCode) == 0):
            return (res.status.dmStatusMessage, res.data)
        else:
            raise InvalidUsage(str(res.status))
    except:
        raise InvalidUsage(str(res.status))


@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

def _addMime(attach):
    fname = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open(fname, 'w') as f:
        f.write(base64.standard_b64decode(attach['content']))
        mime = sendmessage.get_mime(fname)
        attach['content_type'] = mime
        os.remove(fname)

def _checkAttachements(atts):
    for a in atts:
        if(not a.get('content_type', None)):
            _addMime(a)
    for a in atts:
        if(not a.get('filename', None)
           or not a.get('content', None)):
            raise InvalidUsage('wrong attachements!')

@app.route('/send', methods=['POST'])
def send():
    try:
        recpt = request.form.get('recpt')
        uname = request.form.get('uname')
        pwd = request.form.get('pwd')
        subj = request.form.get('subj')
        text = request.form.get('content')
        attachment = request.files['attach']
        atts = [(
            attachment.content_type,
            attachment.filename,
            base64.standard_b64encode(attachment.read())
        )] if len(attachment.filename) > 0 else []
        res = _do_send(recpt, uname, pwd, subj, text, atts)
        m = "%s, ID zpravy: %s" % (res[0], str(res[1]))
        ctx = {'message': m, 'class': 'success'}
    except Exception, e:
        ctx = {'message': e, 'class': 'alert'}
        import traceback
        traceback.print_exc()

    return render_template('index.html', **ctx)

@app.route('/api', methods=['POST'])
def send_ajax():
    if(request.content_type != 'application/json'):
        raise InvalidUsage('only json encoded data suported')
    if('attach' in request.json):
        _checkAttachements(request.json['attach'])
        request.json['attach'] = [(
            a['content_type'], a['filename'], a['content']
        ) for a in request.json['attach']]
    res = _do_send(**request.json)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0')
