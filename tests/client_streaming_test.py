from aiosignalrcore.subject import Subject
from tests.base_test_case import BaseTestCase, Urls


class TestClientStreamMethod(BaseTestCase):
    def test_stream(self):
        self.complete = False
        self.items = list(range(0, 10))
        subject = Subject()
        self.connection.send("UploadStream", subject)
        while len(self.items) > 0:
            subject.next(str(self.items.pop()))
        subject.complete()
        self.assertTrue(len(self.items) == 0)


class TestClientStreamMethodMsgPack(TestClientStreamMethod):
    def get_connection(self):
        return super().get_connection(msgpack=True)


class TestClientNosslStreamMethodMsgPack(TestClientStreamMethodMsgPack):
    server_url = Urls.server_url_no_ssl


class TestClientNosslStreamMethod(TestClientStreamMethod):
    server_url = Urls.server_url_no_ssl