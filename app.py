from flask import Flask, request, session, render_template, g, url_for,redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == '123456':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))
    if g.user:
        return redirect(url_for('protected'))

    return render_template('index.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html', userlogon = g.user)
    return redirect(url_for('index'))

@app.route('/getsession')
def getsession():
    if 'user' in session:
        return session['user']
    return 'Not Login'

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


