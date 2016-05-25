from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *

from ycmd.completers.completer import Completer
from ycmd import responses
from ycmd import utils

import subprocess
import re
import logging

_logger = logging.getLogger(__name__)

def log(level, msg):
    _logger.log(level, '[jrnlcompl] %s' % msg)

def error(msg):
    log(logging.ERROR, msg)

def warning(msg):
    log(logging.WARNING, msg)

def info(msg):
    log(logging.INFO, msg)

def debug(msg):
    log(logging.DEBUG, msg)

class JrnlTagsCompleter( Completer ):
    """
    General completer that provides Jrnl tag names in completions.
    """

    def __init__( self, user_options ):
        super ( JrnlTagsCompleter, self ).__init__( user_options )
        self._trigger = [ '@' ]

        info('Jrnl Tags Completer loaded')

    def SupportedFiletypes( self ):
        return [ 'text' ]

    def ShouldUseNowInner( self, request_data ):
        current_line = request_data[ 'line_value' ]
        start_codepoint = request_data[ 'start_codepoint' ]
        trigger_codepoint = start_codepoint - 1

        info('Jrnl shoud be used ?')
        return (
                trigger_codepoint > 0 and
                ( current_line [ trigger_codepoint - 1 ] in self._trigger ) )


        return self.CursorIsOnAtKey( request_data )

    def ComputeCandidatesInner(self, request_data ):
        jrnl_out = subprocess.check_output("jrnl --tags", shell=True)
        candidates = re.findall("@\w+", jrnl_out.decode('utf-8'))
        info('candidates computed')

        completion_dicts = []
        for c in candidates:
            completion_dicts.append( responses.BuildCompletionData(c[1:], "", "", c, "", "" ) )

        return completion_dicts
