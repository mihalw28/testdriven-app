import sys
import unittest

import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

COV = coverage.coverage(
    branch=True, include="project/*", omit=["project/tests/*", "project/config.py"]
)
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """Runs trhe tests without code coverage."""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.session.add(User(username="tomek", email="michal@tomek.com"))
    db.session.add(User(username="michalwaszak", email="michalwaszak@email.com"))
    db.session.commit()


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("project/tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == "__main__":
    cli()
