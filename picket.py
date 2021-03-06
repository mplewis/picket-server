from flask import (Flask, flash, redirect, render_template, request, url_for, g,
                   send_from_directory)
from flask.ext.login import (LoginManager, current_user, login_required,
                             login_user, logout_user, UserMixin, AnonymousUser,
                             confirm_login)
from flask.ext.uploads import (UploadSet, configure_uploads, IMAGES,
                               UploadNotAllowed)

from modules import site_config
from modules.site_users import get_user, load_users_from_file
from modules.site_upload import allowed_file
from modules.fn_utils import gen_pleasing_fn, fn_split

# Flask app
app = Flask(__name__)
app.config.from_object(site_config) # read all uppercase config vars from env

# Upload
images = UploadSet('images', site_config.ALLOWED_EXTENSIONS)
configure_uploads(app, images)

# Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'You need to log in to access this page.'

# Loads a single user for the login manager
@login_manager.user_loader
def load_user(user_id):
    # Load users from disk into memory every time a user object is referenced
    # This should keep our user database current at all times.
    # Is this a good idea?
    ALL_USERS = load_users_from_file()
    return get_user(user_id, ALL_USERS)

# Shortcut function to simplify checking whether a user is logged in
# Returns True if a user is logged in and not anonymous, False otherwise
def user_logged_in(g_user):
    return g_user is not None and g_user.is_authenticated()

# Set up the login manager
login_manager.setup_app(app)

# Make g.user a globally accessible version of the current request's user
@app.before_request
def before_request():
    g.user = current_user

# Login form
@app.route(site_config.ROUTE_LOGIN, methods=['GET', 'POST'])
def login():
    # If user is logged in, send them directly to content
    if user_logged_in(g.user):
        flash('Welcome back, ' + g.user.username + '!',
              'information')
        return redirect(url_for('manage'))
    # If the login form is valid (username and password are filled in),
    # proceed with attempting login
    if request.method == 'POST':
        remember_me = True # defaults to remember me, do I want to change this?
        data = request.form
        username = data['username']
        password = data['password']
        # Load users from file
        ALL_USERS = load_users_from_file()
        # Grab user object from user object dictionary
        user_obj = get_user(username, ALL_USERS)
        # Check for empty username and password
        if username.strip() == '':
            flash('You need to provide a username.', 'information')
        elif password == '':
            flash('You need to provide a password.', 'information')
        # Check for valid username
        elif username in ALL_USERS:
            # Check user's password
            if user_obj.check_password(password):
                # Try logging in!
                if login_user(user_obj, remember=remember_me):
                    # Yay, it worked! Send user to content.
                    flash(g.user.username + ' logged in successfully.',
                          'success')
                    return redirect(request.args.get('next') or
                                    url_for('manage'))
                # Uh oh. Something went wrong
                else:
                    # User isn't active. They can't login.
                    if not user_obj.is_active():
                        flash('Login failed: ' + username +
                              ' is inactive.', 'error')
                    # I don't know why login failed; username and password
                    # are OK, user is active, but login_user returned false.
                    else:
                        flash('Login failed for an unknown reason.', 'error')
            # Bad password
            else:
                flash('Invalid username or password.', 'warning')
        # Bad username
        else:
            flash('Invalid username or password.', 'warning')
    return render_template('login.html')

# Main logged-in content page
@app.route(site_config.ROUTE_MANAGE)
@login_required
def manage():
    # Kinda a placeholder page right now. Will list all uploaded images later.
    return render_template('manage.html')

# Upload images
@app.route(site_config.ROUTE_UPLOAD, methods=['GET', 'POST'])
@login_required
def upload():
    # If submitting the form
    if request.method == 'POST':
        print request.form
        print request.files
        # Rename the image name to the name in the form while keeping the
        # extension the same
        save_as_name = request.form.get('file-name')
        uploaded_image = request.files.get('upload-file')
        original_fn = uploaded_image.filename
        original_name, original_ext = fn_split(original_fn)
        new_fn = save_as_name + '.' + original_ext
        uploaded_image.filename = new_fn
        # Try to submit the file
        try:
            filename = images.save(uploaded_image)
        # Server blocked upload (empty file, wrong type)
        except UploadNotAllowed:
            flash('Your upload was not allowed by the server.', 'error')
        # File was allowed through; redirect directly to the file
        else:
            return redirect(url_for('view', filename=filename))
    # Generate a nice filename to put in the "save as" box
    random_fn = gen_pleasing_fn(site_config.RANDOM_FN_LENGTH)
    # Render page with nice filename
    return render_template('upload.html', default_fn=random_fn)

# Log out
@app.route(site_config.ROUTE_LOGOUT)
def logout():
    if not user_logged_in(g.user):
        flash("You aren't logged in!", 'warning')
    else:
        # After logout_user(), g.user will be the Anonymous user.
        # Save it so we know who we logged out.
        username_logging_out = g.user.username
        logout_user()
        flash('You have been logged out, ' + username_logging_out + '.', 'success')
    # Send them to the homepage
    return redirect(url_for('login'))

# /logout (without slash) redirects to /logout/
@app.route(site_config.ROUTE_LOGOUT_FIX)
def logout_fix():
    return redirect(url_for('logout'))

# Serve the file requested
@app.route(site_config.ROUTE_VIEW + '<filename>')
def view(filename):
    return send_from_directory(app.config['UPLOADED_IMAGES_DEST'], filename)

# Redirect to the manager if the files directory is requested directly
@app.route(site_config.ROUTE_VIEW)
def empty_view_request():
    return redirect(url_for('manage'))

# Run the app
if __name__ == '__main__':
    app.run(debug=site_config.SITE_DEBUG_MODE)