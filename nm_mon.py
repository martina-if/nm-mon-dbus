import sys
import traceback
import gobject
import dbus
import dbus.mainloop.glib

def handle_signal(*args, **kwargs):
  print "=== New signal ============"
  print "Len: ", len(args)

  for arg in args:
    print "Len dict: ", len(arg)
    for k in arg:
      print k, ":: ", arg[k]


  return
  for arg in args:
    print arg
    if isinstance(arg, dbus.Dictionary):
      for key in arg:
        if key != "ActiveConnections":
          continue
        val = arg[key]
        print type(val)
        #print dir(val)
        print key, "::: ",
        for e in val:
          print e,
        print
        #check_connections(val)
        #print val
    else:
      print arg

def check_connections(connections):
  # Get active connection state
  manager_prop_iface = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
  active = manager_prop_iface.Get("org.freedesktop.NetworkManager", "ActiveConnections")
  for c in active:
    print "Connection: ", c
    ac_proxy = bus.get_object("org.freedesktop.NetworkManager", c)
    prop_iface = dbus.Interface(ac_proxy, "org.freedesktop.DBus.Properties")
    state = prop_iface.Get("org.freedesktop.NetworkManager.Connection.Active", "State")

    # Connections in NM are a collection of settings that describe everything
    # needed to connect to a specific network.  Lets get those details so we
    # can find the user-readable name of the connection.
    con_path = prop_iface.Get("org.freedesktop.NetworkManager.Connection.Active", "Connection")
    service_proxy = bus.get_object("org.freedesktop.NetworkManager", con_path)
    con_iface = dbus.Interface(service_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
    con_details = con_iface.GetSettings()
    con_name = con_details['connection']['id']

    if state == 2:   # activated
      print "Connection '%s' is activated" % con_name
    else:
      print "Connection '%s' is activating" % con_name


if __name__ == '__main__':
  dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

  bus = dbus.SystemBus()
  #try:
    #object  = bus.get_object("org.freedesktop.NetworkManager","/org/freedesktop/NetworkManager")
    #object.connect_to_signal("HelloSignal", hello_signal_handler, dbus_interface="com.example.TestService", arg0="Hello")
  #except dbus.DBusException:
    #traceback.print_exc()
    #sys.exit(1)

  bus.add_signal_receiver(handle_signal, dbus_interface = "org.freedesktop.NetworkManager")
  #bus.add_signal_receiver(handle_signal, dbus_interface="org.freedesktop.NetworkManager", signal_name="PropertiesChanged")
  #bus.add_signal_receiver(handle_signal, dbus_interface="org.freedesktop.NetworkManager", message_keyword="ActiveConnections")

  loop = gobject.MainLoop()
  loop.run()

