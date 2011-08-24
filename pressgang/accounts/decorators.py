
from django.contrib.auth.decorators import permission_required

# Decorators for user blog management permissions
can_install_blogs = permission_required('pressgang.can_install_blogs')
can_manage_blogs = permission_required('pressgang.can_manage_blogs')
can_view_blogs = permission_required('pressgang.can_view_blogs')
