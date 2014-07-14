from ctypes import *
import logging as log
#lib = cdll.LoadLibrary('./wm_name.so')
#lib = CDLL('./libwselfmname.so', mode=RTLD_GLOBAL)


#lib.connect_x()

class Xserver(object):
  def __init__(self):
    self.xlib = CDLL('./libwmname.so', mode=RTLD_GLOBAL)

  def connect(self):
    log.debug("Connecting")
    self.connection = self.xlib.connect_x()
    if self.connection == 0:
      raise XError("Error while trying to connect")

  def disconnect(self):
    log.debug("Disconnecting")
    res = self.xlib.disconnect_x(self.connection)
    if res != 0:
      raise XError("Error trying to disconnect")

  def set_screen(self):
    res = self.xlib.set_screen(self.connection)
    if res != 0:
      raise XError("Error trying to set screen")

  def set_wm_name(self, text):
    log.debug("Setting name: "+ text)
    res = self.xlib.set_wm_name(self.connection, text)
    if res != 0:
      raise XError("Error trying to set name: " + res)

class XError(Exception):
  def __init__(self, msg):
    self.msg = "Xerror: " + msg

  def __str__(self):
    return repr(self.msg)

if __name__ == '__main__':
  x = Xserver()
  x.connect()
  x.set_screen()
  x.set_wm_name("HOLA\0")
  x.disconnect()
