from flask import Flask, render_template

app=Flask(__name__)

#Mock array of providers
providers = [
    {'title': 'DC', 'name': 'Lafferty'},
    {'title': 'DDS', 'name': 'Rones'}
]

@app.route('/')
def providers_index():
    """Show all providers"""
    return render_template ('providers_index.html', providers=providers)

if __name__ == '__main__':
    app.run(debug=True)

