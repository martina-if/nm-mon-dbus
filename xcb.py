from ctypes import *
#lib = cdll.LoadLibrary('./wm_name.so')
#lib = CDLL('./libwselfmname.so', mode=RTLD_GLOBAL)


#lib.connect_x()

class Xserver(object):
  def __init__(self):
    self.xlib = CDLL('./libwmname.so', mode=RTLD_GLOBAL)

  def connect(self):
    print "Connecting"
    self.connection = self.xlib.connect_x()
    if self.connection == 0:
      print "Error while trying to connect"

  def disconnect(self):
    print "Disconnecting"
    res = self.xlib.disconnect_x(self.connection)
    if res != 0:
      print "Error trying to disconnect"

  def set_screen(self):
    res = self.xlib.set_screen(self.connection)
    if res != 0:
      print "Error trying to set screen"

  def set_wm_name(self, text):
    print "Setting name"
    res = self.xlib.set_wm_name(self.connection, text)
    if res != 0:
      print "Error trying to set name: ", res

  def myprint(self, text):
    print "Trying to print..."
    self.xlib.myprint(text)


if __name__ == '__main__':
  x = Xserver()
  x.connect()
  x.set_screen()
  x.set_wm_name("HOLA\0")
  x.myprint("hey")
  x.disconnect()
