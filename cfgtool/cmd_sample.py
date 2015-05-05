#!/usr/bin/env python

import clip, logging, logtool
from cfgtool.cmdbase import CmdBase

LOG = logging.getLogger (__name__)

class Action (CmdBase):

  @logtool.log_call
  def run (self):
    rc = process_cfgs (self.conf.templ_ext, self.conf.sample_ext,
                       self.make_file)
    if rc:
      self.err ("%d errors" % err)
    clip.exit (err = (True if rc else False))
