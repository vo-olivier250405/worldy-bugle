import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('feeds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('resume', models.TextField()),
                ('country', models.CharField(max_length=3)),
                ('url', models.URLField()),
                ('published_at', models.DateTimeField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feeds.source')),
            ],
        ),
    ]
