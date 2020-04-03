from flask_restplus.fields import String


class PasswordFormat(String):
    """Password field for RestApi"""

    def format(self, value: str) -> str:
        """
        Show masked password
        :param value: Value of field
        :type value: str
        :return: Just an eight stars
        :rtype: str
        """

        return "********"
