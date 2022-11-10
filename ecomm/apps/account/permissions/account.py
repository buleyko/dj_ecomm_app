# from django.contrib.auth.models import Permission
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.auth import get_user_model
# Account = get_user_model()

# content_type = ContentType.objects.get_for_model(Account)
# dashboard_page_permission = Permission.objects.create(
#     codename='view_dashboard',
#     name='View Dashboard page',
#     content_type=content_type,
# )