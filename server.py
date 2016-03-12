'''
Created on Mar 6, 2015

@author: vencax
'''
from flask import Flask
from datoveschranky import sendmessage
from flask.globals import request
from flask import render_template
import base64

app = Flask(__name__)


def _do_send(req):
    recpt = req.form.get('recpt')
    uname = req.form.get('uname')
    pwd = req.form.get('pwd')
    subj = req.form.get('subj').encode('utf-8')
    cont = base64.standard_b64encode(req.form.get('content').encode('utf-8'))
    attachements = [
        ('text/plain', 'zprava.txt', cont)
    ]
    if 'attach' in req.files:
        attach = req.files['attach']
        if attach.content_length > 0:
            attachements.append((
                attach.content_type,
                attach.filename,
                base64.standard_b64encode(attach.read())
            ))
    res = sendmessage.send(recpt, uname, pwd, subj, attachements)
    return (res.status.dmStatusMessage, res.data)


@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    try:
        res = _do_send(request)
        m = "%s, ID zpravy: %s" % (res[0], str(res[1]))
        ctx = {'message': m, 'class': 'success'}
    except Exception, e:
        ctx = {'message': e, 'class': 'alert'}
        import traceback
        traceback.print_exc()
    
    return render_template('index.html', **ctx)

@app.route('/send', methods=['POST'])
def send_ajax():
    try:
        return _do_send(request)
    except Exception, e:
        return e

    
if __name__ == '__main__':
    app.run(host='0.0.0.0')
