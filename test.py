from gi.repository import Gtk
builder=Gtk.Builder()
builder.add_from_file("example.glade")
 #we don't really have two buttons here, this is just an example
builder.add_objects_from_file("example.glade", ("button1", "button2"))