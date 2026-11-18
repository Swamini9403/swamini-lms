from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(name="course", options={"ordering": ["module_no", "id"]}),
        migrations.AddField(model_name="course", name="module_no", field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name="lesson", name="summary", field=models.TextField(blank=True)),
        migrations.AddField(
            model_name="lesson",
            name="video_id",
            field=models.CharField(blank=True, help_text="YouTube video ID", max_length=20),
        ),
        migrations.AddField(model_name="lesson", name="video_title", field=models.CharField(blank=True, max_length=200)),
        migrations.AddField(model_name="lesson", name="channel", field=models.CharField(blank=True, max_length=120)),
    ]
