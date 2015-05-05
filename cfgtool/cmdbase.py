#!/usr/bin/env python

import clip, importlib, itertools, json, logging, logtool, os, re, socket, subprocess, sys, termcolor
from socket import gethostname
from addict import Dict
from path import path
from cfgtool.main import CONFIG
from cfgtool.cmdio import CmdIO

LOG = logging.getLogger (__name__)
VARIABLE_REGEX = r"\$\{([A-Za-z0-9._]+)\}"
ESCAPED_REGEX = r"\$\{\{([A-Za-z0-9._]+)\}\}"
COLOUR_ERROR = "red"
COLOUR_INFO = "white"
COLOUR_INFO_BAD = "magenta"
COLOUR_WARN = "yellow"
COLOUR_REPORT = "green"
COLOUR_FIELDNAME = "cyan"
COLOUR_VALUE = "green"

@logtool.log_call
def implementation (this, **kwargs):
  cmd = importlib.import_module ("cfgtool.cmd_%s" % this)
  item = getattr (cmd, "Action")
  item (kwargs).run ()

class CmdBase (CmdIO):

  @logtool.log_call
  def __init__ (self, kwargs):
    super (CmdBase, self).__init__ (kwargs)
    self.re_var = re.compile (VARIABLE_REGEX)
    self.re_escvar = re.compile (ESCAPED_REGEX)
    self.conf = CONFIG
    self.belief = {}
    self.cfgfiles = []
    self.load_beliefs ()
    self.load_cfglist ()

    self.topo_list = []
    self.topo = Dict ()
    self.cfgs = []
    self.load_topos ()
    self.load_cfgs ()
    self.validate ()

  @logtool.log_call
  def load_beliefs (self):
    beliefs = [f for f in self.conf.cfgtool_dir.glob (self.conf.belief_ext)]
      for fname in sorted (beliefs):
        try:
          self.belief.update (json.loads (file (fname).read ()))
        except Exception as e:
          logtool.log_fault (e)
          self.error ("Error loading belief: %s -- %s" % (fname, e))
          raise ValueErrr
    self.belief.update ({
      "LOCAL_HOSTNAME": self.get_localhostname (),
      "LOCAL_STRTIME": self.conf.time_str,
      "LOCAL_UTTIME": self.conf.time_ut,
    })

  @logtool.log_call
  def template_check (self, e):
    if e[0] = "/":
      e = e[1:]
    entry = self.work_dir / e
    fname = path ("%s.%s" % (entry, self.conf.templ_ext))
    if not fname.is_file ():
      self.error ("Template missing: %s" % fname)
      entry = None
    return entry

  @logtool.log_call
  def load_cfglist (self):
    fname = self.conf.modules_dir / self.module
    files = [f.strip () for f in fname.lines () if f.strip ()[0] != "#"]
    flist = map (template_check, files)
    if None in flist:
      raise ValueError
    self.cfgfiles = [f in flist if f is not None]

  @logtool.log_call
  def get_localhostname (self):
    return socket.gethostname ().split (".")[0]

  @logtool.log_call
  def get_belief (longkey):
    keylist = longkey.split (".")
    rc = reduce (lambda d, k: d[k], keylist, self.belief)
    if rc == {}:
      raise ValueError
    return rc

  @logtool.log_call
  def instantiate_file (self, in_file, out_file):
    err = 0
    with file (in_file) as file_in:
      with open (out_file, "w") as file_out:
        for line in file_in:
          for pattern, re_pat in [("%s$(%s)%s", self.re_var),
                                  ("%s${%s}%s", self.re_escvar)]:
            while True:
              m = re_pat.search (line)
              if not m:
                break
              # t = m.group (0) # Entire match
              k = m.group (1) # Variable name
              try:
                v = self.get_value (k) # Replacement token
                self.report ("Mapped: ${%s} -> %s" % (k, v))
              except ValueError:
                v = k
                err += 1
                self.error ("Can't find value for: ${%s}" % k)
              line = pattern % (line[:m.start(0)], v, line[m.end(0):])
          out_file.write (line)
    return err

  @logtool.log_call
  def make_file (self, in_file, out_file):
    self.report ("File: %s" % in_file)
    if self.conf.backup and out_file.is_file ():
      out_file.rename ("%s-backup.%s" % (out_file, self.conf.time_str))
    else:
      out_file.remove_p ()
    rc = self.instantiate_file (in_file, out_file)
    if rc:
      self.error ("Failed.  Some variables were not defined.")
    return rc

  @logtool.log_call
  def compare_files (self, file1, file2):
    cmd = "diff -q %s %s > /dev/null" % (file1, file2)
    self.info ("\t%s" % cmd)
    rc = 0
    try:
      rc = subprocess.call (cmd, shell = True)
      if rc < 0:
        self.error ("Compare terminated by signal: %s" % (-rc))
    except OSError, e:
      self.error ("Compare catastrophically failed: %s" % e)
    return rc

  @logtool.log_call
  def process_cfgs (self, cfg_ext, out_ext, func):
    err = 0
    self.report ("Module: %s" % self.module)
    for cfg in self.cfgfiles:
      in_file = cfg + cfg_ext
      out_file = cfg + out_ext
      rc = func (in_file, out_file)
      if rc:
        err += 1
        self.error ("Error in processing: %s" % in_file)
    if err:
      self.error ("%d files failed to process." % err)
    return err
