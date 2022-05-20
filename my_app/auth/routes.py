# Aly Nour & Isabella Dube-Miglioli & Yuansheng zhang

from datetime import timedelta
from sqlite3 import IntegrityError

from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user

from urllib.parse import urlparse, urljoin
from flask import request

from my_app import db, login_manager
from my_app.auth.forms import SignupForm, LoginForm, SecurityForm
from my_app.models import User, Profile

auth_bp = Blueprint( 'auth', __name__, url_prefix='/signup' )
login_bp = Blueprint( 'login', __name__, url_prefix='/login' )


@auth_bp.route( '/signup', methods=['GET', 'POST'] )
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User( firstname=form.first_name.data, lastname=form.last_name.data,
                     email=form.email.data, security_answer=form.security_answer.data )
        user.set_password( form.password.data )

        try:
            db.session.add( user )
            db.session.commit()
            flash( f"Hello, {user.firstname} {user.lastname}. You are signed up." )
        except IntegrityError:
            db.session.rollback()
            flash( f'Error, unable to register {form.email.data}. ', 'error' )
            return redirect( url_for( 'auth.signup' ) )
        return redirect( url_for( 'main_bp.index' ) )
    return render_template( 'signup.html', title='Sign Up', form=form )


@auth_bp.route( '/login', methods=['GET', 'POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email=form.email.data ).first()
        login_user( user, remember=form.remember.data, duration=timedelta( minutes=1 ) )
        next = request.args.get( 'next' )
        if not is_safe_url( next ):
            return abort( 400 )

        # adaptive redirecting
        user_id = User.query.filter( User.email == form.email.data ).first().id
        adaptive_route = user_route( user_id )
        return redirect( next or adaptive_route or url_for( 'main_bp.index', name=user.firstname ) )
    return render_template( 'login.html', title='Login', form=form )


def user_route( user_id ):
    user_profile = Profile.query.filter( Profile.id == user_id ).first()
    if user_profile is not None:
        preference_region = user_profile.region
    else:
        preference_region = None

    if preference_region == 'EU':
        user_route = '/dash_app_eu/'
    elif preference_region == 'Southern Europe':
        user_route = '/dash_app_s_eu/'
    elif preference_region == 'Italy':
        user_route = '/dash_app_italy/'
    elif preference_region == 'Spain':
        user_route = '/spain_img'
    else:
        user_route = None
    return user_route


@auth_bp.route( '/logout' )
@login_required
def logout():
    logout_user()
    return redirect( url_for( 'main_bp.index' ) )


@login_manager.user_loader
def load_user( user_id ) -> object:
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get( user_id )
    return None


def is_safe_url( target ):
    host_url = urlparse( request.host_url )
    redirect_url = urlparse( urljoin( request.host_url, target ) )
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get( 'next' )
    if url and is_safe_url( url ):
        return url
    url = request.referrer
    if url and is_safe_url( url ):
        return url
    return '/'


@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to Login page.
    # flash( 'You must be logged in to view that page.' )
    next = url_for( request.endpoint, **request.view_args )
    return redirect( url_for( 'auth.login', next=next ) )


@auth_bp.route( '/forgot_password', methods=['GET', 'POST'] )
def forgot_password():
    form = SecurityForm()
    if form.validate_on_submit():
        user = User.query.filter_by( email=form.email.data ).first()
        login_user( user )
        next = request.args.get( 'next' )
        if not is_safe_url( next ):
            return abort( 400 )
        flash( f"Hello, {user.firstname} {user.lastname}." )
        # adaptive redirecting
        user_id = User.query.filter( User.email == form.email.data ).first().id
        adaptive_route = user_route( user_id )
        return redirect( next or adaptive_route or url_for( 'main_bp.index', name=user.firstname ) )
    return render_template( 'forgot_password.html', title='Forgot password', form=form )
