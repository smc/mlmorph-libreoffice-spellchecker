import logging
import unohelper
import os
import sys
import locale
import uno
from com.sun.star.beans import XPropertyChangeListener, UnknownPropertyException, PropertyValue
from com.sun.star.linguistic2 import LinguServiceEvent
from com.sun.star.linguistic2.LinguServiceEventFlags import SPELL_CORRECT_WORDS_AGAIN, SPELL_WRONG_WORDS_AGAIN

class PropertyManager(unohelper.Base, XPropertyChangeListener):

	def __init__(self):
		self.__messageLanguage = "en_US"
		logging.debug("PropertyManager.__init__")
		self.__linguPropSet = None
		self.__linguEventListeners = {}
		self.initialize()

	def propertyChange(self, evt):
		logging.debug("PropertyManager.propertyChange")
		self.__setProperties(self.__linguPropSet)
		event = LinguServiceEvent()
		event.nEvent = SPELL_CORRECT_WORDS_AGAIN | SPELL_WRONG_WORDS_AGAIN
		self.__sendLinguEvent(event)

	def __setUiLanguage(self):
		try:
			lang = self.readFromRegistry("org.openoffice.Office.Linguistic/General", "UILocale")
			logging.debug("Specified UI locale = '" + lang + "'")
			if lang is not None and len(lang) > 0:
				self.__messageLanguage = lang
			else:
				# Use system default language
				lang = locale.getdefaultlocale()[0]
				if lang is not None:
					logging.debug("Locale language = '" + lang + "'")
					self.__messageLanguage = lang
		except UnknownPropertyException:
			logging.error("PropertyManager.initialize caught UnknownPropertyException")

	def initialize(self):
		logging.debug("PropertyManager.initialize: starting")
		self.__setUiLanguage()

		compContext = uno.getComponentContext()
		servManager = compContext.ServiceManager
		self.__linguPropSet = servManager.createInstanceWithContext("com.sun.star.linguistic2.LinguProperties", compContext)
		logging.debug("PropertyManager.initialize: property manager initalized")
		# synchronize the local settings from global preferences
		self.__setProperties(self.__linguPropSet)
		# request that all users of linguistic services run the spellchecker
		# again with updated settings
		event = LinguServiceEvent()
		event.nEvent = SPELL_CORRECT_WORDS_AGAIN | SPELL_WRONG_WORDS_AGAIN
		self.__sendLinguEvent(event)

	def addLinguServiceEventListener(self, xLstnr):
		logging.debug("PropertyManager.addLinguServiceEventListener")
		if id(xLstnr) in self.__linguEventListeners:
			return False
		self.__linguEventListeners[id(xLstnr)] = xLstnr
		return True

	def removeLinguServiceEventListener(self, xLstnr):
		logging.debug("PropertyManager.removeLinguServiceEventListener")
		if id(xLstnr) in self.__linguEventListeners:
			del self.__linguEventListeners[id(xLstnr)]
			return True
		return False

	def readFromRegistry(self, group, key):
		rootView = PropertyManager.getRegistryProperties(group)
		if rootView is None:
			logging.error("PropertyManager.readFromRegistry: failed to obtain rootView " + group)
			raise UnknownPropertyException()
		return rootView.getHierarchicalPropertyValue(key)

	def getMessageLanguage(self):
		return self.__messageLanguage

	def reloadVoikkoSettings(self):
		event = LinguServiceEvent()
		event.nEvent = 0
		logging.exception("PropertyManager.reloadVoikkoSettings")
		self.__sendLinguEvent(event)

	def __setProperties(self, properties):
		for p in ["IsSpellWithDigits", "IsSpellUpperCase"]:
			pValue = PropertyValue()
			pValue.Name = p
			pValue.Value = properties.getPropertyValue(p)
			self.setValue(pValue)

	def setValues(self, values):
		for v in values:
			self.setValue(v)

	def resetValues(self, values):
		for v in values:
			globalV = PropertyValue()
			globalV.Name = v.Name
			globalV.Value = self.__linguPropSet.getPropertyValue(v.Name)
			self.setValue(globalV)

	def setValue(self, value):
		logging.exception("PropertyManager.reloadVoikkoSettings" + value.Name)

	def __sendLinguEvent(self, event):
		logging.debug("PropertyManager.sendLinguEvent")
		for key, lstnr in self.__linguEventListeners.items():
			logging.debug("PropertyManager.sendLinguEvent sending event" + key)
			lstnr.processLinguServiceEvent(event)

	def getRegistryProperties(group):
		logging.debug("PropertyManager.getRegistryProperties: " + group)
		compContext = uno.getComponentContext()
		servManager = compContext.ServiceManager
		provider = servManager.createInstanceWithContext("com.sun.star.configuration.ConfigurationProvider", compContext)
		pathArgument = PropertyValue()
		pathArgument.Name = "nodepath"
		pathArgument.Value = group
		aArguments = (pathArgument,)
		rootView = provider.createInstanceWithArguments("com.sun.star.configuration.ConfigurationUpdateAccess", aArguments)
		return rootView

	getRegistryProperties = staticmethod(getRegistryProperties)

	def getInstance():
		if PropertyManager.instance is None:
			PropertyManager.instance = PropertyManager()
		return PropertyManager.instance
	getInstance = staticmethod(getInstance)

PropertyManager.instance = None
PropertyManager.loadingFailed = False
PropertyManager.VOIKKO_OPT_IGNORE_NUMBERS = 1
PropertyManager.VOIKKO_OPT_IGNORE_UPPERCASE = 3
PropertyManager.VOIKKO_OPT_IGNORE_DOT = 0
PropertyManager.VOIKKO_OPT_ACCEPT_TITLES_IN_GC = 13
PropertyManager.VOIKKO_OPT_ACCEPT_BULLETED_LISTS_IN_GC = 16
PropertyManager.VOIKKO_OPT_ACCEPT_UNFINISHED_PARAGRAPHS_IN_GC = 14
