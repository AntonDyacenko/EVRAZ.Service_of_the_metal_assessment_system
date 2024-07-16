from app import create_app, db, bcrypt
from app.models import User

app = create_app()
app.app_context().push()

hashed_password = bcrypt.generate_password_hash('system').decode('utf-8')
system_user = User(username='System', email='system@messenger.com', password=hashed_password)
db.session.add(system_user)
db.session.commit()
