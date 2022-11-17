from django.test import TestCase
from bikingapp.models import Event, BookmarkEvent
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        self.assertIs(False, False)

    def test_home_page_loads_properly(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_browse_events_loads_properly(self):
        response = self.client.get("/browse_events")
        self.assertEqual(response.status_code, 200)

    def test_map_loads_properly(self):
        response = self.client.get("/map")
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
        """test if account is being created"""
        user = User.objects.create_user(username="testuser", password="12345")
        user.save()
        get_user = User.objects.get(username="testuser")
        self.assertEqual("testuser", get_user.username)

    def test_create_event_after_creating_user(self):
        """test if a new user is able to create events"""
        user = User.objects.create_user(username="testuser", password="12345")
        user.save()
        event = Event.objects.create(
            title="test event",
            location="test location",
            description="test description",
            created_by=user.username,
        )
        event.save()
        self.assertEqual(user.username, event.created_by)
    
    def test_was_published_recently_with_future_question(self):
        self.assertIs(False, False)

    def test_home_page_loads_properly(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_browse_events_loads_properly(self):
        response = self.client.get("/browse_events")
        self.assertEqual(response.status_code, 200)

    def test_map_loads_properly(self):
        response = self.client.get("/map")
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
        """test if account is being created"""
        user = User.objects.create_user(username="testuser", password="12345")
        user.save()
        get_user = User.objects.get(username="testuser")
        self.assertEqual("testuser", get_user.username)

    def test_create_event_after_creating_user(self):
        """test if a new user is able to create events"""
        user = User.objects.create_user(username="testuser", password="12345")
        user.save()
        event = Event.objects.create(
            title="test event",
            location="test location",
            description="test description",
            created_by=user.username,
        )
        event.save()
        self.assertEqual(user.username, event.created_by)
    def setUp(self):
        self.form =SignupForm
        self.user = User.objects.create_user(
            username="test", password="test", email="test@test.com"
        )
        self.request = self.client.get("signup")

    def test_user(self):
        self.client.login(username="test", password="test")
        assert self.user.is_authenticated

    def test_user_can_login(self):
        login = self.client.login(username="test", password="test")
        self.assertEquals(login, True)

    def test_user_cant_login_with_wrong_password(self):
        login = self.client.login(username="test", password="hfhf")
        self.assertEquals(login, False)

    def test_user_cant_see_signup_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get("signup")
        assert response.status_code == 404

    def test_user_cant_see_login_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get("login")
        assert response.status_code == 404

    def test_cant_login_with_username_that_is_taken(self):
        form = SignupForm(
            {
                "username": "test",
                "first_name": "James",
                "last_name": "Joyce",
                "email": "James@Joyce.com",
                "password1": "test",
                "password2": "test",
            }
        )
        self.assertFormError(
            form, "username", "A user with that username already exists." )

    # def test_cant_login_with_email_that_is_taken(self):
    #
    #     form = SignUpForm(
    #         {
    #             "username": "Bloomsday2022",
    #             "first_name": "James",
    #             "last_name": "Joyce",
    #             "email": "test@test.com",
    #             "password1": "test",
    #             "password2": "test",
    #         })
    #     self.assertFormError(form, "email", "A user with that email already exists.")

    def test_form_errors(self):
        form = SignupForm(
            {
                "username": "test",
                "first_name": "James",
                "last_name": "Joyce",
                "email": "test",
                "password1": "123",
                "password2": "123",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors["email"], ["Enter a valid email address."])
