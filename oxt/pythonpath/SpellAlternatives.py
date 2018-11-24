import unohelper
from com.sun.star.linguistic2 import XSpellAlternatives
from com.sun.star.linguistic2.SpellFailure import SPELLING_ERROR

class SpellAlternatives(unohelper.Base, XSpellAlternatives):

	def __init__(self, word, alternatives, locale):
		self.__word = word
		self.__alternatives = alternatives
		self.__locale = locale

	def getWord(self):
		return self.__word

	def getLocale(self):
		return self.__locale

	def getFailureType(self):
		return SPELLING_ERROR

	def getAlternativesCount(self):
		return len(self.__alternatives)

	def getAlternatives(self):
		return tuple(self.__alternatives)
