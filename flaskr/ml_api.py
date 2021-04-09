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

import urllib.request
from datetime import datetime
from flask_dropzone import Dropzone
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
    #f.show()
    import plotly
    #plotly.io.orca.config.executable = '/Users/smaket/miniforge3/pkgs/plotly-orca-3.4.2-0/bin/orca'

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
        buf = BytesIO()
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        if file and allowed_file(file.filename):

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            db.execute("INSERT INTO uploads (file_name) VALUES (?)", (file.filename,))
            db.commit()

            print('File successfully uploaded ' + file.filename + ' to the database!')
            return detect(image=filename)
        else:
            msg = 1



    return redirect(url_for('ml_api.holds_detection_with_error'))

def detect(image):
    print(image)
    return redirect(url_for('ml_api.api_selection'))






