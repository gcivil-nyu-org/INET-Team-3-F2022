from django.test import TestCase
from bikingapp.models import Event, BookmarkEvent
from django.contrib.auth.models import User


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

    def test_event_has_correct_title(self):
        """Events are given title correctly when saving"""
        event = Event.objects.create(
            title="test event", location="test location", description="test description"
        )
        event.save()
        self.assertEqual("test event", event.title)

    def test_event_has_correct_location(self):
        """Events are given title correctly when saving"""
        event = Event.objects.create(
            title="test event", location="test location", description="test description"
        )
        event.save()
        self.assertEqual("test location", event.location)

    def test_bookmarking_event_possible_user(self):
        """Check if bookmarking an event is working with specific user"""
        event = Event.objects.create(
            title="test event", location="test location", description="test description"
        )
        event.save()
        user = User.objects.create_user(username="testuser", password="12345")
        # login = self.client.login(username="testuser", password="12345")
        bookmark_event = BookmarkEvent.objects.create(user=user, event=event)
        bookmark_event.save()
        self.assertEqual(user, bookmark_event.user)

    def test_bookmarking_event_possible_event(self):
        """Check if bookmarking an event is working with specific event"""
        event = Event.objects.create(
            title="test event", location="test location", description="test description"
        )
        event.save()
        user = User.objects.create_user(username="testuser", password="12345")
        # login = self.client.login(username="testuser", password="12345")
        bookmark_event = BookmarkEvent.objects.create(user=user, event=event)
        bookmark_event.save()
        self.assertEqual(event, bookmark_event.event)

    def test_create_user(self):
        """test if accoutn is being created"""
        user = User.objects.create_user(username="testuser", password="12345")
        user.save()
        get_user = User.objects.get(username="testuser")
        self.assertEqual("testuser", get_user.username)
