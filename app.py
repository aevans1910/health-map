from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Health_Map
providers = db.providers

app=Flask(__name__)

#Mock array of providers
# providers = [
#     {'title': 'DC', 'name': 'Lafferty'},
#     {'title': 'DDS', 'name': 'Rones'}
# ]

@app.route('/')
def providers_index():
    """Show all providers"""
    return render_template ('providers_index.html', providers=providers.find())

if __name__ == '__main__':
    app.run(debug=True)

