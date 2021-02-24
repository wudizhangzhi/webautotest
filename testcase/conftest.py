import pytest
import allure
from allure_commons.types import AttachmentType
from PIL import ImageGrab
from io import BytesIO


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport():
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        with BytesIO() as output:
            img = ImageGrab.grab()
            img.save(output, 'PNG')
            data = output.getvalue()
        allure.attach(data, name="异常截图", attachment_type=AttachmentType.PNG)
