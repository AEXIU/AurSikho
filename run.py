"""
Aursikho — Online Course Enrollment System
Entry point: creates the app, seeds default admin, and runs the dev server.
"""
from app import create_app, db
from app.models import User

app = create_app()


def seed_admin():
    """Create a default admin user if none exists."""
    with app.app_context():
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@aursikho.com',
                full_name='Platform Admin',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print('[+] Default admin created: admin@aursikho.com / admin123')


if __name__ == '__main__':
    seed_admin()
    app.run(debug=True, port=5000)
