from __future__ import absolute_import, unicode_literals

"""
    Does the best we can to deals with the issue of changing external user models defined in implementations
    http://kevindias.com/writing/django-custom-user-models-south-and-reusable-apps/
"""

try:
    from django.contrib.auth import get_user_model
except ImportError:  # django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()

user_orm_label = '%s.%s' % (User._meta.app_label, User._meta.object_name)
user_model_label = '%s.%s' % (User._meta.app_label, User._meta.model_name)

user_model_definition = {
    'Meta': {
        'object_name': User.__name__,
        'db_table': "'%s'" % User._meta.db_table
    },
    User._meta.pk.attname: (
        'django.db.models.fields.AutoField', [],
        {
            'primary_key': 'True',
            'db_column': "'%s'" % User._meta.pk.column
        },
    ),
}
