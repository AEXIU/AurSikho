"""
Main public routes: Home, Browse Courses, About.
"""
from flask import Blueprint, render_template, request
from app.models import Course, User, Enrollment

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    """Landing page with featured courses and platform stats."""
    featured_courses = Course.query.filter_by(is_published=True).order_by(
        Course.created_at.desc()).limit(6).all()

    # Platform statistics
    stats = {
        'total_courses': Course.query.filter_by(is_published=True).count(),
        'total_students': User.query.filter_by(role='student').count(),
        'total_instructors': User.query.filter_by(role='instructor').count(),
        'total_enrollments': Enrollment.query.count(),
    }

    return render_template('main/home.html', courses=featured_courses, stats=stats, title='Home')


@main_bp.route('/browse')
def browse():
    """Browse all published courses with search and filter."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category = request.args.get('category', '', type=str)
    difficulty = request.args.get('difficulty', '', type=str)

    query = Course.query.filter_by(is_published=True)

    if search:
        query = query.filter(Course.title.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    courses = query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False)

    # Get unique categories for filter dropdown
    categories = db.session.query(Course.category).filter_by(
        is_published=True).distinct().all()
    categories = [c[0] for c in categories]

    return render_template('main/browse.html', courses=courses, categories=categories,
                           search=search, current_category=category,
                           current_difficulty=difficulty, title='Browse Courses')


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('main/about.html', title='About')


# Need to import db here since we use it in browse
from app import db
