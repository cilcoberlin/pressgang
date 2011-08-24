
from django import forms
from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str

import os
from base64 import b64decode, b64encode
from Crypto.Cipher import ARC4

class EncryptedCharField(models.TextField):
	"""A field that stores short text data in an encrypted format."""

	__metaclass__ = models.SubfieldBase

	_SALT_SIZE = 8

	@classmethod
	def encrypt(cls, plaintext):
		if plaintext is None:
			return None
		salt = os.urandom(cls._SALT_SIZE)
		cipher = ARC4.new(salt + settings.SECRET_KEY)
		plaintext = smart_str(plaintext)
		plaintext = "%3d%s%s" % (len(plaintext), plaintext, os.urandom(256 - len(plaintext)))
		return "%s$%s" % (b64encode(salt), b64encode(cipher.encrypt(plaintext)))

	@classmethod
	def decrypt(cls, ciphertext):
		salt, ciphertext = [b64decode(part) for part in ciphertext.split('$')]
		cipher = ARC4.new(salt + settings.SECRET_KEY)
		plaintext = cipher.decrypt(ciphertext)
		return plaintext[3:3 + int(plaintext[:3].strip())]

	def formfield(self, **kwargs):
		"""Use a password input for all encrypted values."""
		defaults = {'widget': forms.PasswordInput}
		defaults.update(kwargs)
		return super(EncryptedCharField, self).formfield(**defaults)

	def to_python(self, value):
		"""Decrypt the stored value if it needs it."""
		try:
			return EncryptedCharField.decrypt(value)
		except (AttributeError, TypeError, ValueError):
			return value

	def get_prep_value(self, value):
		"""Encrypt the value when saving."""
		return EncryptedCharField.encrypt(value)
