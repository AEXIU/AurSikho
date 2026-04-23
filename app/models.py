"""
Database models for Aursikho.
Defines all entities: User, Course, Lesson, Quiz, Enrollment, Certificate, etc.
"""
from datetime import datetime, timezone
import uuid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """User model supporting student, instructor, and admin roles."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # student, instructor, admin
    full_name = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text, default='')
    avatar = db.Column(db.String(256), default='default.png')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    courses_teaching = db.relationship('Course', backref='instructor', lazy='dynamic')
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic')
    certificates = db.relationship('Certificate', backref='student', lazy='dynamic')

    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Verify a password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_enrolled(self, course):
        """Check if user is enrolled in a specific course."""
        return self.enrollments.filter_by(course_id=course.id).first() is not None

    def get_enrollment(self, course):
        """Get enrollment record for a specific course."""
        return self.enrollments.filter_by(course_id=course.id).first()

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_instructor(self):
        return self.role == 'instructor'

    @property
    def is_student(self):
        return self.role == 'student'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Course(db.Model):
    """Course model with lessons, quizzes, and enrollments."""
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(300), default='')
    thumbnail = db.Column(db.String(256), default='default_course.png')
    category = db.Column(db.String(50), nullable=False, default='General')
    difficulty = db.Column(db.String(20), nullable=False, default='beginner')  # beginner, intermediate, advanced
    is_published = db.Column(db.Boolean, default=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy='dynamic',
                              order_by='Lesson.order_num', cascade='all, delete-orphan')
    quizzes = db.relationship('Quiz', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def total_lessons(self):
        return self.lessons.count()

    @property
    def total_enrolled(self):
        return self.enrollments.count()

    @property
    def total_duration(self):
        """Total duration in minutes."""
        return sum(l.duration_minutes for l in self.lessons.all() if l.duration_minutes)

    @property
    def difficulty_badge_color(self):
        colors = {
            'beginner': 'success',
            'intermediate': 'warning',
            'advanced': 'danger'
        }
        return colors.get(self.difficulty, 'secondary')

    def __repr__(self):
        return f'<Course {self.title}>'


class Lesson(db.Model):
    """Individual lesson within a course."""
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, default='')  # Text content or description
    video_url = db.Column(db.String(500), default='')  # YouTube embed URL
    lesson_type = db.Column(db.String(20), default='video')  # video, text
    order_num = db.Column(db.Integer, default=0)
    duration_minutes = db.Column(db.Integer, default=0)

    # Relationships
    progress_records = db.relationship('LessonProgress', backref='lesson', lazy='dynamic',
                                       cascade='all, delete-orphan')

    @property
    def youtube_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        url = self.video_url or ''
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'
        elif 'youtube.com/embed/' in url:
            return url
        return url

    def __repr__(self):
        return f'<Lesson {self.title}>'


class Quiz(db.Model):
    """Quiz associated with a course for completion assessment."""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    passing_score = db.Column(db.Integer, default=60)  # Percentage needed to pass

    # Relationships
    questions = db.relationship('QuizQuestion', backref='quiz', lazy='dynamic',
                                cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic',
                               cascade='all, delete-orphan')

    @property
    def total_questions(self):
        return self.questions.count()

    def __repr__(self):
        return f'<Quiz {self.title}>'


class QuizQuestion(db.Model):
    """Multiple choice question within a quiz."""
    __tablename__ = 'quiz_questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(300), nullable=False)
    option_b = db.Column(db.String(300), nullable=False)
    option_c = db.Column(db.String(300), nullable=False)
    option_d = db.Column(db.String(300), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'a', 'b', 'c', or 'd'

    def __repr__(self):
        return f'<QuizQuestion {self.id}>'


class Enrollment(db.Model):
    """Tracks student enrollment and progress in a course."""
    __tablename__ = 'enrollments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    lesson_progress = db.relationship('LessonProgress', backref='enrollment', lazy='dynamic',
                                      cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='enrollment', lazy='dynamic',
                                    cascade='all, delete-orphan')
    certificate = db.relationship('Certificate', backref='enrollment', uselist=False,
                                  cascade='all, delete-orphan')

    # Unique constraint: a student can only enroll once per course
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='unique_enrollment'),)

    @property
    def progress_percentage(self):
        """Calculate overall progress based on completed lessons."""
        total = self.course.total_lessons
        if total == 0:
            return 0
        completed_count = self.lesson_progress.filter_by(completed=True).count()
        return int((completed_count / total) * 100)

    @property
    def lessons_completed_count(self):
        return self.lesson_progress.filter_by(completed=True).count()

    @property
    def quiz_passed(self):
        """Check if student passed any quiz for this course."""
        return self.quiz_attempts.filter_by(passed=True).first() is not None

    @property
    def can_get_certificate(self):
        """Check if student is eligible for certificate (all lessons done + quiz passed)."""
        all_lessons_done = self.progress_percentage == 100
        quiz = self.course.quizzes.first()
        if quiz:
            return all_lessons_done and self.quiz_passed
        return all_lessons_done

    def __repr__(self):
        return f'<Enrollment Student:{self.student_id} Course:{self.course_id}>'


class LessonProgress(db.Model):
    """Tracks individual lesson completion for an enrollment."""
    __tablename__ = 'lesson_progress'

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('enrollment_id', 'lesson_id', name='unique_lesson_progress'),)

    def __repr__(self):
        return f'<LessonProgress Enrollment:{self.enrollment_id} Lesson:{self.lesson_id}>'


class QuizAttempt(db.Model):
    """Records a student's quiz attempt and score."""
    __tablename__ = 'quiz_attempts'

    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer, default=0)  # Percentage score
    passed = db.Column(db.Boolean, default=False)
    attempted_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<QuizAttempt Score:{self.score}% Passed:{self.passed}>'


class Certificate(db.Model):
    """Generated certificate for course completion."""
    __tablename__ = 'certificates'

    id = db.Column(db.Integer, primary_key=True)
    certificate_uid = db.Column(db.String(36), unique=True, nullable=False,
                                default=lambda: str(uuid.uuid4()))
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollments.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_path = db.Column(db.String(500), nullable=True)
    issued_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships (via backref in other models, plus direct access)
    course = db.relationship('Course', backref='certificates')

    def __repr__(self):
        return f'<Certificate {self.certificate_uid}>'
