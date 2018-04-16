from pypom import Page
from selenium.webdriver.common.by import By


class SignupPage(Page):

    _username_field_locator = (By.CSS_SELECTOR, "#id_username")
    _email_field_locator = (By.CSS_SELECTOR, "#id_email")
    _password_field_locator = (By.CSS_SELECTOR, "#id_password1")
    _password_confirmation_field_locator = (By.CSS_SELECTOR, "#id_password2")
    _create_account_button_locator = (By.CSS_SELECTOR, "button[type=submit]")


class BoardsPage(Page):

    _navbar_locator = (By.CSS_SELECTOR, "nav")
    _user_menu_locator = (By.CSS_SELECTOR, "#userMenu")
    _burger_menu_locator = (By.CSS_SELECTOR, ".navbar-toggler")
    _board_link_locator = (By.CSS_SELECTOR, "td > a")

    @property
    def loaded(self):
        return self.is_element_displayed(*self._navbar_locator)

    def is_user_menu_displayed(self):
        return self.is_element_displayed(*self._user_menu_locator)

    def is_burger_menu_displayed(self):
        return self.is_element_displayed(*self._user_menu_locator)

    def is_board_link_displayed(self):
        return self.is_element_displayed(*self._board_link_locator)


class LoginPage(Page):

    _username_field_locator = (By.CSS_SELECTOR, "#id_username")
    _password_field_locator = (By.CSS_SELECTOR, "#id_password")
    _login_button_locator = (By.CSS_SELECTOR, "button[type=submit]")

    def login_user(self, username, password):
        self.find_element(*self._username_field_locator).send_keys(username)
        self.find_element(*self._password_field_locator).send_keys(password)
        self.find_element(*self._login_button_locator).click()


class TopicsPage(Page):

    _new_topic_button_locator = (By.CSS_SELECTOR, "#new_topic")
    _navbar_locator = (By.CSS_SELECTOR, "nav")
    _topics_table_locator = (By.CSS_SELECTOR, "#topics_table")

    def is_topics_table_displayed(self):
        return self.is_element_displayed(*self._topics_table_locator)

    @property
    def loaded(self):
        return self.is_element_displayed(*self._navbar_locator)


class NewTopicPage(Page):
    _subject_field_locator = (By.CSS_SELECTOR, "#id_subject")
    _message_field_locator = (By.CSS_SELECTOR, "#id_message")
    _post_button_locator = (By.CSS_SELECTOR, "button[type=submit]")

    @property
    def loaded(self):
        return self.is_element_displayed(*self._post_button_locator)


class TopicViewPage(Page):

    _first_post_locator = (By.CSS_SELECTOR, ".card.border-dark")
    _first_post_subject_locator = (By.CSS_SELECTOR, ".card-header")
    _first_post_message_locator = (By.CSS_SELECTOR, ".card-body p")
    _navbar_locator = (By.CSS_SELECTOR, "nav")

    @property
    def loaded(self):
        return self.is_element_displayed(*self._navbar_locator)

    def is_first_message_displayed(self):
        return self.is_element_displayed(*self._first_post_locator)

