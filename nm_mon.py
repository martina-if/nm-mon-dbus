import sys
from xcb import Xserver,XError
import logging as log
import gobject
import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

# Copied from include/NetworkManager.h
nm_states = {
   0: "Unknown",
  10: "Asleep",
  20: "Disconnected",
  30: "Disconnecting",
  40: "Connecting",
  50: "Connected local",
  60: "Connected site",
  70: "Connected global",
}

connection_states = {
  0: "Unknown",
  1: "Activating",
  2: "Activated",
  3: "Deactivated",
}

class NetMonitor(object):

  def __init__(self):
    # Set up the bus
    self.bus = dbus.SystemBus()
    self.bus.add_signal_receiver(self.signal_handler, dbus_interface = "org.freedesktop.NetworkManager")
    # Set up the main proxy and interface for network manager properties
    nm_proxy = self.bus.get_object("org.freedesktop.NetworkManager", "/org/freedesktop/NetworkManager")
    self.nm_iface = dbus.Interface(nm_proxy, "org.freedesktop.DBus.Properties")

    # X client
    try:
      self.xserver = Xserver()
      self.xserver.connect()
      self.xserver.set_screen()
    except XError as e:
      log.error(e)

  def signal_handler(self, *args, **kwargs):
    arg = args[0] # Only first field of the tuple has info
    if type(arg) == dbus.Dictionary:
      for k in arg:
        if k == "State":
          self.state_changed(arg[k])

  def state_changed(self, state):
    log.debug("State changed: "+ nm_states[state])
    self.check_connections()

  def check_connections(self):
    # Get the list of active connections
    active = self.nm_iface.Get("org.freedesktop.NetworkManager", "ActiveConnections")

    for c in active:
      # Get the state of this active connection
      active_con_proxy = self.bus.get_object("org.freedesktop.NetworkManager", c)
      properties_iface = dbus.Interface(active_con_proxy, "org.freedesktop.DBus.Properties")
      state = properties_iface.Get("org.freedesktop.NetworkManager.Connection.Active", "State")

      # Connections in NM are a collection of settings that describe everything
      # needed to connect to a specific network.  Lets get those details so we
      # can find the user-readable name of the connection.
      connection_path = properties_iface.Get("org.freedesktop.NetworkManager.Connection.Active", "Connection")
      service_proxy = self.bus.get_object("org.freedesktop.NetworkManager", connection_path)
      connection_iface = dbus.Interface(service_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
      connection_details = connection_iface.GetSettings()
      connection_name = connection_details['connection']['id']
      connection_status = connection_states[state]

      log.debug("Connection '%s' is %s" % (connection_name, connection_status))

      # Set wm name with the name of the connection when it activates
      try:
        if connection_status == "Activated":
          self.xserver.set_wm_name(str(connection_name))
      except XError as e:
        print e


if __name__ == '__main__':

  netmon = NetMonitor()
  loop = gobject.MainLoop()
  loop.run()

