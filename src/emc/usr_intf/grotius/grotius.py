#!/usr/bin/env python

import sys, os
BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
libdir = os.path.join(BASE, "lib", "python")
datadir = os.path.join(BASE, "share", "linuxcnc")
imagedir = os.path.join(BASE, "share", "linuxcnc")
sys.path.insert(0, libdir)
xmlname = os.path.join(datadir,"grotius.glade")


import sys
import math 
import pygtk
pygtk.require("2.0")
import gtk
import linuxcnc, hal
import gremlin
import gladevcp.makepins
import gobject
import hal, time
from gmoccapy import widgets 


try:
    # path to TCL for external programs only needed for halshow button
    TCLPATH = os.environ['LINUXCNC_TCL_DIR']
except:
    pass

try:
    CONFIGPATH = os.environ['CONFIG_DIR']
except:
    pass

class grotius_gui(object):

  def __init__(self, inifile):

    self.builder = gtk.Builder()
    self.builder.add_from_file(xmlname)
    self.builder.connect_signals(self)
    self.version = os.environ['LINUXCNCVERSION']
    self.ini_file_path = os.environ['INI_FILE_NAME']
    self.ini_file_object = linuxcnc.ini(self.ini_file_path)
    self.machine_name = self.ini_file_object.find('EMC', 'MACHINE')
    self.cnc = linuxcnc
    self.widgets = widgets.Widgets(self.builder)
    self.c = linuxcnc.command()
    self.s = linuxcnc.stat()
    self.error = linuxcnc.error_channel()
    self.halcomp = hal.component("grotius_gui")
    self.panel = gladevcp.makepins.GladePanel(self.halcomp, xmlname, self.builder, None)
    self.halcomp.ready()
    self.window = self.builder.get_object('main_window')
    self.window.set_title(self.machine_name + ' Version ' + self.version)
    
    self.window.show_all()
    gobject.timeout_add(100, self.periodic)

    self.widgets.adaptive_feed.set_property("min", -1)
    self.widgets.adaptive_feed.set_property("max", 1)

    self.widgets.gremlin.current_view = 'p'
    self.widgets.gremlin.set_current_view() 
    self.widgets.gremlin.show_extents_option = False

    self.widgets.manual_tab.set_sensitive(False)  
    self.widgets.user_tab_box.set_sensitive(False)  
    
  #initialise program speed widget value at startup...
    x = self.widgets.program_speed.get_value()
    self.widgets.program_speed.set_value(x+0) 
    self.c.maxvel(self.widgets.program_speed.get_value()/60)

    self.widgets.jog_speed.get_value()

    self.settings = gtk.settings_get_default()
    self.settings.set_property("gtk-theme-name", "Adwaita-dark")

  def on_adaptive_feed_value_changed(self, widget, data=None):
    self.o['adaptive-feed'] = self.widgets.adaptive_feed.get_value()
    x = self.widgets.adaptive_feed.get_value()
    self.widgets.adaptive_feed.set_value(x+0)

  def on_torch_on_pressed(self, widget, data=None):
    print " torch on "
    #self.c.spindle( 1, self.widgets.power.get_value())
    self.c.spindle( 1, 1 ) 

  def on_torch_off_pressed(self, widget, data=None):
    print " torch off "
    self.c.spindle( 1, 0 ) 
 
  def on_emergency_stop_pressed(self, widget, data=None):
    self.c.abort()
    self.c.state(self.cnc.STATE_ESTOP_RESET) 
    self.c.state(self.cnc.STATE_ON)   
    self.widgets.manual_tab.set_sensitive(True)
    self.widgets.user_tab_box.set_sensitive(True) 

  def on_start_pressed(self, widget, data=None):
    self.widgets.manual_tab.set_sensitive(False)

    self.c.mode(self.cnc.MODE_AUTO)
    self.c.wait_complete()  
    
    command = int(self.widgets.start_entry.get_text())  
    self.c.auto(self.cnc.AUTO_RUN, command)

  def on_step_pressed(self, widget, data=None):
    self.c.auto(self.cnc.AUTO_STEP)
    print " step "

  def on_pause_pressed(self, widget, data=None):
    self.c.auto(self.cnc.AUTO_PAUSE)
    print " pauze "

  def on_resume_pressed(self, widget, data=None):
    self.c.auto(self.cnc.AUTO_RESUME)
    print " resume "

  def on_stop_pressed(self, widget, data=None):   
    self.c.abort()
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete() 
    self.widgets.manual_tab.set_sensitive(True)
    self.widgets.user_tab_box.set_sensitive(True)
    print " stop "

  def periodic(self): 
    return True 

  def on_halshow_pressed(self, widget, data=None):  
    print " halshow "
    p = os.popen( "tclsh %s/bin/halshow.tcl &" % TCLPATH )

# ======================================================================= 
  def on_x_plus_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete()  
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 0, (self.widgets.jog_speed.get_value()/60))  #linuxcnc joint update version
    print " x plus " 
 
  def on_x_plus_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 0)  #linuxcnc joint update version
    print " x stop "
    
  def on_x_min_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete()
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 0, -(self.widgets.jog_speed.get_value()/60))
    print " x min " 
 
  def on_x_min_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 0)
    print " x stop "
# =======================================================================    
  def on_y_plus_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete() 
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 1, (self.widgets.jog_speed.get_value()/60))
    print " y plus "
       
  def on_y_plus_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 1)
    print " y stop "
    
  def on_y_min_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete() 
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 1, -(self.widgets.jog_speed.get_value()/60))
    print " y min "  
    
  def on_y_min_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 1)
    print " y stop "
# =======================================================================    
  def on_z_plus_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete() 
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 2, (self.widgets.jog_speed.get_value()/60))
    print " z plus "
       
  def on_z_plus_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 2)
    print " z stop "
    
  def on_z_min_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete()  
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 2, -(self.widgets.jog_speed.get_value()/60))
    print " z min " 
    
  def on_z_min_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 2)
    print " z stop "
# =======================================================================  
  def on_a_plus_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete() 
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 3, (self.widgets.jog_speed.get_value()/60))
    print " a plus "
  
  def on_a_plus_released(self, widget, data=None): 
    self.c.jog(linuxcnc.JOG_STOP, 0, 3)
    print " a stop "
 
  def on_a_min_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete() 
    self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 3, -(self.widgets.jog_speed.get_value()/60))
    print " a min "   
   
  def on_a_min_released(self, widget, data=None): 
    print " a stop "
    self.c.jog(linuxcnc.JOG_STOP, 0, 3)
# =======================================================================  
  def on_b_plus_pressed(self, widget, data=None): 
    #self.c.mode(self.cnc.MODE_MANUAL)
    #self.c.wait_complete() 
    #self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 4, (self.widgets.jog_speed.get_value()/60))
    print " b plus " 
 
  def on_b_plus_released(self, widget, data=None): 
    #self.c.jog(linuxcnc.JOG_STOP, 0, 4)
    print " b stop "

  def on_b_min_pressed(self, widget, data=None): 
    #self.c.mode(self.cnc.MODE_MANUAL)
    #self.c.wait_complete() 
    #self.c.jog(linuxcnc.JOG_CONTINUOUS, 0, 4, -(self.widgets.jog_speed.get_value()/60))
    print " b min not "  
 
  def on_b_min_released(self, widget, data=None): 
    #print " b stop "
    #self.c.jog(linuxcnc.JOG_STOP, 0, 4)
    print " b stop not"
# =======================================================================  

  def on_set_pos_x_pressed(self, widget, data=None):
    self.entry1 = self.widgets.entry_x
    self.x = float(self.entry1.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G10 L20 P0 X{0}".format(self.x)              
    self.c.mdi(command)
    print " x position set "  
    
  def on_set_pos_y_pressed(self, widget, data=None):
    self.entry2 = self.widgets.entry_y
    self.y = float(self.entry2.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G10 L20 P1 Y{0}".format(self.y)              
    self.c.mdi(command)
    print " y position set "   
    
  def on_set_pos_z_pressed(self, widget, data=None):
    self.entry3 = self.widgets.entry_z
    self.z = float(self.entry3.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G10 L20 P1 Z{0}".format(self.z)              
    self.c.mdi(command)
    print " z position set " 
    
  def on_set_pos_a_pressed(self, widget, data=None):
    self.entry4 = self.widgets.entry_a
    self.a = float(self.entry4.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G10 L20 P1 A{0}".format(self.a)              
    self.c.mdi(command)
    print " a position set "
    
  def on_set_pos_b_pressed(self, widget, data=None):
    #self.entry5 = self.widgets.entry_b
    #self.b = float(self.entry5.get_text())
    #self.c.mode(self.cnc.MODE_MDI)
    #self.c.wait_complete()
    #command = "G10 L20 P1 B{0}".format(self.b)              
    #self.c.mdi(command)
    print " b position set " 
    
  def on_set_pos_all_pressed(self, widget, data=None):
    self.entry1 = self.widgets.entry_x
    self.entry2 = self.widgets.entry_y
    self.entry3 = self.widgets.entry_z
    self.entry4 = self.widgets.entry_a
        
    self.x = float(self.entry1.get_text())
    self.y = float(self.entry2.get_text())
    self.z = float(self.entry3.get_text())
    self.a = float(self.entry4.get_text())
        
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    #this is a tuple example, see http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch13s03.html
    command = "G10 L20 P1 X{0}".format(self.x) + "Y{0}".format(self.y) + "Z{0}".format(self.z) + "A{0}".format(self.a)            
    self.c.mdi(command)

    self.widgets.gremlin.clear_live_plotter() 

    print " all position set " 
    
  def on_zero_all_pressed(self, widget, data=None):
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    #this is a tuple example, see http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch13s03.html
    command = "G10 L20 P1 X0 Y0 Z0 A0"        
    self.c.mdi(command)

    self.widgets.entry_x.set_text("0")
    self.widgets.entry_y.set_text("0")
    self.widgets.entry_z.set_text("0")
    self.widgets.entry_a.set_text("0")

    self.c.mode(self.cnc.MODE_MANUAL)
    self.c.wait_complete()

    self.widgets.gremlin.reloadfile(None)
    self.widgets.gremlin.clear_live_plotter() 
    print " Zero all " 

  def on_goto_pos_x_pressed(self, widget, data=None):
    self.entry1 = self.widgets.entry_x
    self.x = float(self.entry1.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G01 X{0}".format(self.x) + "F{0}".format(self.widgets.jog_speed.get_value())              
    self.c.mdi(command)
    print " goto x position "  
    
  def on_goto_pos_y_pressed(self, widget, data=None):
    self.entry2 = self.widgets.entry_y
    self.y = float(self.entry2.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G01 Y{0}".format(self.y) + "F{0}".format(self.widgets.jog_speed.get_value())              
    self.c.mdi(command)
    print " goto y position "  
    
  def on_goto_pos_z_pressed(self, widget, data=None):
    self.entry3 = self.widgets.entry_z
    self.z = float(self.entry3.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G01 Z{0}".format(self.z) + "F{0}".format(self.widgets.jog_speed.get_value())              
    self.c.mdi(command)
    print " goto z position "  
    
  def on_goto_pos_a_pressed(self, widget, data=None):
    self.entry4 = self.widgets.entry_a
    self.a = float(self.entry4.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G01 A{0}".format(self.a) + "F{0}".format(self.widgets.jog_speed.get_value())              
    self.c.mdi(command)
    print " goto a position "  
    
  def on_goto_pos_b_pressed(self, widget, data=None):
    self.entry5 = self.widgets.entry_b
    self.b = float(self.entry5.get_text())
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G01 B{0}".format(self.b) + "F{0}".format(self.widgets.jog_speed.get_value())              
    self.c.mdi(command)
    print " goto b position "  
    
  def on_goto_pos_all_pressed(self, widget, data=None):
    self.entry1 = self.widgets.entry_x
    self.entry2 = self.widgets.entry_y
    self.entry3 = self.widgets.entry_z
    self.entry4 = self.widgets.entry_a
    self.entry5 = self.widgets.entry_b
        
    self.x = float(self.entry1.get_text())
    self.y = float(self.entry2.get_text())
    self.z = float(self.entry3.get_text())
    self.a = float(self.entry4.get_text())
    self.b = float(self.entry5.get_text())
       
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    #this is a tuple example, see http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch13s03.html
    command = "G01 X{0}".format(self.x) + "Y{0}".format(self.y) + "Z{0}".format(self.z) + "A{0}".format(self.a) + "B{0}".format(self.b) + "F{0}".format(self.widgets.jog_speed.get_value())           
    self.c.mdi(command)
    print " goto all position "  
    
  def on_goto_zero_pressed(self, widget, data=None): 
    self.c.mode(self.cnc.MODE_MDI)
    self.c.wait_complete()
    command = "G01 X0 Y0 Z0 A0" + "F{0}".format(self.widgets.jog_speed.get_value())              
    self.c.mdi(command)
    print " goto zero " 
    
# ======================================================================= 
 
  def on_home_all_pressed(self, widget, data=None):
    self.s.poll()
    if not self.s.estop and self.s.enabled and self.cnc.MODE_MANUAL:
       self.c.mode(self.cnc.MODE_MANUAL)
       self.c.wait_complete()

       # 1:teleop, 0: joint
       self.c.teleop_enable(0)
       self.c.wait_complete()

       #self.c.home(0) 
       #self.c.wait_complete()
       #self.c.home(2) 
       #self.c.wait_complete()
       #self.c.home(3) 
       #self.c.wait_complete()
       #self.c.home(4)   
       #self.c.wait_complete()
       self.c.home(-1) 

       self.widgets.gremlin.clear_live_plotter()  
       print " home all "
          

    if self.s.estop and not self.s.enabled:
       print " can not home all, machine in E-stop or not enabled "
    
    #if self.s.homed:
       


  def on_jog_speed_value_changed(self, widget, data=None):
    x = self.widgets.jog_speed.get_value()
    self.widgets.jog_speed.set_value(x+0)

  def on_program_speed_value_changed(self, widget, data=None):
    x = self.widgets.program_speed.get_value()
    self.widgets.program_speed.set_value(x+0) 
    self.c.maxvel(self.widgets.program_speed.get_value()/60)
   
  def on_edit_gcode_pressed(self, widget, data=None): 
    self.widgets.vcp_sourceview.set_sensitive(True)
    self.widgets.vcp_sourceview.grab_focus()
    print " edit g-code "
    
  def on_clear_mdi_pressed(self, widget, data=None):  
    #self.widgets.vcp_mdihistory.model.clear()  
    self.widgets.vcp_mdihistory.model.clear()      
    print " clear mdi "
    
  def on_zoom_in_pressed(self, widget, data=None):
    self.widgets.gremlin.zoom_in()
    print " zoom in "    
    
  def on_zoom_out_pressed(self, widget, data=None): 
    self.widgets.gremlin.zoom_out()
    print " zoom out "  
    
  def on_view_3d_pressed(self, widget, data=None): 
    self.widgets.gremlin.current_view = 'p'
    self.widgets.gremlin.set_current_view()  
    print " view 3d "   
    
  def on_top_view_pressed(self, widget, data=None): 
    self.widgets.gremlin.current_view = 'z'
    self.widgets.gremlin.set_current_view()   
    print " view top "

  def on_view_side_pressed(self, widget, data=None): 
    self.widgets.gremlin.current_view = 'x'
    self.widgets.gremlin.set_current_view()   
    print " view top "

  def on_clear_plot_pressed(self, widget, data=None): 
    self.widgets.gremlin.clear_live_plotter()  
    print " clear plot "
    
  def on_close_pressed(self, widget, data=None):
    gtk.main_quit() 

  def postgui(self):
    inifile = linuxcnc.ini(self.ini_file_path)
    postgui_halfile = inifile.find("HAL", "POSTGUI_HALFILE")
    return postgui_halfile,sys.argv[2]

  def __getitem__(self, item):
        return getattr(self, item)
  def __setitem__(self, item, value):
        return setattr(self, item, value)


  def report_gcode_error(self, result, seq, filename):
    import gcode
    error_str = gcode.strerror(result)
    error = 'G-Code error in ' + os.path.basename(filename) + ' Near line ' + str(seq) + ' of ' + filename + ' ' + error_str
    grotius_gui.update_statusbar(error)

# run the program
if __name__ == "__main__":
  if len(sys.argv) > 2 and sys.argv[1] == '-ini':
    hwg = grotius_gui(sys.argv[2])
  else:
    hwg = grotius_gui()

  # load a postgui file if one is present in the INI file
  postgui_halfile,inifile = grotius_gui.postgui(hwg)

  if postgui_halfile:
    res = os.spawnvp(os.P_WAIT, "halcmd", ["halcmd", "-i",inifile,"-f", postgui_halfile])
    if res: raise SystemExit, res

  gtk.main()
  
#library list 
#self.widgets.power.set_value(100)

#gobject.timeout_add(100, self.periodic)
#def periodic(self):  
#return True

#import buttons
#buttons.test() 

#self.h = hal.component("adaptive")
#self.h.newpin("speed", hal.HAL_FLOAT, hal.HAL_OUT) 
    
#self.widgets.emergency_stop_led.set_active(True)  ## or False

#self.widgets.thc_speed.set_property("color", gtk.gdk.Color("#5dff00"))

    #    aList = [1, 'xyz', 'zara', 'abc']
    #    aList.insert( 1, 1100)
    #    print "Final List : ", aList
        
    #    y = "neeeyy\n"
    #    x = "jo jo jo doei\n"
    #    z = "1"
    #    self.widgets.textbuffer.set_text(x + y + z)
        #self.widgets.textbuffer.add_text(z) 
        #z = z + 1
# self.c.auto(linuxcnc.AUTO_RUN, program_start_line)
# self.widgets.gremlin.metric_units = True

#self.c.teleop_enable(1)

#self.widgets.gremlin.show_program == False
#self.widgets.gremlin.show_program == True


