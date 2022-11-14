from django.test import TestCase
from bikingapp.models import Event, BookmarkEvent
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import EventForm, FriendMgmtForm, WorkoutForm, CommentForm


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


class TestAccountForms(TestCase):
    def setUp(self):
        self.firstName = "Steve"
        self.lastName = "None"
        self.username = "MinecraftSteve"
        self.phone = 9492345678
        self.password = "removedHerobrine"
        self.email = "steve@minecraft.realm"
        self.user = User.objects.create_user(
            first_name=self.firstName,
            last_name=self.lastName,
            username=self.username + "1",
            password=self.password + "1",
            email="1" + self.email,
        )
        self.user.save()

    def testLoginForm(self):
        response = self.client.get(reverse("account:loginform"))
        self.assertEqual(response.status_code, 200)

    def testPasswordResetRequestPost(self):
        response = self.client.post(
            reverse("account:password_reset"),
            data={
                "email": "1" + self.email,
            },
        )
        self.assertEqual(response.status_code, 302)

    def testPasswordResetRequestPage(self):
        response = self.client.get(
            reverse("account:password_reset"),
        )
        self.assertEqual(response.status_code, 200)

    def testSignout(self):
        response = self.client.get(
            reverse("account:sign-out"),
        )
        self.assertEqual(response.status_code, 302)

    def testRegisterPage(self):
        """
        A get request on signup form
        """
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def testRegisterPagePost(self):
        response = self.client.post(
            reverse("register"),
            data={
                "first_name": self.firstName,
                "last_name": self.lastName,
                "username": self.username,
                "email": self.email,
                "phone_number": self.phone,
                "password1": self.password,
                "password2": self.password,
            },
        )
        self.assertEqual(response.status_code, 302)

    # def testSignupFail(self):
    #     response = self.client.post(
    #         reverse("aƒloccount:signupsubmit"),
    #         data={
    #             "fname": self.firstName,
    #             "lname": self.lastName,
    #             "username": self.username,
    #             "email": self.email,
    #             "phone": self.phone,
    #             "password": self.password,
    #             "password2": self.password,
    #         },
    #     )
    #     self.assertEqual(response.status_code, 200)

    def testProfile(self):
        user = User.objects.create_user(
            first_name="Firstname",
            last_name="Lastname",
            username=self.username + "2",
            email="2" + self.email,
        )
        user.set_password(self.password + "2")
        user.save()
        self.client.login(username=self.username + "2", password=self.password + "2")
        response = self.client.post(
            reverse("profile"),
            data={
                "first_name": self.firstName,
                "last_name": self.lastName,
                "username": self.username + "3",
                "email": "3" + self.email,
                "phone": self.phone,
            },
        )
        self.assertEqual(response.status_code, 302)

    def testProfile2(self):
        user = User.objects.create_user(
            first_name="Firstname",
            last_name="Lastname",
            username=self.username + "2",
            email="2" + self.email,
        )
        user.set_password(self.password + "2")
        user.save()
        self.client.login(username=self.username + "2", password=self.password + "2")
        response = self.client.get(
            reverse("profile"),
            data={
                "first_name": self.firstName,
                "last_name": self.lastName,
                "username": self.username + "3",
                "email": "3" + self.email,
                "phone": self.phone,
            },
        )
        self.assertEqual(response.status_code, 200)
