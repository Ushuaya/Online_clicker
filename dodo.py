"""Make automatization."""

import glob
from doit.tools import create_folder


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o Clicker.pot ClickerMSU'],
            'file_dep': glob.glob('ClickerMSU/*.py'),
            'targets': ['Clicker.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D Clicker -d po -i Clicker.pot'],
            'file_dep': ['Clicker.pot'],
            'targets': ['po/ru/LC_MESSAGES/Clicker.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['ClickerMSU/ru/LC_MESSAGES']),
                'pybabel compile -D Clicker -l ru -i po/ru/LC_MESSAGES/Clicker.po -d ClickerMSU'
                       ],
            'file_dep': ['po/ru/LC_MESSAGES/Clicker.po'],
            'targets': ['ClickerMSU/ru/LC_MESSAGES/Clicker.mo'],
           }


def task_test():
    """Perform tests."""
    return {
            'actions': ['python3 -m unittest -b'],
           }


def task_html():
    """Make HTML documentationi."""
    return {
            'actions': ['sphinx-build -M html docs build'],
           }

def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -xdf'],
           }

def task_sdist():
    """Create source distribution."""
    return {
            'actions': ['python -m build -s'],
            'task_dep': ['gitclean'],
           }

def task_wheel():
    """Create binary wheel distribution."""
    return {
            'actions': ['python -m build -w'],
            'task_dep': ['mo'],
           }

def task_app():
    """Run application."""
    return {
            'actions': ['python -m ClickerMSU'],
            'task_dep': ['mo'],
           }

def task_style():
    """Check style with flake8."""
    return {
            'actions': ['flake8 ClickerMSU']
           }

def task_docstyle():
    """Check docstrings with pydocstyle."""
    return {
            'actions': ['pydocstyle ClickerMSU']
           }

def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle', 'test']
           }

def task_publish():
    """Publish distros on test.pypi.org"""
    return {
            'task_dep': ['sdist', 'wheel'],
            'actions': ['twine upload -u __token__ --repository testpypi dist/*'],
            'verbosity': 2
           }
