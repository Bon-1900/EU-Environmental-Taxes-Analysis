# Aly Nour & Isabella Dube-Miglioli

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from my_app import photos, db
from my_app.community.forms import ProfileForm, BlogForm
from my_app.models import Profile, User, Blog

community_bp = Blueprint('community_bp', __name__, url_prefix='/community')


@community_bp.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    blog = Blog.query.join(User).filter(User.id == current_user.id).first()
    if blog:
        return redirect(url_for('community_bp.update_blog'))
    else:
        return redirect(url_for('community_bp.create_blog'))


@community_bp.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    form = BlogForm()

    if form.validate_on_submit() and request.method == 'POST':
        p = Blog(answer_1=form.answer_1.data, answer_2=form.answer_2.data, answer_3=form.answer_3.data,
                 answer_4=form.answer_4.data, user_id=current_user.id)
        db.session.add(p)
        db.session.commit()

        return redirect(url_for('community_bp.display_blogs'))
    return render_template('blog.html', title='Blog', form=form)


@community_bp.route('/update_blog', methods=['GET', 'POST'])
@login_required
def update_blog():
    flash('Opinion already registered, do you wanna update it?')

    blog = Blog.query.join(User).filter_by(id=current_user.id).first()
    form = BlogForm(obj=blog)

    if request.method == 'POST' and form.validate_on_submit():
        blog.answer_1 = form.answer_1.data
        blog.answer_2 = form.answer_2.data
        blog.answer_3 = form.answer_3.data
        blog.answer_4 = form.answer_4.data

        db.session.commit()

        return redirect(url_for('community_bp.display_blogs', username=blog.answer_1))
    return render_template('display_blog.html', form=form)


@community_bp.route('/display_blogs', methods=['GET', 'POST'])
@login_required
def display_blogs():
    users = None
    posts = None
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Enter content to search for")
            return redirect(url_for("community_bp.blog"))
        posts = Blog.query.filter((Blog.answer_1.contains(term))).all()

        if not posts:
            flash("No posts were found.")
            return redirect(url_for("community_bp.update_blog"))
    else:
        posts = Blog.query.all()

    urls = []
    users = Profile.query.all()

    for post in posts:
        url = photos.url("Opinion.png")
        urls.append(url)

    return render_template("display_blogs.html", blogs=zip(posts, urls))


@community_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('community_bp.update_profile'))
    else:
        return redirect(url_for('community_bp.create_profile'))


@community_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        filename = 'User_icon.PNG'
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                if 'photo' != 'User_icon.PNG':
                    filename = photos.save(request.files['photo'])

        p = Profile(username=form.username.data, bio=form.bio.data, photo=filename, age=form.age.data,
                    region=form.region.data, user_id=current_user.id)

        db.session.add(p)
        db.session.commit()
        return redirect(url_for('community_bp.display_profiles', username=p.username))
    return render_template('profile.html', form=form)


@community_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)

    if request.method == 'POST' and form.validate_on_submit():

        profile.username = form.username.data
        profile.bio = form.bio.data
        profile.age = form.age.data
        profile.region = form.region.data

        db.session.commit()

        picture = form.photo

        if picture is not None:
            if 'photo' in request.files:
                if request.files['photo'].filename != '':
                    filename = photos.save(request.files['photo'])
                    profile.photo = filename
                    db.session.commit()

        return redirect(url_for('community_bp.display_profiles', username=profile.username))

    return render_template('profile.html', form=form)


@community_bp.route('/display_profiles', methods=['GET', 'POST'])
@community_bp.route('/display_profiles/<username>/', methods=['GET', 'POST'])
@login_required
def display_profiles(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for("community_bp.blog"))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        results = Profile.query.filter_by(username=username).all()
    if not results:
        flash("Username not found.")
        return redirect(url_for("main_bp.index"))
    urls = []

    for result in results:
        url = photos.url(result.photo)
        urls.append(url)

    return render_template("display_profile.html", profiles=zip(results, urls))
