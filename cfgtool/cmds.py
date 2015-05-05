#! /usr/bin/env python

import clip, logging, logtool
from cfgtool.main import app_main, CONFIG
from cfgtool.cmdbase import implementation

LOG = logging.getLogger (__name__)

@app_main.subcommand (
  name = "check",
  description = "Check currency of configuration files")
@logtool.log_call
def check ():
  implementation ("check", CONFIG)

@app_main.subcommand (
  name = "clean",
  description = "Remove old backups")
@logtool.log_call
def clean ():
  implementation ("clean", CONFIG)

@app_main.subcommand (
  name = "sample",
  description = "Generate sample configuration files")
@logtool.log_call
def sample ():
  implementation ("sample", CONFIG)

@app_main.subcommand (
  name = "status",
  description = "Report status of configuration files")
@logtool.log_call
def status ():
  implementation ("status", CONFIG)

@app_main.subcommand (
  name = "write",
  description = "Write new configuration files (requires --force)")
@logtool.log_call
def write ():
  implementation ("write", CONFIG)
