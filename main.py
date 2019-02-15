# MIT License
#
# Copyright (c) 2018 Cameron Dempsey
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import os
import subprocess

from celery import Celery
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.contrib.cache import MemcachedCache, SimpleCache
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

AGENTS_FOLDER = r'pacman-contest\agents'
LOGS_FOLDER = r'logs'
ALLOWED_EXTENSIONS = {'py'}


app = Flask(__name__)
app.secret_key = 'B6XcwyXNfJvBm5ENATl7r2S58MTj4ULo'
app.name = "pacman-comp-site"
app.config['AGENTS_FOLDER'] = AGENTS_FOLDER
app.config['LOGS_FOLDER'] = LOGS_FOLDER
app.config['CELERY_BROKER_URL'] = 'amqp://default:password@localhost:5672/defaultvhost'
# app.config['CELERY_RESULT_BACKEND'] = 'amqp://default:password@localhost:5672/defaultvhost'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

try:
    cache = MemcachedCache()
except RuntimeError:
    cache = SimpleCache()
cache.set('agent-list', [])
_, _, _l = next(os.walk(LOGS_FOLDER), (None, None, []))
cache.set('requests', len(_l)//2)
cache.set('logs', 0)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    _, _, filenames = next(os.walk(AGENTS_FOLDER), (None, None, []))
    agents = [fn.rsplit('.', 1)[0] for fn in filenames]
    _, _, logs = next(os.walk(LOGS_FOLDER), (None, None, []))
    requests = cache.get('requests') - (len(logs)//2)
    return render_template('home.html', requests=requests, agents=agents)


@app.route('/submit-request', methods=['POST'])
def submit_request():
    team1 = request.form['team1']
    team2 = request.form['team2']
    run_match.delay(team1, team2)
    cache.inc("requests")
    flash("Request submitted")
    return redirect(url_for('home'))


@app.route('/submit-agent', methods=['POST'])
def submit_agent():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['AGENTS_FOLDER'], filename)
        app.logger.info('Saving file to: %s', path)
        file.save(path)
        # cache.set(agent_name, filename)
        # agent_list = cache.get('agent-list')
        # if agent_name not in agent_list:
        #     agent_list.append(agent_name)
        #     cache.set('agent-list', agent_list)
        # if (cache.get('comp-task') is None) and (len(cache.get('agent-list')) >= 2):
        #     task = run_comp.apply_async()
        #     cache.set('comp-task', task.id)
        flash("Uploaded successfully")
        return redirect(url_for('home'))
    else:
        flash("Invalid file or filename")
        return redirect(url_for('home'))


@app.route('/results')
def results():
    _, _, filenames = next(os.walk(app.config['LOGS_FOLDER']), (None, None, []))
    logs = []
    replays = []
    for fn in filenames:
        ext = fn.rsplit('.', 1)[1]
        if ext == "log": logs.append(fn)
        elif ext == "replay": replays.append(fn)
    logs.sort()
    replays.sort()
    return render_template('results.html', logs=logs, replays=replays)


@app.route('/results/<path:filename>', methods=['GET', 'POST'])
def download_result(filename):
    path = os.path.join(app.root_path, app.config['LOGS_FOLDER'])
    return send_from_directory(directory=path, filename=filename)


# @app.route('/status')
# def status():
#     task_id = cache.get('comp-task')
#     if task_id is None:
#         return render_template('status.html', content="IDLE")
#     task = run_comp.AsyncResult(task_id)
#     if task.state == 'PENDING':
#         return render_template('status.html', content="PENDING")
#     elif task.state != 'FAILURE':
#         match = task.info.get('match', (None, None))
#         return render_template('status.html', content="RUNNING " + str(match[0]) + " VS " + str(match[1]))
#     else:
#         return render_template('status.html', content="EXCEPTION HAS OCCURRED:" + str(task.info))


@celery.task()
def run_match(team1, team2):
    app.logger.info("Starting "+team1+" VS "+team2+" match "+str(cache.get('requests')))
    log_name = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")+"-"+team1+"_vs_"+team2
    outcome = subprocess.run(["python2", "pacman-contest/capture.py", "-r", "agents/"+team1, "-b", "agents/"+team2,
                              "-q", "-l", "RANDOM", "--record", "-c"],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    with open(os.path.join(app.config['LOGS_FOLDER'], log_name+".log"), 'wb') as file:
        file.write(outcome.stdout)
    # cache.dec("requests")
    app.logger.info("Finished " + team1 + " VS " + team2 + " match")


# @celery.task(bind=True)
# def run_comp(self, team1, team2):
#     # agent_list = cache.get('agent-list')
#     # matches = combinations(agent_list)
#     for m in matches:
#         self.update_state(state="RUNNING", meta={'match': m})
#     cache.delete('comp-task')
#     return None, None




if __name__ == '__main__':
    app.run()
