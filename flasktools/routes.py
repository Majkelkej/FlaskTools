import os, sys, logging, secrets, re, pygeoip, webbrowser
from flask import render_template, url_for, flash, redirect, request, abort
from flasktools import app
from flasktools.forms import ImportLogForm
from flask_table import Table, Col
from werkzeug import secure_filename


def save_log(file):
        f = request.files['file']
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(f.filename)
        if f_ext != '.log':
            flash('No log file!', 'warning')
            return
        file_fn = random_hex + f_ext
        file_path = os.path.join(app.root_path, 'static/files', file_fn)
        f.save(file_path)
        ips = []
        ips = list_of_ips(file_path)
        #flash(file_path, 'success')
        if ips:
            #flash('File uploaded: ', 'success')
            return ips

def list_of_ips(file_path):
    #flash(file_path, 'success')
    ips = []
    #flash(ips, 'success')
    #return ips
    with open(file_path, "r") as logfile:
        for line in logfile.readlines():
            #flash(line, 'success')
            line = line.rstrip()
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', line)
            if regex is not None:
                ips.extend(regex)
        return ips

def try_log(file):
    ips = []

    with open(file, "r") as f:
        f.read()
        flash(f, 'warning')
        for text in f:
            regex = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', text)
            if regex is not None:
                ips.extend(regex)
        flash('klar','success')
        return ips

def add_location(ips):
    ips_dict = {}
    geodata = os.path.join(app.root_path, 'static/', 'GeoLiteCity.dat')
    gip = pygeoip.GeoIP(geodata)
    for addr in ips:
        rec = gip.record_by_addr(addr)
        try:
            country = rec['country_name']
        except:
            country = ''
        if rec is not None:
            country = rec['country_name']

            if country not in ips_dict:
                ips_dict.setdefault(country, []).append(0)
            if addr not in ips_dict[country]:
                ips_dict.setdefault(country, []).append(addr)
            ips_dict[country][0] += 1
    new_dict = []
    for key, value in ips_dict.items():
        new_dict.append({'country':key, 'count':value[0], 'ips':value[1:]})
    return new_dict



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = ImportLogForm()
    if request.method == 'POST':
#    if form.validate_on_submit():
        #file = request.files.get('file')
        ips = save_log('file')
        form.uploaded.data = 'ips'

        #flash('returned', 'success')
#            log_file = try_log(file)
        if ips:
           # flash('tillbaka i route', 'success')
            new_dict = add_location(ips)
            form.uploaded.data = new_dict
#                return redirect(url_for('home'))
#        except:
#            return redirect(url_for('home'))
#    form.uploaded.data = 'TEXT'
    return render_template('home.html', form=form)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

