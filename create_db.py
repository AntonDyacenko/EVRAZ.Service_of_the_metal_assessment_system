from app import create_app, db, bcrypt
from app.models import User

app = create_app()

with app.app_context():
    # Проверка, существует ли уже системный пользователь
    system_user = User.query.filter_by(email='system@messenger.com').first()

    if not system_user:
        # Если системного пользователя нет, создаем его с изображением system.png
        hashed_password = bcrypt.generate_password_hash('system').decode('utf-8')
        system_user = User(username='System', email='system@messenger.com', password=hashed_password,
                           image_file='system.png')
        db.session.add(system_user)
        db.session.commit()
        print("Системный пользователь создан.")
    else:
        # Если системный пользователь уже существует, проверяем его аватарку
        if system_user.image_file != 'system.jpg':
            # Если у него нет аватарки system.jpg или она называется иначе, заменяем на system.png
            system_user.image_file = 'system.png'
            db.session.commit()
            print("Аватарка системного пользователя обновлена.")
        else:
            print("Аватарка системного пользователя уже корректная (system.jpg).")
