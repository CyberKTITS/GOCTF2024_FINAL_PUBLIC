from app.app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Create all tables
    db.create_all()

    # Check if the admin user already exists
    if not User.query.filter_by(username='Alex').first():
        admin_user = User(username='Alex', isadmin='yes')
        admin_user.set_password('SuperSecret!')
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

