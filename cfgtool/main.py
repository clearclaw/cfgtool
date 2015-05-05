#!/usr/bin/env python

import clip, logging, logtool, sys
from functools import partial
from socket import gethostname
from addict import Dict
from path import path
from configobj import ConfigObj

LOG = logging.getLogger (__name__)

APP = clip.App ()
PROCESS_UTTIME, PROCESS_STRTIME = logtool.now (slug = True)
CONFIG = Dict ({
  "cfgtool_dir": path (DEFAULT_CFGTOOLDIR),
  "debug": False,
  "templ_ext": ".templ",
  "belief_ext": ".json",
  "backup_ext": ".backup",
  "check_ext": ".check",
  "out_ext": "",
  "sample_ext": ".sample",
  "time_ut": PROCESS_UTTIME,
  "time_str": PROCESS_STRTIME,
})
DEFAULT_CFGTOOLDIR = path ("/etc/cfgtool")
DEFAULT_CONFIGFILE = "cfgtool.conf"
DEFAULT_BELIEFDIR = DEFAULT_CFGTOOLDIR / "belief.d"
DEFAULT_BELIEFEXT = ".belief"
DEFAULT_MODDIR = DEFAULT_CFGTOOLDIR / "modules.d"
DEFAULT_MODEXT = ".cfgs"
DEFAULT_WORKDIR = "/"

@logtool.log_call
def option_setopt (option, value):
  CONFIG[option] = value

@logtool.log_call
def option_module (value):
  CONFIG.module = value
  CONFIG.cfgs_file = CONFIG.modules_dir / "%s.cfgs" % value

@logtool.log_call
def option_logging (flag):
  logging.basicConfig (level = logging.DEBUG)
  CONFIG.debug = flag

@APP.main (name = path (sys.argv[0]).basename (),
           description = "cfgtool",
           tree_view = "-H")
@clip.flag ('-H', '--HELP', hidden = True, help = "Help for all sub-commands")
@clip.opt ("-c", "--cfgtooldir", name = "ct_dir",
           help =  "Cfgtool directory root to use.",
           default = DEFAULT_CFGTOOLDIR, hidden = True, inherit_only = True,
           callback = partial (option_setopt, "cfgtool_dir"))
@clip.opt ("-w", "--workdir", name = "work_dir",
           help = "Working root directory to use.",
           default = DEFAULT_WORKDIR, hidden = True, inherit_only = True,
           callback = partial (option_setopt, "work_dir"))
@clip.opt ("-m", "--module", name = "module",
           help = "Module to localise for (required)",
           hidden = True, inherit_only = True, callback = option_module)
@clip.opt ("-t", "--target", name = "target",
           help = "Target host(name) to localise for",
           default = gethostname (), hidden = True, inherit_only = True,
           callback = partial (option_setopt, "target"))
@clip.flag ("-b", "--nobackup", name = "nobackup",
            help = "Disable backups of touched files",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "nobackup"))
@clip.flag ("-D", "--debug", name = "debug", help = "Enable debug logging",
            default = False, hidden = True, inherit_only = True,
            callback = option_logging)
@clip.flag ("-f", "--force", name = "force", help = "Don't stop at errors",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "force"))
@clip.flag ("-C", "--nocolour", name = "nocolour",
            help = "Suppress colours in reports",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "nocolour"))
@clip.flag ("-q", "--quiet", name = "quiet", help = "Suppress output",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "quiet"))
@logtool.log_call
def app_main (*args, **kwargs): # pylint: disable = W0613
  if not sys.stdout.isatty ():
    option_setopt ("nocolour", True)

@logtool.log_call
def main ():
  try:
    conf = ConfigObj (self.conf.cfgtool_dir / DEFAULT_CONFIGFILE,
                      interpolation = False)
  except: # pylint: disable = W0702
    conf = {}
  CONFIG.modules_dir = path (conf.get ("modules_dir", DEFAULT_MODULEDIR))
  CONFIG.belief_dir = path (conf.get ("belief_dir", DEFAULT_BELIEFDIR))
  CONFIG.work_dir = path (conf.get ("work_dir", DEFAULT_WORKDIR))
  try:
    APP.run ()
  except KeyboardInterrupt:
    pass
  except clip.ClipExit:
    pass
  except Exception as e:
    logtool.log_fault (e)

if __name__ == "__main__":
  main()
