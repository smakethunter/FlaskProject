from flask import (
    Blueprint, flash, g, redirect, render_template, url_for,make_response
)
from flask import request
from werkzeug.exceptions import abort

import random
from flaskr.db import get_db
import datetime
from io import BytesIO
import base64
import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

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
    service = get_db().execute("SELECT name, description FROM services WHERE id = ? ", (1,)).fetchone()
    if request.method == 'POST':
        company = request.form['title']
        error = None
        if not company:
            error = 'Company required'
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('ml_api.predict', service = company))
    return render_template('ml_api/services/1.html', service=service, request=request)

@bp.route('/ml_api/services/1_pred/str/<service>', methods = ('GET', 'POST'))
def predict(service):
    from flaskr.parse import get_historical_data
    from flaskr.simple import Simple
    import matplotlib.pyplot as plt
    import numpy as np




    import base64
    from io import BytesIO

    from matplotlib.figure import Figure
    import pandas as pd
    # Generate the figure **without using pyplot**.
    try:
        data = get_historical_data(str(service).lower())
    except Exception:
        abort(404, f"Company: '{service}' doesn't exist")

    next_day = pd.DataFrame([[0, 0, 0]], columns=['Diff1', 'Diff2', 'Diff5'])

    for interval in [1, 2, 5]:
        next_day[f'Diff{interval}'] = data.iloc[-interval]['AveragePrice']
    next_day['tomorrow'] = 0
    model = Simple(data, all_data = True)



    print(next_day)
    result = np.array(model.learn(32))

    fig = Figure(figsize=(10,10))
    ax = fig.subplots(2,1)
    labels = list(data.index[-14:].date)
    labels = [x.strftime("%m/%d/%Y") for x in labels]
    ax[0].plot(labels,data['AveragePrice'].tail(14))
    ax[0].set_title('Last 14 days')
    ax[1].set_title('Model accuracy')
    print(labels)
    ax[0].set_xticklabels(labels, rotation=45, horizontalalignment="right")
    ax[1].plot(result[:, 0])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    tomorrow = model.model.predict(next_day[['Diff1', 'Diff2', 'Diff5']].values)[0, 0]
    tomorrow = round(tomorrow, 2)
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('/ml_api/services/1_pred.html',response = data, service = service, tomorrow = tomorrow)








