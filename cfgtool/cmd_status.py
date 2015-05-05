#!/usr/bin/env python

import clip, logging, logtool
from cfgtool.cmdbase import CmdBase

LOG = logging.getLogger (__name__)

class Action (CmdBase):

  @logtool.log_call
  def run (self):
    for fname in self.cfgs:
      for f in fname.dirname ().glob ("%s.%s*" % (fname.basename (), ext)):
        f.remove ()
