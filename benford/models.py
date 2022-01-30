from . import db


class Analysis(db.Model):

    __tablename__ = 'analysis'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    filename = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    column_name = db.Column(
        db.String(80),
        index=True,
        unique=False,
        nullable=False
    )
    created = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=False
    )
    p_value = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )

    chi_square = db.Column(
        db.Float,
        index=False,
        unique=False,
        nullable=False
    )

    benford_confirmed = db.Column(
        db.Boolean,
        index=False,
        unique=False,
        nullable=False
    )

    observed_distribution = db.Column(
        db.PickleType,
        index=False,
        unique=False,
        nullable=False
    )

    expected_distribution = db.Column(
        db.PickleType,
        index=False,
        unique=False,
        nullable=False
    )
