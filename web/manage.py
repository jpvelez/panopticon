#!/usr/bin/env python
import os
import sys
import site

if __name__ == '__main__':

#     # ---------- do something here to ensure virtualenv working correctly?
#     # manipulate the path to use virtualenv only when running
#     # locally. this is also what we do in the django.wsgi files but need
#     # to also do this here so that locally run django instances are not
#     # dependent on locally installed packages that are not in
#     # virtualenv. inspired by
#     # http://jmoiron.net/blog/deploying-django-mod-wsgi-virtualenv/
#     venv = os.path.join(PROJECT_DIR, "env", "lib", "python2.6", "site-packages")
#     prev_sys_path = list(sys.path)
#     site.addsitedir(venv)
#     sys.path.append(PROJECT_DIR)
#     new_sys_path = [p for p in sys.path if p not in prev_sys_path]
#     for item in new_sys_path:
#         sys.path.remove(item)
#     sys.path[:0] = new_sys_path
#     # NOTE: this only **prepends** the virtualenv stuff. it does NOT
#     # remove all of the existing site packages that come from running this
#     # script with the local python interpreter
# 
#     # activate the virtual environment --- this must be done very early in
#     # the manage.py script to use the correct version of django
#     setup_virtualenv_command = 'setup_virtualenv'
#     activate_this = os.path.join(PROJECT_DIR, 'env', 'bin', 'activate_this.py')
#     execfile(activate_this, dict(__file__=activate_this))

    # --------------------------- below is the original manage.py script
    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)
