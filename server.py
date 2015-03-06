'''
Created on Mar 6, 2015

@author: vencax
'''
from flask import Flask
from datoveschranky import sendmessage
from flask.globals import request
from flask import render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():    
    recpt = request.form.get('recpt')
    uname = request.form.get('uname')
    pwd = request.form.get('content')
    subj = request.form.get('content')
    attachements = [
        ('text/plain', 'obsah zpravy', request.form.get('content'))
    ]
    try:
        res = sendmessage.send(recpt, uname, pwd, subj, attachements)
        ctx = {'message': res, 'class': 'success'}
    except Exception, e:
        ctx = {'message': e, 'class': 'alert'}
    
    return render_template('index.html', **ctx)
    
if __name__ == '__main__':
    app.run()