"""Contributers: Aly Nour & Yuansheng zhang"""

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/', defaults={'name': 'Anonymous'})
@main_bp.route('/<name>')
def index(name):
    if not current_user.is_anonymous:
        name = current_user.firstname
    return render_template('index.html', title="EU environmental taxes analysis", name=name)


@main_bp.route('/dash_app_eu')
def dash_app1():
    return redirect('/dash_app_eu/')


@main_bp.route('/dash_app_s_eu')
def dash_app2():
    return redirect('/dash_app_s_eu/')


@main_bp.route('/dash_app_italy')
def dash_app3():
    return redirect('/dash_app_italy/')


@main_bp.route('/spain_img')
@login_required
def spain_img():
    return render_template( 'spain_img.html', title="spain_img")
