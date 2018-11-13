import pytest


@pytest.fixture(autouse=True)
def set_qsettings_value(qapp, request):
    """Set application name dynamically and org name fixed"""
    app_name = '%s.%s' % (request.module.__name__, request.function.__name__)
    qapp.setOrganizationName('hellomoto')
    qapp.setApplicationName(app_name)
