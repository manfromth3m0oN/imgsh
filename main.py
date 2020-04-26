from flask import Flask, render_template, request, redirect
import redis
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
db = redis.Redis(host='localhost', port=6379, db=0)

current_milli_time = lambda: int(round(time.time() * 1000))

@app.route('/')
def index():
    top = db.scan(count=9)[1]
    return render_template('index.html', posts=top)

@app.route('/all')
def all():
    ret = ''
    scan = db.scan()[1]
    for i in scan:
        ret = ret + '<a href="./static/storage/'+i.decode()+'">'+i.decode()+'</a><br/>'
    return ret

@app.route('/<id>')
def img(id):
    time = db.get(id)
    return render_template('img.html', id=id, time=time)

@app.route('/uupload')
def uploadpage():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['img']
    file.save('./static/storage/' + secure_filename(file.filename))
    db.set(secure_filename(file.filename), current_milli_time())
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
