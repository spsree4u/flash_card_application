from flask import Flask, url_for
app = Flask(__name__)

@app.route("/first")
def first_func():
    return url_for('second_func')

@app.route("/second")
def second_func():
    return url_for('first_func') 

if __name__ == '__main__':
  app.run(debug = True)