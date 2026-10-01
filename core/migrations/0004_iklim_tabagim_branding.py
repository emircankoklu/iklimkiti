from django.db import migrations, models


def update_homepage_branding(apps, schema_editor):
    homepage_model = apps.get_model('core', 'HomePageContent')
    for homepage in homepage_model.objects.all().iterator():
        homepage.hero_description = homepage.hero_description.replace('İklimKiti', 'İklim Tabağım')
        homepage.assistant_title = homepage.assistant_title.replace('İklimKiti', 'İklim Tabağım')
        homepage.save(update_fields=['hero_description', 'assistant_title'])


def restore_homepage_branding(apps, schema_editor):
    homepage_model = apps.get_model('core', 'HomePageContent')
    for homepage in homepage_model.objects.all().iterator():
        homepage.hero_description = homepage.hero_description.replace('İklim Tabağım', 'İklimKiti')
        homepage.assistant_title = homepage.assistant_title.replace('İklim Tabağım', 'İklimKiti')
        homepage.save(update_fields=['hero_description', 'assistant_title'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_chatpromptlog'),
    ]

    operations = [
        migrations.RunPython(update_homepage_branding, restore_homepage_branding),
        migrations.AlterField(
            model_name='homepagecontent',
            name='hero_description',
            field=models.TextField(default='İklim Tabağım ile gıda güvenliği, sürdürülebilir yaşam ve iklim değişikliği hakkında öğren, keşfet ve oyunlarla kendini geliştir.'),
        ),
        migrations.AlterField(
            model_name='homepagecontent',
            name='assistant_title',
            field=models.CharField(default='İklim Tabağım Asistanı', max_length=200),
        ),
    ]
