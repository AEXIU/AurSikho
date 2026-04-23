# AurSikho — Part 2: Viva & Presentation Guide

This guide is exclusively for you and your team (Ashish & Himanshi) to prepare for your final project submission and Viva with Prof. Khushbu Kushwaha.

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

### The Technical Walkthrough
1. **The Architecture:** *"We built the backend using Python and the Flask framework. We didn't just write all the code in one file; we used the **App Factory Pattern** and **Blueprints** to separate our code into clean modules (Auth, Courses, Admin, Certificates). This makes our codebase highly scalable."*
2. **The Database:** *"For our database, we are using SQLite mapped via Flask-SQLAlchemy. We designed 9 relational tables including Users, Courses, Enrollments, and Quiz Attempts, ensuring strict data integrity."*
3. **The Highlight Feature:** *"Our most complex technical achievement is the **Certificate Engine**. We didn't use an external API. We used the Python `Pillow` (PIL) library to programmatically draw the student's name, course, and date onto a high-resolution PNG template, generating a unique UUID that makes every certificate publicly verifiable on our platform."*

---

## ❓ 3. Top Viva Questions & Answers

Your external examiner or guide will likely ask technical questions to ensure you wrote the code. Here is how to answer them:

**Q1: What architecture does your Flask app follow?**
> **Answer:** "It follows the MVT (Model-View-Template) architecture. We used SQLAlchemy for the Models, Flask Blueprints for the Views (Routing), and Jinja2 with Bootstrap 5 for the Templates."

**Q2: How did you implement security for user passwords?**
> **Answer:** "We never store passwords in plain text. We used the `Werkzeug.security` library to hash passwords using the `PBKDF2:SHA256` encryption algorithm before saving them to the database."

**Q3: How are you managing different user roles (Student, Instructor, Admin)?**
> **Answer:** "We added a `role` column to our User model. We then wrote custom Python decorators (like `@instructor_required`) that wrap around our routes. If a student tries to access an instructor route, the decorator intercepts the request, blocks it, and redirects them."

**Q4: How does the certificate generation actually work?**
> **Answer:** "When a student passes a quiz, the system checks if their progress is 100%. If yes, we invoke the `Pillow` image library. The script loads a blank, high-resolution base template, loads TrueType fonts (like Great Vibes and Roboto), calculates the exact X/Y coordinates to center the text, draws the student's name and UUID, and saves the final PNG to our static folder."

**Q5: How are the YouTube videos playing on your site without violating CORS?**
> **Answer:** "We don't host the massive video files on our server. Instructors simply paste a standard YouTube link. We wrote a Python property in our `Lesson` model that parses the URL and automatically converts it into a secure YouTube `<iframe>` embed link."

**Q6: Why did you choose SQLite instead of MySQL or MongoDB?**
> **Answer:** "SQLite is a lightweight, serverless relational database that stores data in a single file (`aursikho.db`). Since this is a semester project, SQLite provides all the necessary relational integrity (Foreign Keys, Joins) without the overhead of configuring a separate database server. However, because we used the SQLAlchemy ORM, we could easily migrate to PostgreSQL or MySQL simply by changing one line of code in our `config.py`."

---
**Good luck with the Viva! You've got an amazing project to show off.**
