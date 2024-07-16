from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    # Проверка, существует ли уже системный пользователь
    system_user = User.query.filter_by(email='system@messenger.com').first()
    if not system_user:
        hashed_password = bcrypt.generate_password_hash('system').decode('utf-8')
        system_user = User(username='System', email='system@messenger.com', password=hashed_password)
        db.session.add(system_user)
        db.session.commit()
        print("Системный пользователь создан.")
    else:
        print("Системный пользователь уже существует.")
