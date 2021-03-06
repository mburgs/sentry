# Generated by Django 1.11.29 on 2021-02-10 19:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import sentry.db.models.fields.bounded
import sentry.db.models.fields.foreignkey
import sentry.db.models.fields.jsonfield


class Migration(migrations.Migration):
    # This flag is used to mark that a migration shouldn't be automatically run in
    # production. We set this to True for operations that we think are risky and want
    # someone from ops to run manually and monitor.
    # General advice is that if in doubt, mark your migration as `is_dangerous`.
    # Some things you should always mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that
    #   they can be monitored. Since data migrations will now hold a transaction open
    #   this is even more important.
    # - Adding columns to highly active tables, even ones that are NULL.
    is_dangerous = False

    # This flag is used to decide whether to run this migration in a transaction or not.
    # By default we prefer to run in a transaction, but for migrations where you want
    # to `CREATE INDEX CONCURRENTLY` this needs to be set to False. Typically you'll
    # want to create an index concurrently when adding one to an existing table.
    # You'll also usually want to set this to `False` if you're writing a data
    # migration, since we don't want the entire migration to run in one long-running
    # transaction.
    atomic = True

    dependencies = [
        ("sentry", "0159_create_externaluser_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectCodeOwners",
            fields=[
                (
                    "id",
                    sentry.db.models.fields.bounded.BoundedBigAutoField(
                        primary_key=True, serialize=False
                    ),
                ),
                ("date_updated", models.DateTimeField(default=django.utils.timezone.now)),
                ("raw", models.TextField(null=True)),
                ("schema", sentry.db.models.fields.jsonfield.JSONField(null=True)),
                ("date_added", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "organization_integration",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sentry.OrganizationIntegration",
                    ),
                ),
                (
                    "project",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        db_constraint=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sentry.Project",
                    ),
                ),
                (
                    "repository_project_path_config",
                    sentry.db.models.fields.foreignkey.FlexibleForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="sentry.RepositoryProjectPathConfig",
                    ),
                ),
            ],
            options={
                "db_table": "sentry_projectcodeowners",
            },
        ),
    ]
