"""
Admin panel routes: user management, platform oversight.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Course, Enrollment, Certificate
from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/panel')
@login_required
@admin_required
def panel():
    """Admin panel with platform overview."""
    users = User.query.order_by(User.created_at.desc()).all()
    courses = Course.query.order_by(Course.created_at.desc()).all()

    stats = {
        'total_users': len(users),
        'total_students': sum(1 for u in users if u.role == 'student'),
        'total_instructors': sum(1 for u in users if u.role == 'instructor'),
        'total_courses': len(courses),
        'published_courses': sum(1 for c in courses if c.is_published),
        'total_enrollments': Enrollment.query.count(),
        'total_certificates': Certificate.query.count(),
    }

    return render_template('admin/panel.html', users=users, courses=courses,
                           stats=stats, title='Admin Panel')


@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user account."""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.panel'))
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{user.username}" has been deleted.', 'success')
    return redirect(url_for('admin.panel'))


@admin_bp.route('/user/<int:user_id>/toggle-role', methods=['POST'])
@login_required
@admin_required
def toggle_role(user_id):
    """Change a user's role."""
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ('student', 'instructor', 'admin'):
        user.role = new_role
        db.session.commit()
        flash(f'User "{user.username}" role changed to {new_role}.', 'success')
    return redirect(url_for('admin.panel'))
