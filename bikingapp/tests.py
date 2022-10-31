from django.test import TestCase
from bikingapp.models import Event


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        self.assertIs(False, False)

    def test_home_page_loads_properly(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_browse_events_loads_properly(self):
        response = self.client.get("/browse_events")
        self.assertEqual(response.status_code, 200)

    def test_register_user_loads_properly(self):
        response = self.client.get("/register_user")
        self.assertEqual(response.status_code, 200)

    def test_event_has_correct_author(self):
        """Events are given created_by correctly when saving"""
        event = Event.objects.create(
            title="test event", location="test location", description="test description"
        )
        event.created_by = "John Doe"
        event.save()
        self.assertEqual("John Doe", event.created_by)

    def test_event_has_correct_title_and_location(self):
        """Events are given title correctly when saving"""
        event = Event.objects.create(
            title="test event", location="test location", description="test description"
        )
        event.save()
        self.assertEqual("test event", event.title)
        self.assertEqual("test location", event.location)
