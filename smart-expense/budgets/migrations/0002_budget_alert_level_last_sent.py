from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("budgets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="budget",
            name="alert_level_last_sent",
            field=models.CharField(
                choices=[("on_track", "On track"), ("warning", "Warning"), ("exceeded", "Exceeded")],
                default="on_track",
                max_length=10,
            ),
        ),
    ]
