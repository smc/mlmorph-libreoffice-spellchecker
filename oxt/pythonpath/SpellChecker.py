import logging
import unohelper
from com.sun.star.linguistic2 import XSpellChecker, XLinguServiceEventBroadcaster
from com.sun.star.lang import Locale
from com.sun.star.lang import XServiceInfo, XInitialization, XServiceDisplayName

from mlmorph import Analyser
from mlmorph_spellchecker import spellcheck, getSuggestions

from SpellAlternatives import SpellAlternatives

class SpellChecker(unohelper.Base, XServiceInfo, XSpellChecker, XLinguServiceEventBroadcaster, XInitialization, XServiceDisplayName):

	def __init__(self, ctx, *args):
		self.analyser = Analyser()
		logging.debug("SpellChecker.__init__")

	# From XServiceInfo
	def getImplementationName(self):
		return SpellChecker.IMPLEMENTATION_NAME

	def supportsService(self, serviceName):
		return serviceName in self.getSupportedServiceNames()

	def getSupportedServiceNames(self):
		return SpellChecker.SUPPORTED_SERVICE_NAMES

	# From XSupportedLocales
	def getLocales(self):
		locales = [Locale("ml", "IN", "")]
		return tuple(locales)

	def hasLocale(self, aLocale):
		if aLocale.Language == "ml" and aLocale.Country == "IN":
			return True
		return False

	# From XSpellChecker
	def isValid(self, word, locale, properties):
		return spellcheck(word, self.analyser)

	def spell(self, word, locale, properties):
		suggestions = getSuggestions(word, self.analyser)
		return SpellAlternatives(word, suggestions, locale)

	# From XLinguServiceEventBroadcaster
	def addLinguServiceEventListener(self, xLstnr):
		logging.debug("SpellChecker.addLinguServiceEventListener")
		return True

	def removeLinguServiceEventListener(self, xLstnr):
		logging.debug("SpellChecker.removeLinguServiceEventListener")
		return True

	# From XInitialization
	def initialize(self, seq):
		pass

	# From XServiceDisplayName
	def getServiceDisplayName(self, locale):
		if locale.Language == "ml":
			return "Mlmorph സ്പെൽചെക്കർ"
		else:
			return "Mlmorph Spellchecker"

SpellChecker.IMPLEMENTATION_NAME = "mlmorph.SpellChecker"
SpellChecker.SUPPORTED_SERVICE_NAMES = ("com.sun.star.linguistic2.SpellChecker",)
