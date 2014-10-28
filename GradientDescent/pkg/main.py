'''
Created on Oct 22, 2014

@author: alejandro
'''

from gi.repository import Gtk

import ui

if __name__ == '__main__':
    win = ui.MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    
    