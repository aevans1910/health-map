from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/providers/new')
def providers_new():
    """List a new provider"""
    return render_template('providers_new.html')

@app.route('/providers', methods=['POST'])
def providers_submit():
    """Submit a new provider profile"""
    provider = {
        'title' : request.form.get('title'),
        'name' : request.form.get('name'),
        'location' : request.form.get('location'),
        'phone' : request.form.get('phone')
    }
    providers.insert_one(provider)
    return redirect(url_for('providers_index'))

if __name__ == '__main__':
    app.run(debug=True)

