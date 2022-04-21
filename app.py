
from flask import Flask, redirect , render_template , request, url_for
app = Flask(__name__)

@app.route('/' , methods=['post' , 'get'])
def welcome():
    if request.method=='POST':
        return redirect(url_for('ide'))
    else:
        return render_template('base.html')

@app.route('/ide')
def ide():
    return render_template('ide.html')

app.run(debug=True)