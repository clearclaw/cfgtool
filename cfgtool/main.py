#!/usr/bin/env python

import clip, logging, logtool, sys
from functools import partial
from socket import gethostname
from addict import Dict
from path import path

LOG = logging.getLogger (__name__)

APP = clip.App ()
PROCESS_UTTIME, PROCESS_STRTIME = logtool.now (slug = True)
DEFAULT_CONFIGFILE = "cfgtool.conf"
DEFAULT_BELIEFDIR = "etc/cfgtool/belief.d"
DEFAULT_MODULEDIR = "etc/cfgtool/module.d"
DEFAULT_WORKDIR = "/"
CONFIG = Dict ({
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

class CmdError (Exception):
  pass

@logtool.log_call
def option_setopt (option, value):
  CONFIG[option] = value

@logtool.log_call
def option_logging (flag):
  logging.basicConfig (level = logging.DEBUG)
  CONFIG.debug = flag

@APP.main (name = path (sys.argv[0]).basename (),
           description = "cfgtool",
           tree_view = "-H")
@clip.flag ('-H', '--HELP', hidden = True, help = "Help for all sub-commands")
@clip.flag ("-b", "--nobackup",
            help = "Disable backups of touched files",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "nobackup"))
@clip.flag ("-f", "--force", help = "Don't stop at errors",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "force"))
@clip.opt ("-W", "--workdir",
           help = "Working root directory to use.",
           default = DEFAULT_WORKDIR, hidden = True, inherit_only = True,
           callback = partial (option_setopt, "work_dir"))
@clip.opt ("-M", "--moduledir",
           help = "Module directory to use.",
           default = DEFAULT_WORKDIR + DEFAULT_MODULEDIR, hidden = True,
           inherit_only = True,
           callback = partial (option_setopt, "module__dir"))
@clip.opt ("-B", "--beliefdir",
           help = "Belief directory to use.",
           default = DEFAULT_WORKDIR + DEFAULT_BELIEFDIR, hidden = True,
           inherit_only = True, callback = partial (option_setopt, "belief_dir"))
@clip.flag ("-D", "--debug",
            help = "Enable debug logging",
            default = False, hidden = True, inherit_only = True,
            callback = option_logging)
@clip.flag ("-C", "--nocolour",
            help = "Suppress colours in reports",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "nocolour"))
@clip.flag ("-q", "--quiet",
            help = "Suppress output",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "quiet"))
@clip.flag ("-v", "--verbose",
            help = "Verbose output (see variable mappings)",
            default = False, hidden = True, inherit_only = True,
            callback = partial (option_setopt, "verbose"))
@logtool.log_call
def app_main (*args, **kwargs): # pylint: disable = W0613
  if not sys.stdout.isatty ():
    option_setopt ("nocolour", True)
  CONFIG.work_dir = path (CONFIG.get ("work_dir", DEFAULT_WORKDIR))
  CONFIG.module_dir = path (CONFIG.get ("module_dir",
                                        CONFIG.work_dir / DEFAULT_MODULEDIR))
  CONFIG.belief_dir = path (CONFIG.get ("belief_dir",
                                        CONFIG.work_dir / DEFAULT_BELIEFDIR))

@logtool.log_call
def main ():
  try:
    APP.run ()
  except clip.ClipExit as e:
    sys.exit (1 if e.status else 0)
  except (CmdError, KeyboardInterrupt):
    sys.exit (2)
  except Exception as e:
    logtool.log_fault (e)
    sys.exit (3)

if __name__ == "__main__":
  main()
