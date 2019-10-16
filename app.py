from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

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
    provider_id = providers.insert_one(provider).inserted_id
    return redirect(url_for('providers_show', provider_id=provider_id)) 

@app.route('/providers/<provider_id>')
def providers_show(provider_id):
    """Show a single provider"""
    provider = providers.find_one({'_id': ObjectId(provider_id)})
    return render_template ('providers_show.html', provider=provider)

@app.route('/providers/<provider_id>/edit')
def providers_edit(provider_id):
    """Show the edit form for a provider"""
    provider = providers.find_one({'_id': ObjectId(provider_id)})
    return render_template('providers_edit.html', provider=provider)

@app.route('/providers/<provider_id>', methods=['POST'])
def providers_update(provider_id):
    """Submit an edited profile"""
    updated_provider = {
        'title': request.form.get('title'),
        'name': request.form.get('name'),
        'location': request.form.get('location'),
        'phone': request.form.get('phone')
    }
    providers.update_one(
        {'_id':ObjectId(provider_id)},
        {'$set': updated_provider})
    return redirect(url_for('providers_show', provider_id=provider_id))


if __name__ == '__main__':
    app.run(debug=True)

