from . import audio_handler

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for, stream_with_context, Response)

from flaskr.db import get_db

bp = Blueprint('tuner', __name__, url_prefix='/tuner')

def config_required(view):
    #view decorator that redirects unconfigured users to config
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.config is None:
            return redirect(url_for('tuner.config'))

        return view(**kwargs)

    return wrapped_view


#broken: saving audio configs
##@bp.before_app_request
##def load_config():
##    #if a config is stored in session, load it up
##    config = session.get('config')
##    if config is None:
##        g.config = None
##    else:
##        g.user = get_db().execute()
            
        
    


@bp.route('/config', methods=('GET', 'POST'))
#route URL /tuner/config to the config view function
def audioconfig():
    #get system drivers and input devices
    host_apis, input_devices = audio_handler.queryInputDevices()
    #extract device names to display on form
    devices = [(d['name'], host_apis[d['hostapi']]['name']) for d in input_devices]
    #config view function
    if request.method == 'POST':
        device = eval(request.form['device'])
        db = get_db()
        error = None

        if not device:
            #throw error if no device selected
            error = 'Input device is required.'

        if error is None:
                #store device name and driver in 
                db.execute(
                    "insert into audioconfig (device, driver) values (?,?)",
                    (device[0], device[1]),
                )
                db.commit()
                return redirect(url_for("tuner.tune"))

        flash(error)

    return render_template('tuner/audioconfig.html', devices=devices)

@bp.route('/stream')
def stream():
    #route for pitch data stream
    db = get_db()
    error = None
    
    config = db.execute(
        "select driver, device from audioconfig").fetchone()

    if not config:
        error = 'Config is required.'

    flash(error)
    return Response(stream_with_context(audio_handler.start_stream(config)), mimetype='text')

@bp.route('/tune')
def tune():
    #view function for tune page
    
    return render_template('tuner/tune.html')
