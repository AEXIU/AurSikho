"""
Instructor dashboard routes: course management, lesson/quiz CRUD.
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Course, Lesson, Quiz, QuizQuestion
from app.forms import CourseForm, LessonForm, QuizForm, QuizQuestionForm
from app.utils.decorators import instructor_required

instructor_bp = Blueprint('instructor', __name__, url_prefix='/instructor')


@instructor_bp.route('/dashboard')
@login_required
@instructor_required
def dashboard():
    courses = Course.query.filter_by(instructor_id=current_user.id).order_by(Course.created_at.desc()).all()
    total_students = sum(c.total_enrolled for c in courses)
    published_count = sum(1 for c in courses if c.is_published)
    return render_template('dashboard/instructor.html', courses=courses,
                           total_students=total_students, published_count=published_count,
                           title='Instructor Dashboard')


@instructor_bp.route('/course/new', methods=['GET', 'POST'])
@login_required
@instructor_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data, description=form.description.data,
                        short_description=form.short_description.data, category=form.category.data,
                        difficulty=form.difficulty.data, instructor_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        flash(f'Course "{course.title}" created! Now add some lessons.', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course.id))
    return render_template('instructor/course_form.html', form=form, is_edit=False, title='Create Course')


@instructor_bp.route('/course/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
@instructor_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and not current_user.is_admin:
        flash('You can only edit your own courses.', 'danger')
        return redirect(url_for('instructor.dashboard'))
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.short_description = form.short_description.data
        course.category = form.category.data
        course.difficulty = form.difficulty.data
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course.id))
    return render_template('instructor/course_form.html', form=form, is_edit=True, course=course, title=f'Edit: {course.title}')


@instructor_bp.route('/course/<int:course_id>')
@login_required
@instructor_required
def manage_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and not current_user.is_admin:
        flash('You can only manage your own courses.', 'danger')
        return redirect(url_for('instructor.dashboard'))
    lessons = course.lessons.order_by(Lesson.order_num).all()
    quizzes = course.quizzes.all()
    enrollments = course.enrollments.all()
    return render_template('instructor/manage_course.html', course=course, lessons=lessons,
                           quizzes=quizzes, enrollments=enrollments, title=f'Manage: {course.title}')


@instructor_bp.route('/course/<int:course_id>/publish', methods=['POST'])
@login_required
@instructor_required
def toggle_publish(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('instructor.dashboard'))
    course.is_published = not course.is_published
    db.session.commit()
    status = 'published' if course.is_published else 'unpublished'
    flash(f'Course has been {status}.', 'success')
    return redirect(url_for('instructor.manage_course', course_id=course.id))


@instructor_bp.route('/course/<int:course_id>/lesson/new', methods=['GET', 'POST'])
@login_required
@instructor_required
def add_lesson(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('instructor.dashboard'))
    form = LessonForm()
    if form.validate_on_submit():
        max_order = db.session.query(db.func.max(Lesson.order_num)).filter_by(course_id=course.id).scalar() or 0
        lesson = Lesson(course_id=course.id, title=form.title.data, content=form.content.data,
                        video_url=form.video_url.data, lesson_type=form.lesson_type.data,
                        duration_minutes=form.duration_minutes.data or 0, order_num=max_order + 1)
        db.session.add(lesson)
        db.session.commit()
        flash(f'Lesson "{lesson.title}" added!', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course.id))
    return render_template('instructor/lesson_form.html', form=form, course=course, is_edit=False, title='Add Lesson')


@instructor_bp.route('/course/<int:course_id>/lesson/<int:lesson_id>/edit', methods=['GET', 'POST'])
@login_required
@instructor_required
def edit_lesson(course_id, lesson_id):
    course = Course.query.get_or_404(course_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    if course.instructor_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('instructor.dashboard'))
    form = LessonForm(obj=lesson)
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.content = form.content.data
        lesson.video_url = form.video_url.data
        lesson.lesson_type = form.lesson_type.data
        lesson.duration_minutes = form.duration_minutes.data or 0
        db.session.commit()
        flash('Lesson updated!', 'success')
        return redirect(url_for('instructor.manage_course', course_id=course.id))
    return render_template('instructor/lesson_form.html', form=form, course=course, lesson=lesson, is_edit=True, title=f'Edit: {lesson.title}')


@instructor_bp.route('/course/<int:course_id>/lesson/<int:lesson_id>/delete', methods=['POST'])
@login_required
@instructor_required
def delete_lesson(course_id, lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    db.session.delete(lesson)
    db.session.commit()
    flash('Lesson deleted.', 'success')
    return redirect(url_for('instructor.manage_course', course_id=course_id))


@instructor_bp.route('/course/<int:course_id>/quiz/new', methods=['GET', 'POST'])
@login_required
@instructor_required
def create_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    existing_quiz = course.quizzes.first()
    if existing_quiz:
        return redirect(url_for('instructor.manage_quiz', course_id=course.id, quiz_id=existing_quiz.id))
    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(course_id=course.id, title=form.title.data, passing_score=form.passing_score.data)
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created! Now add some questions.', 'success')
        return redirect(url_for('instructor.manage_quiz', course_id=course.id, quiz_id=quiz.id))
    return render_template('instructor/quiz_form.html', form=form, course=course, title='Create Quiz')


@instructor_bp.route('/course/<int:course_id>/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
@instructor_required
def manage_quiz(course_id, quiz_id):
    course = Course.query.get_or_404(course_id)
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizQuestionForm()
    if form.validate_on_submit():
        question = QuizQuestion(quiz_id=quiz.id, question_text=form.question_text.data,
                                option_a=form.option_a.data, option_b=form.option_b.data,
                                option_c=form.option_c.data, option_d=form.option_d.data,
                                correct_answer=form.correct_answer.data)
        db.session.add(question)
        db.session.commit()
        flash('Question added!', 'success')
        return redirect(url_for('instructor.manage_quiz', course_id=course.id, quiz_id=quiz.id))
    questions = quiz.questions.all()
    return render_template('instructor/manage_quiz.html', form=form, course=course,
                           quiz=quiz, questions=questions, title=f'Manage Quiz: {quiz.title}')


@instructor_bp.route('/course/<int:course_id>/quiz/<int:quiz_id>/question/<int:question_id>/delete', methods=['POST'])
@login_required
@instructor_required
def delete_question(course_id, quiz_id, question_id):
    question = QuizQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted.', 'success')
    return redirect(url_for('instructor.manage_quiz', course_id=course_id, quiz_id=quiz_id))


@instructor_bp.route('/course/<int:course_id>/delete', methods=['POST'])
@login_required
@instructor_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    if course.instructor_id != current_user.id and not current_user.is_admin:
        return redirect(url_for('instructor.dashboard'))
    db.session.delete(course)
    db.session.commit()
    flash(f'Course "{course.title}" has been deleted.', 'success')
    return redirect(url_for('instructor.dashboard'))
