"""
Course routes: Detail view, enrollment, lesson viewing, quiz taking.
"""
from datetime import datetime, timezone
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Course, Lesson, Enrollment, LessonProgress, Quiz, QuizQuestion, QuizAttempt

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/course/<int:course_id>')
def detail(course_id):
    """Course detail page with lessons list and enrollment option."""
    course = Course.query.get_or_404(course_id)

    # Only show published courses (unless you're the instructor or admin)
    if not course.is_published:
        if not current_user.is_authenticated or \
           (current_user.id != course.instructor_id and not current_user.is_admin):
            abort(404)

    enrollment = None
    if current_user.is_authenticated:
        enrollment = current_user.get_enrollment(course)

    return render_template('courses/detail.html', course=course,
                           enrollment=enrollment, title=course.title)


@courses_bp.route('/course/<int:course_id>/enroll', methods=['POST'])
@login_required
def enroll(course_id):
    """Enroll the current student in a course."""
    course = Course.query.get_or_404(course_id)

    if not course.is_published:
        abort(404)

    if current_user.role != 'student':
        flash('Only students can enroll in courses.', 'warning')
        return redirect(url_for('courses.detail', course_id=course_id))

    if current_user.is_enrolled(course):
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('courses.detail', course_id=course_id))

    enrollment = Enrollment(student_id=current_user.id, course_id=course.id)
    db.session.add(enrollment)
    db.session.commit()

    flash(f'Successfully enrolled in "{course.title}"!', 'success')
    return redirect(url_for('courses.detail', course_id=course_id))


@courses_bp.route('/course/<int:course_id>/lesson/<int:lesson_id>')
@login_required
def view_lesson(course_id, lesson_id):
    """View a specific lesson (must be enrolled)."""
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)

    if lesson.course_id != course.id:
        abort(404)

    enrollment = current_user.get_enrollment(course)
    if not enrollment and current_user.id != course.instructor_id and not current_user.is_admin:
        flash('You must be enrolled to view lessons.', 'warning')
        return redirect(url_for('courses.detail', course_id=course_id))

    # Get lesson progress if enrolled
    lesson_progress = None
    if enrollment:
        lesson_progress = LessonProgress.query.filter_by(
            enrollment_id=enrollment.id, lesson_id=lesson.id).first()

    # Get all lessons for sidebar navigation
    all_lessons = course.lessons.order_by(Lesson.order_num).all()

    # Get completed lesson IDs for the sidebar
    completed_lesson_ids = set()
    if enrollment:
        completed_records = LessonProgress.query.filter_by(
            enrollment_id=enrollment.id, completed=True).all()
        completed_lesson_ids = {lp.lesson_id for lp in completed_records}

    return render_template('courses/lesson.html', course=course, lesson=lesson,
                           enrollment=enrollment, lesson_progress=lesson_progress,
                           all_lessons=all_lessons, completed_lesson_ids=completed_lesson_ids,
                           title=lesson.title)


@courses_bp.route('/course/<int:course_id>/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(course_id, lesson_id):
    """Mark a lesson as completed."""
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)

    if lesson.course_id != course.id:
        abort(404)

    enrollment = current_user.get_enrollment(course)
    if not enrollment:
        abort(403)

    # Check if already marked as complete
    progress = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id, lesson_id=lesson.id).first()

    if not progress:
        progress = LessonProgress(
            enrollment_id=enrollment.id,
            lesson_id=lesson.id,
            completed=True,
            completed_at=datetime.now(timezone.utc)
        )
        db.session.add(progress)
    elif not progress.completed:
        progress.completed = True
        progress.completed_at = datetime.now(timezone.utc)

    # Check if course is now complete
    total_lessons = course.total_lessons
    completed_count = LessonProgress.query.filter_by(
        enrollment_id=enrollment.id, completed=True).count() + (1 if not progress.id else 0)

    if completed_count >= total_lessons:
        quiz = course.quizzes.first()
        if not quiz:
            # No quiz — course is complete
            enrollment.completed = True
            enrollment.completed_at = datetime.now(timezone.utc)

    db.session.commit()
    flash(f'Lesson "{lesson.title}" marked as complete!', 'success')

    # Navigate to next lesson or back to course
    next_lesson = Lesson.query.filter(
        Lesson.course_id == course.id,
        Lesson.order_num > lesson.order_num
    ).order_by(Lesson.order_num).first()

    if next_lesson:
        return redirect(url_for('courses.view_lesson', course_id=course.id, lesson_id=next_lesson.id))
    return redirect(url_for('courses.detail', course_id=course.id))


@courses_bp.route('/course/<int:course_id>/quiz/<int:quiz_id>')
@login_required
def take_quiz(course_id, quiz_id):
    """Display quiz questions for the student."""
    course = Course.query.get_or_404(course_id)
    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.course_id != course.id:
        abort(404)

    enrollment = current_user.get_enrollment(course)
    if not enrollment:
        flash('You must be enrolled to take quizzes.', 'warning')
        return redirect(url_for('courses.detail', course_id=course_id))

    # Check if all lessons are completed
    if enrollment.progress_percentage < 100:
        flash('Please complete all lessons before taking the quiz.', 'warning')
        return redirect(url_for('courses.detail', course_id=course_id))

    questions = quiz.questions.all()

    # Check for previous attempts
    previous_attempt = QuizAttempt.query.filter_by(
        enrollment_id=enrollment.id, quiz_id=quiz.id).order_by(
        QuizAttempt.attempted_at.desc()).first()

    return render_template('courses/quiz.html', course=course, quiz=quiz,
                           questions=questions, enrollment=enrollment,
                           previous_attempt=previous_attempt, title=f'Quiz: {quiz.title}')


@courses_bp.route('/course/<int:course_id>/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(course_id, quiz_id):
    """Process quiz submission and calculate score."""
    course = Course.query.get_or_404(course_id)
    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.course_id != course.id:
        abort(404)

    enrollment = current_user.get_enrollment(course)
    if not enrollment:
        abort(403)

    questions = quiz.questions.all()
    total = len(questions)
    correct = 0

    # Grade each question
    for question in questions:
        answer = request.form.get(f'question_{question.id}', '').lower()
        if answer == question.correct_answer.lower():
            correct += 1

    # Calculate score as percentage
    score = int((correct / total) * 100) if total > 0 else 0
    passed = score >= quiz.passing_score

    # Record attempt
    attempt = QuizAttempt(
        enrollment_id=enrollment.id,
        quiz_id=quiz.id,
        score=score,
        passed=passed
    )
    db.session.add(attempt)

    # If passed, mark course as completed
    if passed and not enrollment.completed:
        enrollment.completed = True
        enrollment.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    if passed:
        flash(f'Congratulations! You scored {score}% and passed the quiz! 🎉', 'success')
    else:
        flash(f'You scored {score}%. You need {quiz.passing_score}% to pass. Try again!', 'warning')

    return redirect(url_for('courses.take_quiz', course_id=course_id, quiz_id=quiz_id))
