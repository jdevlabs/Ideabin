from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

# Todo: (7) Create frontend based exceptions and an error page
from server.exceptions import *

from server.ideas.models import Idea
from server.users.models import User
from server.votes.models import Vote
from server.comments.models import Comment
from server.tags.models import Tag
from server.tagging.models import Tagging

from server.notifications.models import (
    NotifIdeaByUser,
    NotifIdeaUpdate,
    NotifCommentByUser,
    NotifCommentOnIdea
)

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/', endpoint='index')
def homepage():
    # if not current_user.is_anonymous():
    return redirect(url_for('frontend.explore'))
    # return render_template('index.html')


@frontend_bp.route('/add/', endpoint='add')
def add_idea():
    return render_template('add.html')


@frontend_bp.route('/register/', endpoint='register')
def register():
    return render_template('register.html')


@frontend_bp.route('/profile/', endpoint='profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@frontend_bp.route('/explore/', endpoint='explore')
def explore():
    ideas = Idea.query.order_by(Idea.created_on.desc()).limit(50)
    return render_template('explore.html', ideas=ideas)


@frontend_bp.route('/notifications/', endpoint='notifications')
@login_required
def explore():

    notifs = NotifIdeaByUser.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .order_by(NotifIdeaByUser.created_on.desc()).limit(50).all()

    notifs += NotifIdeaUpdate.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .order_by(NotifIdeaUpdate.created_on.desc()).limit(50).all()

    notifs += NotifCommentByUser.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .order_by(NotifCommentByUser.created_on.desc()).limit(50).all()

    notifs += NotifCommentOnIdea.query \
        .filter_by(user_to=current_user.user_id, read=False) \
        .order_by(NotifCommentOnIdea.created_on.desc()).limit(50).all()

    return render_template('notifications.html', notifs=notifs)


@frontend_bp.route('/search/', endpoint='search', methods=['GET'])
def search():
    try:
        term = request.args['q']
        ideas = Idea.query.filter(Idea.title.contains(term)) \
            .order_by(Idea.created_on.desc()).limit(50).all()
    except:
        ideas = []
    return render_template('explore.html', ideas=ideas)


@frontend_bp.route('/u/<string:username>', endpoint='user')
def show_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        raise NotFound

    ideas = Idea.query.filter_by(user_id=user.user_id) \
        .order_by(Idea.created_on.desc()).limit(50)
    return render_template('user.html', user=user, ideas=ideas)


@frontend_bp.route('/t/<string:tagname>', endpoint='tag')
def show_tag(tagname):
    tag = Tag.query.filter_by(tagname=tagname).first()
    if not tag:
        raise NotFound

    ideas = []
    for idea in tag.ideas:
        ideas.append(Idea.query.filter_by(idea_id=idea).first())

    return render_template('tag.html', tag=tag, ideas=ideas)


@frontend_bp.route('/i/<uuid:idea_id>', endpoint='idea')
def show_idea(idea_id):
    idea = Idea.query.get_or_404(idea_id)
    comments = Comment.query.filter_by(idea_id=idea_id) \
        .order_by(Comment.created_on.asc())

    vote = False
    if current_user.is_authenticated():
        vote = Vote.query.filter_by(user_id=current_user.user_id,
                                    idea_id=idea_id).first()

    return render_template('idea.html', idea=idea,
                           comments=comments, is_voted=vote)


@frontend_bp.route('/i/<uuid:idea_id>/edit/', endpoint='edit_idea')
@login_required
def edit_idea(idea_id):
    if current_user.is_admin():
        idea = Idea.query.filter_by(idea_id=idea_id).first()
    else:
        idea = Idea.query.filter_by(
            user_id=current_user.user_id, idea_id=idea_id).first()

    if not idea:
        raise NotFound

    return render_template('add.html', idea=idea)
