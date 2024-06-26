#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    from distutils.sysconfig import get_python_lib

    os.system(
        f"cp  ./custombase.html  {get_python_lib()}/django/contrib/admin/templates/admin/index.html"
    )

    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mainApp.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
