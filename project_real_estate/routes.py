from flask import (render_template, url_for, flash, redirect, request,abort, )
from project_real_estate import db, bcrypt,app
from project_real_estate.forms import RegistrationForm, CompareForm, LoginForm, RequestResetForm, UpdateAccountForm,PropertyForm, ResetPasswordForm, LocationForm
from project_real_estate.models import User, Property,  Location
from flask_login import login_user, current_user, logout_user, login_required

#import pandas as pd
from project_real_estate.utils import send_reset_email
#from utils import save_picture


#Application Routes Configuration
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    props = Property.query.all()
    #props = Property.query.order_by(Property.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', properties=props)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, button_text="Register")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page \
                else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, button_text="Login")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/property/<int:property_id>")
def property(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property.html', title=property.title, property=property)

@app.route("/location/<int:location_id>")
def location(location_id):
    loc = Location.query.get_or_404(location_id)
    return render_template('location.html', title=location.name, location=loc)

@app.route("/location/new", methods=['GET', 'POST'])
@login_required
def new_location():
    form = LocationForm()
    if form.validate_on_submit():
        location = Location(name=form.name.data, description=form.description.data)
        db.session.add(location)
        db.session.commit()
        flash('Your location has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('new_location.html', title='New Location', form=form)

@app.route("/add_property", methods=['GET', 'POST'])
@login_required
def add_property():
    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(title=form.title.data, description=form.description.data, price=form.price.data, location=form.location.data, location_id=form.location.data, owner=current_user)
        db.session.add(property)
        db.session.commit()
        flash('Your property has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('new_property.html', title='New Property', form=form)

@app.route("/properties")
def properties():
    properties = Property.query.all()
    return render_template('properties.html', title="Show all properties", properties=properties)

@app.route("/property/<int:property_id>/update", methods=['GET', 'POST'])
@login_required
def update_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner != current_user:
        abort(403)   #handle HTTP exceptions.
    form = PropertyForm()
    if form.validate_on_submit():
        property.title = form.title.data
        property.description = form.description.data
        property.price = form.price.data
        property.location = form.location.data
        db.session.commit()
        flash('Your property has been updated!', 'success')
        return redirect(url_for('property', property_id=property.id))
    elif request.method == 'GET':
        form.title.data = property.title
        form.description.data = property.description
        form.price.data = property.price
        form.location.data = property.location
    return render_template('new_property.html', title='Update Property', form=form)

@app.route("/property/<int:property_id>/delete", methods=['POST'])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner != current_user:
        abort(403)
    db.session.delete(property)
    db.session.commit()
    flash('Your property has been deleted successful')
    return redirect(url_for('home'))

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        location = request.form.get('location')
        properties = Property.query.filter(Property.location.ilike(f'%{location}%')).all()
        return render_template('search.html', results=properties, location=location)
    return render_template('search.html')

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    properties = Property.query.all()
    form = CompareForm()
    form.properties1.choices = [(p.id, p.title) for p in properties]
    form.properties2.choices = [(p.id, p.title) for p in properties]

    property1 = None
    property2 = None

    if form.validate_on_submit():
        property1 = Property.query.get(form.properties1.data)
        property2 = Property.query.get(form.properties2.data)

    return render_template('compare.html', form=form, property1=property1, property2=property2)

# def reset_password():
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_reset_email(user)
#             flash('An email has been sent with instructions to reset your password.', 'info')
#             return redirect(url_for('login'))
#         else:
#             flash('No account found with that email.')
#     return render_template('reset_password.html', title='Reset Password', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('No account found with that email.', 'warning')
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)



# @app.route("/export_csv")
# @login_required
# def export_csv():
#     properties = Property.query.all()
#     data = [{
#         'Title': property.title,
#         'Description': property.description,
#         'Price': property.price,
#         'Location': property.location,
#         'Date Posted': property.date_posted,
#         'Owner': property.owner.username
#     }
#         for property in properties]
#     df = pd.DataFrame(data)
#     df.to_csv('properties.csv', index=False)
#     flash('Properties have been exported to CSV!', 'success')
#     return redirect(url_for('home'))
#
#     mail.send(msg)

# @app.route("/search_by_location")
# def search_by_location():
#     locations = Location.query.all()
#     return render_template('search_by_location.html', title='Search by Location', locations=locations)

#@app.route('/locations')
# def locations():
#     locs = Location.query.all()
#     return render_template('location.html', title='All Locations', locations=locs)


# @app.route("/submit", methods=['GET', 'POST'])
# @login_required
# def submit():
#     form = PropertyForm()
#     if form.validate_on_submit():
#         property = Property(title=form.title.data,
#                             location=form.location.data,
#                             price=form.price.data,
#                             bedrooms=form.bedrooms.data,
#                             bathrooms=form.bathrooms.data,
#                             description=form.description.data)
#         db.session.add(property)
#         db.session.commit()
#         flash('Your property has been submitted!', 'success')
#         return redirect(url_for('home'))
#     return render_template('submit.html', title='Submit Property', form=form)

# @app.route("/compare", methods=['GET', 'POST'])
# def compare():
#     properties = Property.query.all()
#     return render_template('compare.html', properties=properties)


# @app.route("/listing/new", methods=['GET', 'POST'])
# @login_required
# def new_listing():
#     form = ListingForm()
#     if form.validate_on_submit():
#         listing = Listing(title=form.title.data, location=form.location.data, content=form.content.data, author=current_user)
#         db.session.add(listing)
#         db.session.commit()
#         flash('Your listing has been created!', 'success')
#         return redirect(url_for('home'))
#     return render_template('new_property.html', title='New Listing', form=form, legend='New Listing')

# @app.route("/listing/<int:listing_id>")
# def listing(listing_id):
#     listing = Listing.query.get_or_404(listing_id)
#     return render_template('listing.html', title=listing.title, listing=listing)


# @app.route('/')
# def index():
#     listings = {
#         'items': [
#             {'id': 1, 'title': 'Luxury Villa', 'content': 'Beautiful villa in the heart of the city.', 'price': '1,000,000'},
#             {'id': 2, 'title': 'Cozy Cottage', 'content': 'A charming cottage in a quiet village.', 'price': '300,000'},
#             {'id': 3, 'title': 'Modern Apartment', 'content': 'A sleek apartment with city views.', 'price': '500,000'}
#         ]
#     }
#     return render_template('index.html', listings=listings)

# @app.route('/listing/<int:listing_id>')
# def listing(listing_id):
#     # Mock listing for demonstration purposes
#     listing = {'id': listing_id, 'title': 'Example Listing', 'content': 'Details about the listing.', 'price': '500,000'}
#     return render_template('listing.html', listing=listing)










# #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ADMIN ADDEDE
# from flask import (render_template, url_for, flash, redirect, request, abort)
# from project_real_estate import db, bcrypt, app
# from project_real_estate.forms import (PromoteUserForm, RegistrationForm, CompareForm,
#                                        LoginForm, RequestResetForm, UpdateAccountForm,
#                                        PropertyForm, ResetPasswordForm, LocationForm)
# from project_real_estate.models import User, Property, Location
# from flask_login import login_user, current_user, logout_user, login_required
# from functools import wraps
# from project_real_estate.utils import send_reset_email
#
# # Application Routes Configuration
#
# @app.route("/admin", methods=['GET', 'POST'])
# @login_required
# def admin_panel():
#     if not current_user.is_admin:
#         abort(403)
#     form = PromoteUserForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             user.is_admin = True
#             db.session.commit()
#             flash(f'{user.username} has been promoted to Admin!', 'success')
#         else:
#             flash('User not found.', 'danger')
#     return render_template('admin_panel.html', title='Admin Panel', form=form)
#
# @app.route("/admin/users", methods=['GET'])
# @login_required
# def list_users():
#     if not current_user.is_admin:
#         abort(403)
#     users = User.query.all()
#     return render_template('list_users.html', title='List of Users', users=users)
#
# def admin_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not current_user.is_admin:
#             abort(403)
#         return f(*args, **kwargs)
#     return decorated_function
#
# @app.route("/admin/protected-route")
# @login_required
# @admin_required
# def protected_route():
#     return "This is a protected admin route."
#
# @app.route("/")
# @app.route("/home")
# def home():
#     page = request.args.get('page', 1, type=int)
#     #props = Property.query.order_by(Property.date_posted.desc()).paginate(page=page, per_page=5)
#     props = Property.query.all()
#     return render_template('home.html', properties=props)
#
# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         if User.query.count() == 0:  # Make the first registered user an admin
#             user.is_admin = True
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created successfully', 'success')
#         return redirect(url_for('login'))
#     return render_template('register.html', title='Register', form=form, button_text="Register")
#
# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form, button_text="Login")
#
# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('home'))
#
# @app.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated successfully', 'success')
#         return redirect(url_for('account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     return render_template('account.html', title='Account', form=form)
#
# @app.route("/property/<int:property_id>")
# def property(property_id):
#     prop = Property.query.get_or_404(property_id)
#     return render_template('property.html', title=prop.title, property=prop)
#
# @app.route("/location/<int:location_id>")
# def location(location_id):
#     loc = Location.query.get_or_404(location_id)
#     return render_template('location.html', title=loc.name, location=loc)
#
# @app.route("/location/new", methods=['GET', 'POST'])
# @login_required
# def new_location():
#     form = LocationForm()
#     if form.validate_on_submit():
#         location = Location(name=form.name.data, description=form.description.data)
#         db.session.add(location)
#         db.session.commit()
#         flash('Your location has been added!', 'success')
#         return redirect(url_for('home'))
#     return render_template('new_location.html', title='New Location', form=form)
#
# @app.route("/add_property", methods=['GET', 'POST'])
# @login_required
# def add_property():
#     form = PropertyForm()
#     if form.validate_on_submit():
#         property = Property(
#             title=form.title.data,
#             description=form.description.data,
#             price=form.price.data,
#             location=form.location.data,
#             owner=current_user
#         )
#         db.session.add(property)
#         db.session.commit()
#         flash('Your property has been created!', 'success')
#         return redirect(url_for('home'))
#     return render_template('new_property.html', title='New Property', form=form)
#
# @app.route("/properties")
# def properties():
#     props = Property.query.all()
#     return render_template('properties.html', title="Show All Properties", properties=props)
#
# @app.route("/property/<int:property_id>/update", methods=['GET', 'POST'])
# @login_required
# def update_property(property_id):
#     prop = Property.query.get_or_404(property_id)
#     if prop.owner != current_user:
#         abort(403)   # Handle HTTP exceptions.
#     form = PropertyForm()
#     if form.validate_on_submit():
#         prop.title = form.title.data
#         prop.description = form.description.data
#         prop.price = form.price.data
#         prop.location = form.location.data
#         db.session.commit()
#         flash('Your property has been updated!', 'success')
#         return redirect(url_for('property', property_id=prop.id))
#     elif request.method == 'GET':
#         form.title.data = prop.title
#         form.description.data = prop.description
#         form.price.data = prop.price
#         form.location.data = prop.location
#     return render_template('new_property.html', title='Update Property', form=form)
#
# @app.route("/property/<int:property_id>/delete", methods=['POST'])
# @login_required
# def delete_property(property_id):
#     prop = Property.query.get_or_404(property_id)
#     if prop.owner != current_user:
#         abort(403)
#     db.session.delete(prop)
#     db.session.commit()
#     flash('Your property has been deleted successfully', 'success')
#     return redirect(url_for('home'))
#
# @app.route("/search", methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         location = request.form.get('location')
#         properties = Property.query.filter(Property.location.ilike(f'%{location}%')).all()
#         return render_template('search.html', results=properties, location=location)
#     return render_template('search.html')
#
# @app.route('/compare', methods=['GET', 'POST'])
# def compare():
#     properties = Property.query.all()
#     form = CompareForm()
#     form.properties1.choices = [(p.id, p.title) for p in properties]
#     form.properties2.choices = [(p.id, p.title) for p in properties]
#
#     property1 = None
#     property2 = None
#
#     if form.validate_on_submit():
#         property1 = Property.query.get(form.properties1.data)
#         property2 = Property.query.get(form.properties2.data)
#
#     return render_template('compare.html', form=form, property1=property1, property2=property2)
#
# @app.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user:
#             send_reset_email(user)
#             flash('An email has been sent with instructions to reset your password.', 'info')
#             return redirect(url_for('login'))
#         else:
#             flash('No account found with that email.', 'warning')
#     return render_template('reset_password.html', title='Reset Password', form=form)
#
# @app.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     user = User.verify_reset_token(token)
#     if not user:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('reset_password'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)
