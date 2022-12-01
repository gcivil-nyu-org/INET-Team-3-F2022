from django.test import TestCase
from bikingapp.models import Event, BookmarkEvent, Workout
from bikingapp.models import CustomUser
from bikingapp.forms import UserRegistrationForm


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        self.assertIs(False, False)

    def test_home_page_loads_properly(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_browse_events_loads_properly(self):
        response = self.client.get("/browse_events")
        self.assertEqual(response.status_code, 200)

    def test_create_events_notloads_properly(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/create_event")
        self.assertEqual(response.status_code, 200)

    def test_map_loads_properly(self):
        response = self.client.get("/map")
        self.assertEqual(response.status_code, 200)

    def test_workout_history_loads_properly(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/workout_history")
        self.assertEqual(response.status_code, 200)

    def test_log_workout_loads_properly(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/log_workout")
        self.assertEqual(response.status_code, 200)

    def test_discussion_loads_properly(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/post")
        self.assertEqual(response.status_code, 200)

    def test_discussion_new_notloads_properly(self):
        self.client.login(username="test", password="test")
        response = self.client.get("/post/new")
        self.assertEqual(response.status_code, 301)

    def test_register_user_loads_properly(self):
        response = self.client.get("/register")
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
        user = CustomUser.objects.create_user(username="testuser", password="12345")
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
        user = CustomUser.objects.create_user(username="testuser", password="12345")
        # login = self.client.login(username="testuser", password="12345")
        bookmark_event = BookmarkEvent.objects.create(user=user, event=event)
        bookmark_event.save()
        self.assertEqual(event, bookmark_event.event)

    def test_create_user(self):
        """test if account is being created"""
        user = CustomUser.objects.create_user(username="testuser", password="12345")
        user.save()
        get_user = CustomUser.objects.get(username="testuser")
        self.assertEqual("testuser", get_user.username)

    def test_create_event_after_creating_user(self):
        """test if a new user is able to create events"""
        user = CustomUser.objects.create_user(username="testuser", password="12345")
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
        self.form = UserRegistrationForm
        self.user = CustomUser.objects.create_user(
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
        form = UserRegistrationForm(
            {
                "username": "test",
                "first_name": "James",
                "last_name": "Joyce",
                "email": "James@Joyce.com",
                "password1": "test",
                "password2": "test",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors["username"], ["A user with that username already exists."]
        )

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
        form = UserRegistrationForm(
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

    def test_workout_has_correct_title(self):
        """Events are given title correctly when saving"""
        work = Workout.objects.create(
            title="test title", miles="1", description="test description"
        )
        work.save()
        self.assertEqual("test title", work.title)

    def test_workout_has_correct_date(self):
        """Events are given title correctly when saving"""
        work = Workout.objects.create(
            title="test title",
            miles="1",
            description="test description",
            date="2022-11-15",
        )
        work.save()
        self.assertEqual("2022-11-15", work.date)

    def test_workout_has_correct_miles(self):
        """Events are given title correctly when saving"""
        work = Workout.objects.create(
            title="test title",
            miles="1",
            description="test description",
            date="2022-11-15",
        )
        work.save()
        self.assertEqual("1", work.miles)

    def test_workout_has_correct_desc(self):
        """Events are given title correctly when saving"""
        work = Workout.objects.create(
            title="test title",
            miles="1",
            description="test description",
            date="2022-11-15",
        )
        work.save()
        self.assertEqual("test description", work.description)

    def test_workout_has_correct_starttime(self):
        """Events are given title correctly when saving"""
        work = Workout.objects.create(
            title="test title",
            miles="1",
            description="test description",
            time_start="16:11:40",
        )
        work.save()
        self.assertEqual("16:11:40", work.time_start)

    def test_workout_has_correct_endtime(self):
        """Events are given title correctly when saving"""
        work = Workout.objects.create(
            title="test title",
            miles="1",
            description="test description",
            time_end="16:50:40",
        )
        work.save()
        self.assertEqual("16:50:40", work.time_end)

    def test_first_name_label(self):
        author = CustomUser.objects.get(id=1)
        field_label = author._meta.get_field("first_name").verbose_name
        self.assertEqual(field_label, "first name")

    def test_last_name_label(self):
        author = CustomUser.objects.get(id=1)
        field_label = author._meta.get_field("last_name").verbose_name
        self.assertEqual(field_label, "last name")

    def test_desc_name_label(self):
        author = CustomUser.objects.get(id=1)
        field_label = author._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Description")
    def test_first_name_max_length(self):
        author = CustomUser.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertFalse(max_length, 150)
