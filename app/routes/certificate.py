"""
Certificate routes: generation, viewing, downloading, and public verification.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Certificate, Enrollment, Course
from app.utils.certificate_generator import generate_certificate

certificate_bp = Blueprint('certificate', __name__)


@certificate_bp.route('/certificate/<int:enrollment_id>/generate', methods=['POST'])
@login_required
def generate(enrollment_id):
    """Generate a certificate for a completed course."""
    enrollment = Enrollment.query.get_or_404(enrollment_id)

    if enrollment.student_id != current_user.id:
        flash('You can only generate certificates for your own enrollments.', 'danger')
        return redirect(url_for('student.dashboard'))

    if not enrollment.can_get_certificate:
        flash('You must complete all lessons and pass the quiz to get a certificate.', 'warning')
        return redirect(url_for('courses.detail', course_id=enrollment.course_id))

    # Check if certificate already exists
    if enrollment.certificate:
        flash('Certificate already generated!', 'info')
        return redirect(url_for('certificate.view', uid=enrollment.certificate.certificate_uid))

    # Create certificate record
    cert = Certificate(
        enrollment_id=enrollment.id,
        student_id=current_user.id,
        course_id=enrollment.course_id
    )
    db.session.add(cert)
    db.session.flush()  # Get the UID before generating the image

    # Generate the certificate image
    course = Course.query.get(enrollment.course_id)
    filename = generate_certificate(
        student_name=current_user.full_name,
        course_title=course.title,
        date_issued=cert.issued_at,
        certificate_uid=cert.certificate_uid
    )
    cert.file_path = filename
    db.session.commit()

    flash('Certificate generated successfully! 🎉', 'success')
    return redirect(url_for('certificate.view', uid=cert.certificate_uid))


@certificate_bp.route('/certificate/<uid>')
def view(uid):
    """View a certificate."""
    cert = Certificate.query.filter_by(certificate_uid=uid).first_or_404()
    course = Course.query.get(cert.course_id)
    student = cert.student
    return render_template('certificate/view.html', certificate=cert, course=course,
                           student=student, title='Certificate')


@certificate_bp.route('/certificate/<uid>/download')
def download(uid):
    """Download a certificate image."""
    cert = Certificate.query.filter_by(certificate_uid=uid).first_or_404()
    return send_from_directory(
        current_app.config['CERTIFICATE_FOLDER'],
        cert.file_path,
        as_attachment=True,
        download_name=f'Aursikho_Certificate_{cert.certificate_uid}.png'
    )


@certificate_bp.route('/verify', methods=['GET'])
def verify_page():
    """Public certificate verification page."""
    return render_template('certificate/verify.html', title='Verify Certificate')


@certificate_bp.route('/verify/<uid>')
def verify(uid):
    """Verify a specific certificate."""
    cert = Certificate.query.filter_by(certificate_uid=uid).first()
    if cert:
        course = Course.query.get(cert.course_id)
        student = cert.student
        return render_template('certificate/verify.html', certificate=cert, course=course,
                               student=student, verified=True, title='Certificate Verified')
    return render_template('certificate/verify.html', verified=False, uid=uid,
                           title='Certificate Not Found')
