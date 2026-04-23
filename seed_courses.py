import os
from app import create_app, db
from app.models import User, Course, Lesson, Quiz, QuizQuestion

app = create_app()

def seed_python_course():
    with app.app_context():
        # Check if the instructor exists
        instructor = User.query.filter_by(username='khushbu').first()
        if not instructor:
            instructor = User(
                username='khushbu',
                email='khushbu@aursikho.com',
                full_name='Prof. Khushbu Kushwaha',
                role='instructor',
                bio='Expert Python Educator and Guide.'
            )
            instructor.set_password('password123')
            db.session.add(instructor)
            db.session.commit()
            print("Created Instructor: Prof. Khushbu Kushwaha")
        
        # Check if course exists
        course = Course.query.filter_by(title='Complete Python Masterclass for Beginners').first()
        if not course:
            course = Course(
                title='Complete Python Masterclass for Beginners',
                short_description='Master Python programming from scratch with hands-on examples.',
                description='This comprehensive hybrid course covers everything from basic syntax to advanced functions. Perfect for beginners, it combines high-quality video lectures with detailed text references and concludes with a challenging quiz.',
                category='Programming',
                difficulty='beginner',
                is_published=True,
                instructor_id=instructor.id
            )
            db.session.add(course)
            db.session.commit()
            print("Created Course: Python Masterclass")
            
            # Add Lessons
            lessons_data = [
                {
                    'title': '1. Introduction to Python',
                    'lesson_type': 'video',
                    'video_url': 'https://www.youtube.com/watch?v=kqtD5dpn9C8',
                    'content': '<p>Welcome to the Python Masterclass! Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.</p>',
                    'duration_minutes': 71,
                    'order_num': 1
                },
                {
                    'title': '2. Variables & Data Types',
                    'lesson_type': 'hybrid',
                    'video_url': 'https://www.youtube.com/watch?v=khKv-8q7YmY',
                    'content': '<h3>Variables in Python</h3><p>Variables are containers for storing data values. Unlike other programming languages, Python has no command for declaring a variable. A variable is created the moment you first assign a value to it.</p><pre><code>x = 5\ny = "John"</code></pre>',
                    'duration_minutes': 15,
                    'order_num': 2
                },
                {
                    'title': '3. Control Flow (If...Else)',
                    'lesson_type': 'hybrid',
                    'video_url': 'https://www.youtube.com/watch?v=PqFKRqpHrjw',
                    'content': '<p>Python supports the usual logical conditions from mathematics. These conditions can be used in several ways, most commonly in "if statements" and loops.</p><pre><code>a = 33\nb = 200\nif b > a:\n  print("b is greater than a")</code></pre>',
                    'duration_minutes': 20,
                    'order_num': 3
                },
                {
                    'title': '4. Python Functions',
                    'lesson_type': 'video',
                    'video_url': 'https://www.youtube.com/watch?v=9Os0o3wzS_I',
                    'content': '<p>A function is a block of code which only runs when it is called. You can pass data, known as parameters, into a function. A function can return data as a result.</p>',
                    'duration_minutes': 25,
                    'order_num': 4
                }
            ]
            
            for l_data in lessons_data:
                lesson = Lesson(course_id=course.id, **l_data)
                db.session.add(lesson)
            db.session.commit()
            print("Created 4 Python Lessons")
            
            # Add Quiz
            quiz = Quiz(
                course_id=course.id,
                title='Final Python Assessment',
                passing_score=75
            )
            db.session.add(quiz)
            db.session.commit()
            
            questions = [
                {
                    'question_text': 'What is the correct file extension for Python files?',
                    'option_a': '.pt',
                    'option_b': '.py',
                    'option_c': '.pyt',
                    'option_d': '.ptn',
                    'correct_answer': 'b'
                },
                {
                    'question_text': 'How do you create a variable with the numeric value 5?',
                    'option_a': 'x = 5',
                    'option_b': 'x = int(5)',
                    'option_c': 'Both A and B are correct',
                    'option_d': 'int x = 5',
                    'correct_answer': 'c'
                },
                {
                    'question_text': 'Which of the following is used to define a block of code in Python language?',
                    'option_a': 'Indentation',
                    'option_b': 'Key',
                    'option_c': 'Brackets',
                    'option_d': 'All of the mentioned',
                    'correct_answer': 'a'
                },
                {
                    'question_text': 'Which keyword is used for function in Python language?',
                    'option_a': 'Function',
                    'option_b': 'def',
                    'option_c': 'Fun',
                    'option_d': 'Define',
                    'correct_answer': 'b'
                }
            ]
            
            for q_data in questions:
                q = QuizQuestion(quiz_id=quiz.id, **q_data)
                db.session.add(q)
            db.session.commit()
            print("Created Final Quiz with 4 Questions")
            
        else:
            print("Python course already seeded.")

if __name__ == '__main__':
    seed_python_course()
