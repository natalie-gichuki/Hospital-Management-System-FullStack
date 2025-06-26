# migrations/env.py
from __future__ import with_statement

from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
import logging

from flask import current_app

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_metadata():
    return current_app.extensions['migrate'].db.metadata

def run_migrations_online():
    """
    Run migrations in 'online' mode using the Flask app context.
    """
    from app import create_app

    app = create_app()

    # This callback prevents migration scripts if no schema changes exist
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = None

    with app.app_context():
        connectable = current_app.extensions['migrate'].db.engine

        context.configure(
            connection=connectable.connect(),
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
