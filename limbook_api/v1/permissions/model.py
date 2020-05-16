from limbook_api.db import db, BaseDbModel

role_permission = db.Table(
    'role_permission',
    db.Column(
        'role_id', db.Integer,
        db.ForeignKey('role.id', ondelete="cascade"),
        primary_key=True
    ),
    db.Column(
        'permission_id', db.Integer,
        db.ForeignKey('permission.id'),
        primary_key=True
    )
)


class Permission(BaseDbModel):
    """Permissions"""

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    role = db.relationship(
        'Role', secondary=role_permission,
        backref=db.backref('permissions', lazy=True)
    )

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'created_on': self.created_on.__str__(),
            'updated_on': self.updated_on.__str__(),
        }
