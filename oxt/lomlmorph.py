import os
import uno
import sys
import logging
import unohelper
from com.sun.star.awt.MessageBoxType import ERRORBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
from SpellChecker import SpellChecker

if "MLMORPH_DEBUG" in os.environ:
    logging.getLogger().setLevel(logging.DEBUG)


def messageBox(messageText):
    ctx = uno.getComponentContext()
    sManager = ctx.ServiceManager
    toolkit = sManager.createInstance("com.sun.star.awt.Toolkit")
    msgbox = toolkit.createMessageBox(
        None, ERRORBOX, BUTTONS_OK, "Error initializing mlmorph", messageText)
    return msgbox.execute()


try:
                # name of g_ImplementationHelper is significant, Python component loader expects to find it
    g_ImplementationHelper = unohelper.ImplementationHelper()
    g_ImplementationHelper.addImplementation(SpellChecker,
                                             SpellChecker.IMPLEMENTATION_NAME,
                                             SpellChecker.SUPPORTED_SERVICE_NAMES,)
except OSError as e:
    messageBox("OSError: {0}".format(e))
except AttributeError as e:
    messageBox("AttributeError: {0}".format(e))
except:
    messageBox(str(sys.exc_info()[0]))
