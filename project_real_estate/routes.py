from flask import (render_template, url_for, flash, redirect, request,abort)
from project_real_estate import db, bcrypt,app
from project_real_estate.forms import PromoteUserForm, UpdateUserForm, SearchForm, DeleteForm, RegistrationForm, CompareForm, LoginForm, RequestResetForm, UpdateAccountForm,PropertyForm, LocationForm
from project_real_estate.models import User, Property,  Location
from flask_login import login_user, current_user, logout_user, login_required
#import csv

#Application Routes Configuration

@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    form = PromoteUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            user.is_admin = True
            db.session.commit()
            flash(f'{user.username} has been promoted to Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('User not found.', 'danger')
    users = User.query.all()
    properties = Property.query.all()
    return render_template('admin_dashboard.html', title='Admin Dashboard', users=users, properties=properties, form=form)

@app.route("/admin/users", methods=['GET'])
@login_required
def list_users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template('list_users.html', title='List of Users', users=users)

@app.route("/admin/protected-route")
@login_required
#@admin_required
def protected_route():
    return "This is a protected admin route."

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    props = Property.query.all()
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route("/admin/user/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if not current_user.is_admin:
        abort(403)
    form = UpdateUserForm()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('The user has been updated!', 'success')
        return redirect(url_for('admin_dashboard'))
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.is_admin.data = user.is_admin
    return render_template('admin_update_user.html', title='Admin Update User', form=form, user=user)

@app.route("/property/update/<int:property_id>", methods=['GET', 'POST'])
@login_required
def update_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner != current_user and not current_user.is_admin:
        abort(403)
    form = PropertyForm()
    if form.validate_on_submit():
        property.title = form.title.data
        property.description = form.description.data
        property.price = form.price.data
        property.location = form.location.data
        db.session.commit()
        flash('Your property has been updated!', 'success')
        return redirect(url_for('admin_dashboard', property_id=property.id))
    elif request.method == 'GET':
        form.title.data = property.title
        form.description.data = property.description
        form.price.data = property.price
        form.location.data = property.location
    return render_template('admin_update_property.html', title='Admin Update Property', form=form, legend='Update Property')

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
    property_our = Property.query.get_or_404(property_id)
    return render_template('property.html', title=property.title, property=property_our)

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

#route to display the property details after updating.
@app.route("/property/<int:property_id>")
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property.html', title=property.title, property=property)

@app.route("/property/<int:property_id>/delete", methods=['POST'])
@login_required
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner != current_user:
        abort(403)
    db.session.delete(property)
    db.session.commit()
    flash('Your property has been deleted successful')
    return redirect(url_for('properties'))

@app.route("/properties")
def properties():
    properties = Property.query.all()
    form = DeleteForm()
    return render_template('properties.html', title="Show all properties", properties=properties, form=form)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = []
    search_location = ""
    if form.validate_on_submit():
        search_location = form.search_query.data
        # Query properties by location
        results = Property.query.filter(Property.location.ilike(f'%{search_location}%')).all()
    return render_template('search.html', form=form, results=results, search_location=search_location)

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

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            #send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('login'))
        else:
            flash('No account found with that email.', 'warning')
    return render_template('reset_password.html', title='Reset Password', form=form)

# @app.route("/export_properties_csv")
# @login_required
# def export_properties_csv():
#     if not current_user.is_admin:
#         abort(403)
#     properties = Property.query.all()
#     # Create the response object as a CSV
#     response = make_response()
#     response.headers["Content-Disposition"] = "attachment; filename=properties.csv"
#     response.headers["Content-Type"] = "text/csv"
#
#     # Write data to the CSV
#     writer = csv.writer(response)
#     writer.writerow(["Title", "Description", "Price", "Location", "Date Posted", "Owner"])
#     for property in properties:
#         writer.writerow([property.title, property.description, property.price, property.location, property.date_posted,
#                          property.owner.username])
#     return response
