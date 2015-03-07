'''
Created on Mar 6, 2015

@author: vencax
'''
from flask import Flask
from datoveschranky import sendmessage
from flask.globals import request
from flask import render_template

app = Flask(__name__)

def _do_send(req):
    recpt = req.form.get('recpt')
    uname = req.form.get('uname')
    pwd = req.form.get('pwd')
    subj = req.form.get('subj')
    attachements = [
        ('text/plain', 'obsah zpravy', req.form.get('content'))
    ]
    return sendmessage.send(recpt, uname, pwd, subj, attachements)


@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():    
    try:
        res = _do_send(request)
        ctx = {'message': res, 'class': 'success'}
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
