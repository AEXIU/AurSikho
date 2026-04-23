# AurSikho — Part 2: Python Viva & Presentation Guide

This guide is exclusively for you and your team (Ashish & Himanshi) to prepare for your final project submission and **Python Viva** with Prof. Khushbu Kushwaha.

---

## 💻 1. How to Run the Project in VS Code

Follow these exact steps to start the project flawlessly during your presentation:

1. **Open VS Code:** Open the `OCESdemu` folder in VS Code (`File > Open Folder`).
2. **Open the Terminal:** Press `` Ctrl + ` `` (backtick) or go to `Terminal > New Terminal`.
3. **Activate the Virtual Environment:** 
   - **On Mac/Linux:** Type `source venv/bin/activate` and press Enter.
   - **On Windows:** Type `.\venv\Scripts\activate` and press Enter.
   *(You should see `(venv)` appear on the left side of your terminal prompt).*
4. **Run the Server:** Type `python run.py` and press Enter.
5. **Open the Browser:** Command-click (Mac) or Ctrl-click (Windows) on the `http://127.0.0.1:5000` link that appears in the terminal.

> **Pro Tip for Presentation:** Keep the database populated! Use the `khushbu@aursikho.com` (Instructor) and a test Student account so you don't have to waste time typing data during the demo.

---

## 🎤 2. How to Explain the Project to Ma'am

When it's your turn to present, follow this structure to sound confident and technical:

### The Introduction (The "Hook")
*"Good morning Ma'am. Our project is **AurSikho**, a completely free, hybrid Online Course Enrollment System. While platforms like Udemy and Coursera exist, they often lock verifiable certificates behind massive paywalls. We built AurSikho to completely remove that barrier. It allows instructors to seamlessly create courses using both video and text, and automatically rewards students with a verifiable, dynamically generated digital certificate once they pass the final assessment."*

### The Technical Walkthrough (Python Focused)
1. **The Architecture:** *"We built the backend entirely in **Python** using the Flask framework. We didn't just write all the code in one script; we used the **App Factory Pattern** and Flask **Blueprints** to organize our code into modular Python packages (Auth, Courses, Admin, Certificates)."*
2. **The Database (ORM):** *"Instead of writing raw SQL strings, we leveraged Python's Object-Oriented nature using **Flask-SQLAlchemy**. Every table in our database is represented as a Python Class, which ensures strict data integrity and cleaner code."*
3. **The Highlight Feature:** *"Our most complex technical achievement is the **Certificate Engine**. We used the Python `Pillow` (PIL) library to programmatically draw the student's name, course, and date onto a high-resolution PNG template, generating a unique UUID using Python's built-in `uuid` module."*

---

## 🐍 3. Top Python-Specific Viva Questions & Answers

Since this is a Python Programming Lab Viva, the examiner will heavily focus on core Python concepts, libraries, and how you utilized them. Here is how to answer them perfectly:

**Q1: What is Flask, and why did you choose it over Django for this Python project?**
> **Answer:** "Flask is a lightweight, 'micro' web framework written in Python. We chose it over Django because Flask is highly flexible and doesn't force a specific directory structure or ORM on us. It allowed us to hand-pick the exact Python libraries we needed, like SQLAlchemy for the database and Pillow for image generation, keeping the project modular and clean."

**Q2: I see you have `__init__.py` files everywhere. What is their purpose in Python?**
> **Answer:** "In Python, the `__init__.py` file tells the Python interpreter that the directory should be treated as a Python Package. In our `app` folder, it also serves as our **App Factory**, where we initialize the Flask app instance, configure the database, and register our Blueprints."

**Q3: How are you managing different user roles (Student, Instructor, Admin) in Python?**
> **Answer:** "We used **Python Decorators**. A decorator is a function that takes another function and extends its behavior without explicitly modifying it. We wrote custom decorators like `@instructor_required` that wrap around our routes. If a student tries to access an instructor route, the decorator intercepts the request, checks their role, and blocks them."

**Q4: How does the certificate generation actually work using Python?**
> **Answer:** "We used the `Pillow` library, which is the modern version of the Python Imaging Library (PIL). When a student passes, the script loads a blank, high-resolution `.png` file into memory. It then loads TrueType fonts, calculates the exact X/Y coordinates to center the text dynamically, draws the student's name and UUID, and saves the final PNG to our static folder."

**Q5: What is a Virtual Environment (`venv`), and why did you use it?**
> **Answer:** "A virtual environment is an isolated Python environment. We used it so that all the specific dependencies for our project (like Flask 3.1, Pillow, SQLAlchemy) are installed locally in the project folder, rather than globally on the operating system. This prevents version conflicts with other Python projects."

**Q6: I see `@property` used in your database models. What does that do in Python?**
> **Answer:** "The `@property` decorator allows us to define methods in our classes that can be accessed like attributes. For example, in our `Course` model, we wrote a method to calculate `total_duration` by summing up all lesson minutes. Because of `@property`, we can just call `course.total_duration` in our templates without using parentheses."

**Q7: How did you implement security for user passwords?**
> **Answer:** "We never store passwords in plain text. We used the `Werkzeug.security` library to hash passwords using the `PBKDF2:SHA256` encryption algorithm before saving them to the database, ensuring high-level cryptographic security."

**Q8: What is an ORM, and how are you interacting with your database?**
> **Answer:** "ORM stands for Object-Relational Mapper. We use `Flask-SQLAlchemy`. Instead of writing raw SQL queries, we define our database tables as standard Python Classes (Models). The ORM translates our Python code into SQL automatically, protecting us from SQL injection attacks and making the code highly readable."

---
**Good luck with the Viva! You've got an amazing Python project to show off.**
