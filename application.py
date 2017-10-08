from flask import Flask, render_template, request, redirect, jsonify
from flask import session, make_response, url_for, flash
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Item, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import random
import string
import requests

app = Flask(__name__)

engine = create_engine('sqlite:///categories.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session_db = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Web client 1"


# This function is used to disconnect the user from his or her
# google account
@app.route('/gdisconnect', methods=['GET', 'POST'])
def gdisconnect():
    access_token = session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps
                                 ('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % session[
          'access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del session['access_token']
        del session['gplus_id']
        del session['username']
        del session['email']
        del session['picture']
        response = make_response(json.dumps
                                 ('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps
                                 ('Failed to revoke token for given user.',
                                  400))
        response.headers['Content-Type'] = 'application/json'
    return response


# This function is used to login the user useing his or her
# google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != session['state']:
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

    stored_access_token = session.get('access_token')
    stored_gplus_id = session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    session['username'] = data['name']
    session['picture'] = data['picture']
    session['email'] = data['email']

    output = 'Successfully connected.'
    return output


# this function respoinds to the catalog.json URI and displays all
# catalog items in JSON format to the user
@app.route('/catalog.json')
def cateogryItemJSON():
    result = []
    catagories = session_db.query(Categories).all()
    for catagory in catagories:
        categoryResult = {}
        itemResult = list()
        categoryResult["id"] = catagory.id
        categoryResult["name"] = catagory.name
        items = session_db.query(Item).filter_by(category_id=catagory.id).all()
        for item in items:
            itemResult.append(item.serialize)
        categoryResult["Item"] = itemResult
        result.append(categoryResult)
        print result
    return jsonify(Category=[i for i in result])


# this is the main loading page displays all categories and the
# latest items order in decending order
@app.route('/')
def homePage():
    catelog = session_db.query(Categories).all()
    items = session_db.query(Item).order_by(desc(Item.id)).all()
    return render_template('index.html', catelog=catelog,
                           items=items)


# This function is used to enable the user  to use his or her
# google account as a third party oath provider
@app.route('/login')
def loginPage():
    catelog = session_db.query(Categories).all()
    items = session_db.query(Item).all()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    if(state not in session):
        session['state'] = state
    return render_template('login.html',
                           catelog=catelog, items=items, STATE=state)


# this page displays specific items in a selected
# Category
@app.route('/catalog/<category_name>/items/')
def showCateogry(category_name):
    catelog = session_db.query(Categories).all()
    items = session_db.query(Item).join(
            Categories).filter_by(name=category_name)
    return render_template('categoryShow.html', catelog=catelog,
                           items=items, selectedName=category_name)


# this page displays a description of specific items in a selected
# Category
@app.route('/catalog/<category_name>/<item_title>/')
def showDescription(category_name, item_title):
    catelog = session_db.query(Categories).all()
    items = session_db.query(Item).filter_by(
            title=item_title).join(
            Categories).filter_by(name=category_name).one()
    return render_template('descriptionShow.html', catelog=catelog,
                           items=items, selectedName=category_name)


# this page alows the user to Create a new Item
# the templet checks the session object to see if the user is logged in
# if the user is logged in then the delete function can be executed
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def newItem():
    catelog = session_db.query(Categories).all()
    # check that the user is currently logged in
    if (request.method == 'POST' and session["username"] != ""):

        numberuser = session_db.query(User).filter_by(
                     username=session["username"]).count()
        if (numberuser < 1):
            newUser = User(username=session["username"])
            session_db.add(newUser)
            session_db.commit()

        dbuser = session_db.query(User).filter_by(
                 username=session["username"]).one()

        newItem = Item(title=request.form['title'],
                       description=request.form['description'],
                       category_id=request.form['category'],
                       createdUser_id=dbuser.id)
        session_db.add(newItem)
        session_db.commit()
        return redirect(url_for('showCateogry',
                        category_name=newItem.category.name))
    else:
        return render_template('createItem.html', catelog=catelog)


# this page updates or edits specific items requested by the user
# the templet checks the session object to see if the user is logged in
# if the user is logged in then the delete function can be executed
@app.route('/catalog/<item_title>/edit/', methods=['GET', 'POST'])
def editCategory(item_title):
    catelog = session_db.query(Categories).all()
    # if user not logged in show template telling user that he or she
    # needs to be logged in
    if ('username' not in session):
        return render_template('editItem.html', catelog=catelog,
                               msg="Must be loged in to edit")

    # check to see if user is already in the database
    # if the user is in the datebase then set that user name
    # to the dbuser varable
    numberuser = session_db.query(User).filter_by(
                    username=session["username"]).count()

    if (numberuser < 1):
        dbuser = User(username=session["username"])
        session_db.add(dbuser)
        session_db.commit()
    else:
        dbuser = session_db.query(User).filter_by(
                 username=session["username"]).one()

    # check to see if this is the user that created the item
    # that he or she wants to edit show the user who created
    # this item
    createdBythisUser = session_db.query(Item).filter_by(
                        title=item_title,
                        createdUser_id=dbuser.id).count()

    whoCreated = session_db.query(Item, User).filter_by(
                 title=item_title).join(Item.user).one()

    # if current user is not the user that created the item
    # display a message to the user
    if (createdBythisUser == 0):
        message = (" This was created by user " + whoCreated.User.username +
                   " only that user can alter this content!!!")
        return render_template('editItem.html',
                               items=whoCreated.Item,
                               catelog=catelog,
                               msg=message)

    editedItem = session_db.query(Item).filter_by(
                 title=item_title, createdUser_id=dbuser.id).one()

    if (request.method == 'POST' and session["username"] != "" and
       createdBythisUser > 0):
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session_db.add(editedItem)
        session_db.commit()
        return redirect(url_for('showCateogry',
                                category_name=editedItem.category.name,
                                user_id=dbuser.id))
    else:
        return render_template('editItem.html',
                               items=editedItem,
                               catelog=catelog)


# This page deletes specific items specified by the user
# the templet checks the session object to see if the user is logged in
# if the user is logged in then the delete function can be executed
@app.route('/catalog/<item_title>/delete',
           methods=['GET', 'POST'])
def deleteCategory(item_title):
    catelog = session_db.query(Categories).all()
    # if user not logged in show template telling user that he or she
    # needs to be logged in
    if ('username' not in session):
        return render_template('editItem.html',
                               msg="Must be logged in to delete")

    # check to see if user is already in the database
    # if the user is in the datebase then set that user name
    # to the dbuser varable
    numberuser = session_db.query(User).filter_by(
                    username=session["username"]).count()

    if (numberuser < 1):
        dbuser = User(username=session["username"])
        session_db.add(dbuser)
        session_db.commit()
    else:
        dbuser = session_db.query(User).filter_by(
                 username=session["username"]).one()

    # check to see if this is the user that created the item
    # that he or she wants to edit show the user who created
    # this item
    createdBythisUser = session_db.query(Item).filter_by(
                        title=item_title,
                        createdUser_id=dbuser.id).count()

    whoCreated = session_db.query(Item, User).filter_by(
                 title=item_title).join(Item.user).one()

    # if current user is not the user that created the item
    # display a message to the user
    if (createdBythisUser == 0):
        message = (" This was created by user " + whoCreated.User.username +
                   " only that user can alter this content!!!")
        return render_template('deleteCategory.html',
                               items=whoCreated.Item,
                               msg=message)

    itemToDelete = session_db.query(Item).filter_by(title=item_title,
                                                    createdUser_id=dbuser.id
                                                    ).one()
    if (request.method == 'POST' and session["username"] != ""):
        session_db.delete(itemToDelete)
        session_db.commit()
        catelog = session_db.query(Categories).all()
        items = session_db.query(Item).all()
        return render_template('index.html', catelog=catelog, items=items)
    else:
        return render_template('deleteCategory.html', items=itemToDelete)

if __name__ == '__main__':
    app.secret_key = '3_1G6ali-KlTnRklxA5I6fgl'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
