from flask import render_template
from project_real_estate import app
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500
