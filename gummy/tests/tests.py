from .pages import SignupPage, BoardsPage, LoginPage, TopicsPage, NewTopicPage, TopicViewPage
from django.contrib.auth.models import User
from boards.models import Board
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver


class SignupTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.get(cls.live_server_url + '/signup/')
        cls.signup_page = SignupPage(cls.selenium)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_signup_success(self):
        # Checks that user is registered and logged in (boards page is opened and user menu is displayed)
        self.signup_page.find_element(*self.signup_page._username_field_locator).send_keys('testuser')
        self.signup_page.find_element(*self.signup_page._email_field_locator).send_keys('test@test.com')
        self.signup_page.find_element(*self.signup_page._password_field_locator).send_keys('qwerty123')
        self.signup_page.find_element(*self.signup_page._password_confirmation_field_locator).send_keys('qwerty123')
        self.signup_page.find_element(*self.signup_page._create_account_button_locator).click()
        boards_page = BoardsPage(self.selenium)
        boards_page.wait_for_page_to_load()
        self.assertTrue(boards_page.is_user_menu_displayed())


class LoginTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.get(cls.live_server_url + '/login/')
        cls.login_page = LoginPage(cls.selenium)
        User.objects.create_user(username='testuser', email='test@test.com', password='qwerty123')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_success(self):
        # Checks that user is logged in (boards page is opened and user menu is displayed)
        self.login_page.find_element(*self.login_page._username_field_locator).send_keys('testuser')
        self.login_page.find_element(*self.login_page._password_field_locator).send_keys('qwerty123')
        self.login_page.find_element(*self.login_page._login_button_locator).click()
        boards_page = BoardsPage(self.selenium)
        boards_page.wait_for_page_to_load()
        self.assertTrue(boards_page.is_user_menu_displayed())


class BoardsTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Board.objects.create(name='Django', description='Django Board')
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.get(cls.live_server_url)
        cls.boards_page = BoardsPage(cls.selenium)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_board_is_opened(self):
        # Checks that link to created board opens that boards page
        self.boards_page.find_element(*self.boards_page._board_link_locator).click()
        topics_page = TopicsPage(self.selenium)
        topics_page.wait_for_page_to_load()
        self.assertTrue(topics_page.is_topics_table_displayed())


class NewTopicTestsLoggedOut(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Board.objects.create(name='Django', description='Django Board')
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.get(cls.live_server_url)
        boards_page = BoardsPage(cls.selenium)
        boards_page.find_element(*boards_page._board_link_locator).click()
        cls.topics_page = TopicsPage(cls.selenium)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_new_topic_opens_login_page(self):
        # Checks that new topic button opens login page when user is not logged in
        self.topics_page.find_element(*self.topics_page._new_topic_button_locator).click()
        self.assertTrue('/login/' in self.selenium.current_url)


class NewTopicTestsLoggedIn(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Board.objects.create(name='Django', description='Django Board')
        User.objects.create_user(username='testuser', email='test@test.com', password='qwerty123')
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)
        cls.selenium.set_window_size(1024, 768)
        cls.selenium.get(cls.live_server_url + '/login/')
        cls.login_page = LoginPage(cls.selenium)
        cls.login_page.login_user('testuser', 'qwerty123')
        cls.boards_page = BoardsPage(cls.selenium)
        cls.boards_page.wait_for_page_to_load()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_new_topic_is_created(self):
        # Checks that new topic is created and user is redirected to created topic page
        self.boards_page.find_element(*self.boards_page._board_link_locator).click()
        topics_page = TopicsPage(self.selenium).wait_for_page_to_load()
        topics_page.find_element(*topics_page._new_topic_button_locator).click()
        new_topic_page = NewTopicPage(self.selenium).wait_for_page_to_load()
        new_topic_page.find_element(*new_topic_page._subject_field_locator).send_keys("Test Subject")
        new_topic_page.find_element(*new_topic_page._message_field_locator).send_keys("Test Message")
        new_topic_page.find_element(*new_topic_page._post_button_locator).click()
        topic_view_page = TopicViewPage(self.selenium)
        topic_view_page.wait_for_page_to_load()
        # Check that first message container is displayed
        self.assertTrue(topic_view_page.is_first_message_displayed())
        # Check that entered before subject is displayed
        self.assertEqual(topic_view_page.find_element(*topic_view_page._first_post_subject_locator).text,
                         "Test Subject")
        # Check that entered before message is displayed
        self.assertEqual(topic_view_page.find_element(*topic_view_page._first_post_message_locator).text,
                         "Test Message")
