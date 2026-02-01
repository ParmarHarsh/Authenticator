from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation.
    Includes user.is_active in the hash to ensure token validity.
    """
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp) + text_type(user.is_active))

generate_token = TokenGenerator()