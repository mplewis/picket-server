# Make sure to check these settings and replace them with sane values, then
# rename this file to site_config before you deploy!

# Flask server settings
SITE_DEBUG_MODE = True
CSRF_ENABLED = True
SECRET_KEY = 'not a good secret key, CHANGE ME'
USER_LIST_FILE = 'users.yml'

# Flask routes
# TODO

# flask-upload settings. Name of set is "images"
UPLOADED_IMAGES_DEST = 'uploads'
ALLOWED_EXTENSIONS = set([
	'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'
])
RANDOM_FN_LENGTH = 6