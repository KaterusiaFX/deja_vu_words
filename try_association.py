from webapp import create_app
from webapp.db import db
from webapp.user.models import Association, Parent, Child

app = create_app()


with app.app_context():
    p = Parent.query.filter(Parent.id).first()
    print(p)
    a = Association(extra_data="some data")
    c = Child.query.filter(Child.id).first()
    print(c)
    a.child = c
    p.children.append(a)
    db.session.add(p)
    db.session.commit()