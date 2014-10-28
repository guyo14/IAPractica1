'''
Created on Oct 22, 2014

@author: alejandro
'''

from gi.repository import Gtk, Pango

import files
import algorithm
from wxPython._wx import NULL
from pkg.algorithm import gradient_descent

class MainWindow(Gtk.Window):
	'''
	classdocs
	'''
	
	
	def __init__(self):
		'''
		Constructor
		'''
		Gtk.Window.__init__(self, title="Gradiente Descendente")
		self.set_border_width(10)
		
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(vbox)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		label = Gtk.Label("Archivo de x's:", xalign=0)
		self.filex_entry = Gtk.Entry()
		button = Gtk.Button("Cargar")
		button.connect("clicked", self.on_openbuttons_clicked, self.filex_entry)
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.filex_entry, True, True, 0)
		hbox.pack_start(button, True, True, 0)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		label = Gtk.Label("Archivo de y's:", xalign=0)
		self.filey_entry = Gtk.Entry()
		button = Gtk.Button("Cargar")
		button.connect("clicked", self.on_openbuttons_clicked, self.filey_entry)
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.filey_entry, True, True, 0)
		hbox.pack_start(button, True, True, 0)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		label = Gtk.Label("Alfa:", xalign=0)
		self.alpha_entry = Gtk.Entry()
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.alpha_entry, True, True, 0)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		label = Gtk.Label("Numero de iteraciones:", xalign=0)
		self.iterations_entry = Gtk.Entry()
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.iterations_entry, True, True, 0)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		label = Gtk.Label("Tolerancia:", xalign=0)
		self.tolerance_entry = Gtk.Entry()
		hbox.pack_start(label, True, True, 0)
		hbox.pack_start(self.tolerance_entry, True, True, 0)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		self.go_button = Gtk.Button("Iniciar")
		self.go_button.connect("clicked", self.on_go_button_clicked)
		hbox.pack_start(self.go_button, True, True, 0)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		scroll = Gtk.ScrolledWindow()
		scroll.set_hexpand(True)
		scroll.set_vexpand(True)
		hbox.pack_start(scroll, True, True, 0)
		self.log_textview = Gtk.TextView()
		self.log_textbuffer = self.log_textview.get_buffer()
		scroll.add(self.log_textview)
		self.log_textview.set_cursor_visible(False)
		self.log_textview.set_editable(False)
		self.tag_bold = self.log_textbuffer.create_tag("bold", weight=Pango.Weight.BOLD)
		self.tag_italic = self.log_textbuffer.create_tag("italic", style=Pango.Style.ITALIC)
		
		hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		vbox.pack_start(hbox, True, True, 0)
		self.export_button = Gtk.Button("Exportar")
		hbox.pack_start(self.export_button, True, True, 0)
	
	
	def on_openbuttons_clicked(self, widget, entry):
		dialog = Gtk.FileChooserDialog("Please choose a file", self,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		
		self.add_filters(dialog)
		
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			entry.set_text(dialog.get_filename())
		
		dialog.destroy()
	
	
	def on_go_button_clicked(self, widget):
		filex = self.filex_entry.get_text()
		filey = self.filey_entry.get_text()
		self.log_textbuffer.set_text("")
		error = False
		
		self.write_in_log("Iniciando\n", 1)
		
		self.write_in_log("Leyendo archivo de x's\n", 2)
		if files.verifyFile(filex):
			xstrings = files.readFile(filex)
			xs = self.verify_lists(xstrings)
			if xs == NULL:
				self.write_in_log("\tNo se encontro archivo de x's\n", 0)
				error = True
			else:
				self.write_in_log("\tValores de x: " + str(xs) + "\n", 0)
		else:
			self.write_in_log("\tNo se encontro archivo de x's\n", 0)
			error = True
		
		self.write_in_log("Leyendo archivo de y's\n", 2)
		if files.verifyFile(filey):
			ystrings = files.readFile(filey)
			ys = self.verify_lists(ystrings)
			if ys == NULL:
				self.write_in_log("\tNo se encontro archivo de x's\n", 0)
				error = True
			else:
				self.write_in_log("\tValores de y: " + str(ys) + "\n", 0)
		else:
			self.write_in_log("\tNo se encontro archivo de y's\n", 0)
			error = True
		
		if xs != NULL and ys != NULL:
			self.write_in_log("Validando corcordancia de datos (x's y y's)\n", 2)
			if len(xs) == len(ys):
				self.write_in_log("Los datos concuerdan\n", 0)
			else:
				self.write_in_log("Los datos no concuerdan\n", 1)
				error = True
		
		self.write_in_log("Validando alfa\n", 2)
		try:
			alpha = float(self.alpha_entry.get_text())
			self.write_in_log("\tAlfa: " + repr(alpha) + "\n", 0)
		except ValueError:
			self.write_in_log("\tAlfa no valido\n", 0)
		
		self.write_in_log("Validando numero de iteraciones\n", 2)
		try:
			iterations = int(self.iterations_entry.get_text())
			self.write_in_log("\tNumero de iteraciones: " + repr(iterations) + "\n", 0)
		except ValueError:
			self.write_in_log("\tNumero de iteraciones no valido\n", 0)
		
		self.write_in_log("Validando tolerancia\n", 2)
		try:
			tolerance = float(self.tolerance_entry.get_text())
			self.write_in_log("\tTolerancia: " + repr(tolerance) + "\n", 0)
		except ValueError:
			self.write_in_log("\tToleracia no valida\n", 0)
		
		if not error:
			self.write_in_log("Parametros validos\n", 2)
			self.write_in_log("Iniciando algoritmo\n", 1)
			thetas = gradient_descent(xs, ys, alpha, tolerance, iterations)
			self.write_in_log("Valores teta: " + str(thetas) + "\n", 0)
			self.write_in_log("Finalizacion exitosa\n", 1)
		else:
			self.write_in_log("Parametros no validos\n", 2)
			self.write_in_log("Finalizacion prematura\n", 1)
	
	
	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)
		
		filter_py = Gtk.FileFilter()
		filter_py.set_name("Python files")
		filter_py.add_mime_type("text/x-python")
		dialog.add_filter(filter_py)
		
		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)
	
	
	def write_in_log(self, text, val):
		end = self.log_textbuffer.get_end_iter()
		if val == 1:
			self.log_textbuffer.insert_with_tags(end, text, self.tag_bold)
		elif val == 2:
			self.log_textbuffer.insert_with_tags(end, text, self.tag_italic)
		else:
			self.log_textbuffer.insert(end, text)
	
	
	def verify_lists(self, rows):
		if len(rows) <= 0:
			return NULL
		result = []
		rowSize = len(rows[0])
		for row in rows:
			if len(row) == rowSize:
				tmpRow = []
				for number in row:
					try:
						tmpRow.append(float(number))
					except ValueError:
						return NULL
				result.append(tmpRow)
			else:
				return NULL
		return result
						
			