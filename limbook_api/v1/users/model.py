from limbook_api.db import db, BaseDbModel


class User(BaseDbModel):
    """Users"""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    email_verif_code = db.Column(db.String, nullable=True)
    email_verif_code_expires_on = db.Column(db.DateTime, nullable=True)
    password_reset_code = db.Column(db.String, nullable=True)
    password_reset_code_expires_on = db.Column(db.DateTime, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    profile_picture = db.Column(db.String, nullable=True)
    cover_picture = db.Column(db.String, nullable=True)

    password = db.Column(db.String, nullable=False)
    role_id = db.Column(
        db.Integer, db.ForeignKey('role.id'),
        nullable=False
    )
    role = db.relationship(
        'Role', backref='users', uselist=False,
        lazy=True
    )

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'email_verified': self.email_verified,
            'phone_number': self.phone_number,
            'profile_picture': self.profile_picture,
            'cover_picture': self.cover_picture,
            'role_id': self.role_id,
            'role': self.role.slug,
            'permissions': [p.slug for p in self.role.permissions],
            'created_on': self.created_on.__str__(),
            'updated_on': self.updated_on.__str__(),
        }
