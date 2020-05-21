from django.contrib.auth.hashers import PBKDF2PasswordHasher

class PasswordHasher(PBKDF2PasswordHasher):
    algorithm = 'pbkdf2_wrapped_sha1'

    def encode_sha1_hash(self,sha1_hash, salt=None, iterations=1):
        return super().encode(sha1_hash, salt, iterations)