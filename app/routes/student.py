"""
Student dashboard routes: enrolled courses, progress, certificates.
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Enrollment, Certificate
from app.utils.decorators import role_required

student_bp = Blueprint('student', __name__, url_prefix='/student')


@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    """Student dashboard showing enrolled courses and progress."""
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).order_by(
        Enrollment.enrolled_at.desc()).all()

    # Separate active and completed enrollments
    active_enrollments = [e for e in enrollments if not e.completed]
    completed_enrollments = [e for e in enrollments if e.completed]

    return render_template('dashboard/student.html',
                           active_enrollments=active_enrollments,
                           completed_enrollments=completed_enrollments,
                           title='My Dashboard')


@student_bp.route('/certificates')
@login_required
@role_required('student')
def certificates():
    """View all earned certificates."""
    certs = Certificate.query.filter_by(student_id=current_user.id).order_by(
        Certificate.issued_at.desc()).all()

    return render_template('dashboard/student.html',
                           certificates=certs,
                           show_certificates=True,
                           active_enrollments=[],
                           completed_enrollments=[],
                           title='My Certificates')
