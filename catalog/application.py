from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog of Items"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                        json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2 class="welcome-font">Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 200px; height: 200px;border-radius: 150px; '
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    return output


def createUser(login_session):
    '''Adds the current user to database'''

    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    '''Gets user information for the given user_id'''

    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    '''Gets User ID for that user's Email ID from database'''

    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return render_template('logout.html')
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/catalog/')
def showCategories():
    '''Renders the data to be shown on the Catalog page'''

    categories = session.query(Category).all()
    latest_items = session.query(CatalogItem)\
        .order_by(CatalogItem.created_date.desc())\
        .limit(10).all()
    return render_template('catalog.html', categories=categories,
                           latest_items=latest_items,
                           login_session=login_session)


@app.route('/catalog/<string:category_name>/items/')
def showItems(category_name):
    '''Renders the data to be shown on the page that shows Items
    for that category name'''

    categories = session.query(Category).all()
    items = session.query(CatalogItem).filter_by(category_name=category_name)\
        .all()
    return render_template('items.html', category_name=category_name,
                           items=items, categories=categories,
                           login_session=login_session)


@app.route('/catalog/add/', methods=['GET', 'POST'])
def addItem():
    '''Allows user to add an Item'''

    # If User is not logged in, show log in page instead of add page.
    if 'username' not in login_session:
        return redirect('/login')
    # If User is logged in and sends POST request, save the item added
    # in database.
    if(request.method == 'POST' and request.form['title']):
        newItem = CatalogItem(title=request.form['title'],
                              description=request.form['description'],
                              category_name=request.form['category'],
                              user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash('New Item %s Successfully Added' % newItem.title)
        return redirect(url_for('showCategories'))
    # If User is logged in and sends GET request, show him form to add item.
    else:
        categories = session.query(Category).all()
        return render_template('addItem.html', categories=categories)


@app.route('/catalog/<string:category_name>/<string:item_name>/')
def showItemDetails(category_name, item_name):
    '''Renders the data to be shown on the page that shows the item details
    for that item name'''

    itemDetails = session.query(CatalogItem).filter_by(title=item_name).one()
    creator = getUserInfo(itemDetails.user_id)
    return render_template('itemDetails.html', itemDetails=itemDetails,
                           login_session=login_session, creator=creator)


@app.route('/catalog/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(item_name):
    '''Allows user to edit an Item'''

    # If User is not logged in, show log in page instead of edit page.
    if 'username' not in login_session:
        return redirect('/login')
    # If User is logged in and sends POST request, save the item updated
    # in database.
    if(request.method == 'POST'):
        editedItem = session.query(CatalogItem).filter_by(title=item_name)\
            .one()
        if(request.form['title']):
            editedItem.title = request.form['title']
        if(request.form['description']):
            editedItem.description = request.form['description']
        editedItem.category_name = request.form['category']
        session.add(editedItem)
        session.commit()
        flash('Item %s Successfully Edited' % editedItem.title)
        return redirect(url_for('showItemDetails',
                                category_name=editedItem.category_name,
                                item_name=editedItem.title))
    # If User is logged in and sends GET request, show him form to edit item.
    else:
        categories = session.query(Category).all()
        item = session.query(CatalogItem).filter_by(title=item_name).one()
        return render_template('editItem.html', categories=categories,
                               item=item)


@app.route('/catalog/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(item_name):
    '''Allows user to delete an Item'''

    # If User is not logged in, show log in page instead of delete page.
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(CatalogItem).filter_by(title=item_name).one()
    # If User is logged in and sends POST request, save the item deleted
    # in database.
    if(request.method == 'POST'):
        session.delete(itemToDelete)
        session.commit()
        flash('Item %s Successfully Deleted' % item_name)
        return redirect(url_for('showItems',
                                category_name=itemToDelete.category_name))
    # If User is logged in and sends GET request, show him form to delete item.
    else:
        return render_template('deleteItem.html', item_name=item_name)


@app.route('/catalog.json')
def catalogJSON():
    '''Renders JSON endpoint details for the catalog of items'''

    catalog = session.query(Category).all()
    categories = []
    for c in catalog:
        new_categories = c.serialize
        itemsCatalog = session.query(CatalogItem)\
            .filter_by(category_name=c.name).all()
        items = []
        for i in itemsCatalog:
            items.append(i.serialize)
        new_categories['items'] = items
        categories.append(new_categories)
    return jsonify(catalog=[categories])

if(__name__ == '__main__'):
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
