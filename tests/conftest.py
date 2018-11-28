import pytest
from PyQt5 import QtCore


@pytest.fixture(autouse=True)
def set_qsettings_value(qapp, request):
    """Set application name dynamically and clear stored settings"""
    app_name = 'bci_learning_studio.%s.%s' % (
        request.module.__name__, request.function.__name__)
    qapp.setOrganizationName('hellomoto')
    qapp.setApplicationName(app_name)
    QtCore.QSettings().clear()
