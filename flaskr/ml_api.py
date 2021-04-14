from flask import (
    Blueprint, flash, g, redirect, render_template, url_for,make_response, current_app
)
import dash.dash
from flask import request
from werkzeug.exceptions import abort
from flaskr.db import get_db
import tensorflow as tf
from flaskr.parse import get_historical_data
from flaskr.dashapp1 import dashboard
import base64
from io import BytesIO
from matplotlib.figure import Figure
import pandas as pd
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import os
import tensorflow_hub as hub
import urllib.request
from datetime import datetime

import plotly.express as px
bp = Blueprint('ml_api', __name__)

@bp.route('/ml_api/selection')
def api_selection():
    services = get_db().execute("""
                                SELECT name, description,id
                                FROM services
                                """).fetchall()
    return render_template('/ml_api/select.html', services = services)

def get_service(id, check_author=False):
    service = get_db().execute("""
                            SELECT id,name,description,url_dir FROM services
                            WHERE id = ?
                            """,
                            (id,)).fetchone()
    if service is None:
        abort(404,f"Post {id} doesn't exist")
    if check_author and service['author_id'] != g.user['id']:
        abort(403)
    return service

@bp.route('/int/<int:id>/services')
def service(id):
    service = get_service(id)

    return redirect(url_for(f"ml_api.{service['url_dir']}"))

@bp.route('/ml_api/services/1', methods = ('GET', 'POST'))
def stock_prediction():
       return redirect(url_for('/dashapp/'))

@bp.route('/ml_api/services/1_pred/str/<service>', methods = ('GET', 'POST'))
def predict(service):

    # Generate the figure **without using pyplot**.
    try:
        data = get_historical_data(str(service).lower())
    except Exception:
        abort(404, f"Company: '{service}' doesn't exist")

    next_day = pd.DataFrame([[0, 0, 0]], columns=['Diff1', 'Diff2', 'Diff5'])

    for interval in [1, 2, 5]:
        next_day[f'Diff{interval}'] = data.iloc[-interval]['AveragePrice']
    next_day['tomorrow'] = 0
    model = tf.keras.models.load_model('/Users/smaket/PycharmProjects/flaskProject/flaskr/my_model')

    fig = Figure(figsize=(10,8))
    ax = fig.subplots()
    labels = list(data.index[-14:].date)
    labels = [x.strftime("%m/%d/%Y") for x in labels]
    ax.plot(labels,data['AveragePrice'].tail(14),scaley=True)
    ax.set_title('Last 14 days')
    print(labels)
    ax.set_xticklabels(labels, rotation=45, horizontalalignment="right")
    buf = BytesIO()
    fig.savefig(buf, format="png")
    f = px.line(data['AveragePrice'].tail(14), title='Average price in last 14 days')

    import plotly.io as pio

    img = pio.to_image(f, format='png', engine='kaleido')
    buf = BytesIO(img)

    from plotly.io import to_image


    tomorrow = model.predict(next_day[['Diff1', 'Diff2', 'Diff5']].values)[0, 0]
    tomorrow = round(tomorrow, 2)
    # Embed the result in the html output.
    image = base64.b64encode(buf.getbuffer()).decode("ascii")
    from dash.dependencies import Input, Output

    return render_template('/ml_api/services/1.html',response = image, service = service, tomorrow = tomorrow, dash_url = f, image=1)


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@bp.route('/ml_api/services/2_error')
def holds_detection_with_error():
    info = 'Invalid Uplaod only txt, pdf, png, jpg, jpeg, gif'
    return render_template('/ml_api/services/2.html', info=info)


@bp.route('/ml_api/services/2')
def holds_detection():

    info =''
    return render_template('/ml_api/services/2.html', info = info)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/upload", methods=["POST", "GET"])
def upload():
    msg = ''
    db =get_db()
    if request.method == 'POST':
        file = request.files.get('file')
        filename = secure_filename(file.filename)

        if file and allowed_file(file.filename):
            file_directory = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            file.save(file_directory)

            db.execute("INSERT INTO uploads (file_name) VALUES (?)", (file_directory,))
            db.commit()

            print('File successfully uploaded ' + file.filename + ' to the database!')
            return detect(image=file_directory)
        else:
            msg = 1



    return redirect(url_for('ml_api.holds_detection_with_error'))

def detect(image):
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    from tensorflow.keras.models import load_model
    import numpy as np
    from dog_app_data.utils import get_batch,predict_and_visualize


    # image = tf.io.read_file(image)
    # image = tf.image.decode_image(image, channels=3)
    # image = tf.image.convert_image_dtype(image,tf.float32)
    # image = tf.image.resize(image,[224,244])
    img = get_batch([image],batch_size=1)
    print(next(img.as_numpy_iterator()).shape)
    path_to_model = '/home/smaket/PycharmProjects/flaskProject2/dog_app_data/20210413-173553-whole_data_adam_mnv2.h5'
    breed_predictor = load_model(path_to_model, custom_objects={"KerasLayer": hub.KerasLayer})

    fig1, fig2 = predict_and_visualize(breed_predictor, img)
    buf1 = BytesIO()
    buf2 = BytesIO()
    fig1.savefig(buf1, format="png")
    fig2.savefig(buf2, format="png")

    image1 = base64.b64encode(buf1.getbuffer()).decode("ascii")


    image2 = base64.b64encode(buf2.getbuffer()).decode("ascii")
    return render_template('/ml_api/services/2_pred.html',image1=image1,image2=image2)
    #return redirect(url_for('ml_api.api_selection'))






