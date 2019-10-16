from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def index():
    """Returns homepage"""
    return render_template ('home.html', msg='Health map!')

if __name__ == '__main__':
    app.run(debug=True)

