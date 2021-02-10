# Generated by Django 1.11.29 on 2020-05-13 22:23

from django.db import migrations


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
    atomic = True

    dependencies = [("sentry", "0076_alert_rules_disable_constraints")]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterUniqueTogether(name="alertruleenvironment", unique_together=set()),
                migrations.RemoveField(model_name="alertruleenvironment", name="alert_rule"),
                migrations.RemoveField(model_name="alertruleenvironment", name="environment"),
                migrations.RemoveField(model_name="alertrulequerysubscription", name="alert_rule"),
                migrations.RemoveField(
                    model_name="alertrulequerysubscription", name="query_subscription"
                ),
                migrations.AlterUniqueTogether(
                    name="querysubscriptionenvironment", unique_together=set()
                ),
                migrations.RemoveField(
                    model_name="querysubscriptionenvironment", name="environment"
                ),
                migrations.RemoveField(
                    model_name="querysubscriptionenvironment", name="query_subscription"
                ),
                migrations.RemoveField(model_name="alertrule", name="aggregation"),
                migrations.RemoveField(model_name="alertrule", name="dataset"),
                migrations.RemoveField(model_name="alertrule", name="environment"),
                migrations.RemoveField(model_name="alertrule", name="query"),
                migrations.RemoveField(model_name="alertrule", name="query_subscriptions"),
                migrations.RemoveField(model_name="alertrule", name="resolution"),
                migrations.RemoveField(model_name="alertrule", name="time_window"),
                migrations.RemoveField(model_name="querysubscription", name="aggregation"),
                migrations.RemoveField(model_name="querysubscription", name="dataset"),
                migrations.RemoveField(model_name="querysubscription", name="environments"),
                migrations.RemoveField(model_name="querysubscription", name="query"),
                migrations.RemoveField(model_name="querysubscription", name="resolution"),
                migrations.RemoveField(model_name="querysubscription", name="time_window"),
                migrations.DeleteModel(name="AlertRuleEnvironment"),
                migrations.DeleteModel(name="AlertRuleQuerySubscription"),
                migrations.DeleteModel(name="QuerySubscriptionEnvironment"),
            ]
        )
    ]
