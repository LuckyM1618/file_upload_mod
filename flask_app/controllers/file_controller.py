import os
from flask_app import app
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from flask_app.models.filetest import FileTest

UPLOAD_FOLDER = 'flask_app\\static\\img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = { 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' }


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def form_render():
    return render_template('file_form.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    # check if the post request has a file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')

    # if file part exists in form, save to variable
    file = request.files['file']

    # if the user does not select a file, browser submits an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    # if valid file submitted, save into local folder (does *NOT* save in database!)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # saves the image into the static/img folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # saves img filename in SQL db for reference
        new_file_id = FileTest.save({'filename': filename})

        # *NOTE* if storing images on 3rd party site, the file.save() command will instead be a call to the image hosting site to save it, store the image host URL instead of filename, and use image host URL directly in img tag for src attribute
    
    return redirect(f'/view-image/{new_file_id}')


@app.route('//view-image/<int:file_id>')
def view_image(file_id):
    return render_template('view_image.html', file=FileTest.get_one_by_id({'id': file_id}))

if __name__=="__main__":
    app.run(debug = True)