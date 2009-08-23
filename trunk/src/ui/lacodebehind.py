#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import graphics
import os
import sys
from optparse import OptionParser
from core.interlingua import Interlingua, Concept
from core.utilities import Utilities
from core.lect import Lect
from core.lexicon import Lemma, Word

class AppData:
	def __init_():
		self.lect = None
		self.interlingua = None

data = AppData()

class FrameCodeBehind:
	def __init__(self, frame):
		self.frame = frame
		self.children = {}
		
		self.set_dirty(False)
		self.frame.SetIcon(self.icon())
		
	def set_dirty(self, value = True):
		#self.frame.reload_menu.Enable(value)
		self.frame.save_menu.Enable(value)

	def get_dirty(self):
		return self.frame.save_menu.IsEnabled()
		
	def show_child(self, child_class):
		name = str(child_class)
		if name in self.children:
			child = self.children[name]
		else:
			child = child_class(self.frame, -1, "")
			self.children[name] = child
		child.Show()
		
	def exit(self):
		confirm = True
		if self.get_dirty():
			d= wx.MessageDialog( self, "Are you sure you want to lose all changes?", "Close", wx.ICON_EXCLAMATION|wx.OK|wx.CANCEL)
			# Create a message dialog box
			answer = (d.ShowModal() == wx.ID_OK)
			d.Destroy() # finally destroy it when finished.
		if confirm:
			self.frame.Close(True)

	def icon(self):
		icon = graphics.ArtProvider.get_icon("lilac", wx.ART_OTHER, (16,16))
		return(icon)
	
	
class LACodeBehind(FrameCodeBehind):
	def __init__(self, frame):
	
		FrameCodeBehind.__init__(self, frame)
		
		language_file, interlingua_file, admin = self.__parse_args()
			
		data.interlingua = Interlingua(interlingua_file)
		data.interlingua.load()
		
		if language_file:
			self.__filename = os.path.basename(language_file)
			self.__dirname = os.path.dirname(language_file)
			data.lect = Lect()
			data.lect.load(language_file)
		else:
			self.__filename = ""
			self.__dirname = ""
			data.lect = Lect()
			
		self.__admin = admin
		self.__selected_word_row = None
		
		self.__load_tabs()
	
		
	def __parse_args(self):
		parser = OptionParser("usage: %prog [options] [language_file]")

		parser.add_option("-i", "--interlingua", dest="interlingua",
			default = "data/Latejami.csv", help="Interlingua file to use.", type="string")
		parser.add_option("-a", "--admin", action="store_true", dest="admin",
			default = False, help="Allow administrative tasks.")
			
		options, args = parser.parse_args()

		if len(args)>1:
			parser.print_help()
			sys.exit(0)	

		language_file = None
		if len(args)>0:
			language_file = args[0]
		interlingua_file = options.interlingua
		admin = options.admin
		return (language_file, interlingua_file, admin)		



	def __load_tabs(self):
		lang = data.lect
		frame = self.frame
		frame.code_ctrl.SetValue(lang.code)
		frame.name_ctrl.SetValue(lang.name)
		frame.english_ctrl.SetValue(lang.english_name)
		frame.pos_ctrl.Clear()
		frame.pos_ctrl.AppendItems(lang.get_p_o_s_names())
		frame.lemma_ctrl.Clear()
		for hw in lang.lexicon.iter_lemmas():
			frame.lemma_ctrl.Append("%s.%d" % hw.key(), hw.key())


	def __load_word_grid(self, hw_key):
		def redim(grid, new_rows):
			grid.ClearGrid()
			rows = grid.GetNumberRows()
			if new_rows>rows:
				grid.AppendRows(new_rows - rows)
				for i in range(rows, new_rows):
					grid.SetRowSize(i, 25)
			if new_rows<rows:
				grid.DeleteRows(new_rows, rows - new_rows)
			if new_rows<self.__selected_word_row:
				self.__selected_word_row = None

		words = data.lect.lexicon.retrieve_words(None, hw_key)
		grid = self.frame.word_grid
		redim(grid, len(words))
		for i, w in enumerate(words):
			grid.SetCellValue(i, 0, " ".join(w.categories))
			grid.SetCellValue(i, 1, w.form)
		if self.__selected_word_row is not None:
			grid.SelectRow(self.__selected_word_row)
			w = words[self.__selected_word_row]
			self.frame.word_category_ctrl.SetCategoryValues(w.categories)
			self.frame.form_ctrl.SetValue(w.form)
		else:
			self.frame.word_category_ctrl.SetCategoryValues([])
			self.frame.form_ctrl.SetValue("")
	

	def OnOpen(self, event): # wxGlade: LAFrame.<event_handler>
		fileType = "Lilac language files (.lct)|*.lct"
		dlg = wx.FileDialog(self.frame, "Open a language file...", self.__dirname, "", fileType, wx.OPEN)

		if dlg.ShowModal() == wx.ID_OK:
			self.__filename = dlg.GetFilename()
			self.__dirname = dlg.GetDirectory()
			full_path =  os.path.join(self.__dirname, self.__filename)
			dlg.Destroy()

			self.frame.Refresh()
			self.frame.Update()
			
			wx.BeginBusyCursor()
			try:
				data.lect.load(full_path)
				self.__load_tabs()
				self.set_dirty(False)
			finally:
				wx.EndBusyCursor()
		else:
			dlg.Destroy()

	def OnSave(self, event): # wxGlade: LAFrame.<event_handler>
		full_path =  os.path.join(self.__dirname, self.__filename)
		wx.BeginBusyCursor()
		try:
			data.lect.save(full_path)
			self.set_dirty(False)
		finally:
			wx.EndBusyCursor()
		dlg = wx.MessageDialog(self.frame, "Data have been saved", "Save data", wx.ICON_INFORMATION|wx.OK)
		dlg.ShowModal()
		dlg.Destroy()			

	def OnSaveAs(self, event): # wxGlade: LAFrame.<event_handler>
		fileType = "Lilac language files (.lct)|*.lct"
		dlg = wx.FileDialog(self.frame, "Save the language as...", self.__dirname, self.__filename, fileType, wx.SAVE | wx.OVERWRITE_PROMPT)

		if dlg.ShowModal() == wx.ID_OK:
			self.__filename = dlg.GetFilename()
			self.__dirname = dlg.GetDirectory()
			full_path =  os.path.join(self.__dirname, self.__filename)
			dlg.Destroy()
			self.frame.Refresh()
			self.frame.Update()
			wx.BeginBusyCursor()
			try:
				data.lect.save(full_path)
				self.set_dirty(False)
			finally:
				wx.EndBusyCursor()
		else:
			dlg.Destroy()
			

	def OnExit(self, event): # wxGlade: LAFrame.<event_handler>
		self.exit()

	def OnUndo(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnUndo' not implemented!"
		event.Skip()

	def OnRedo(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRedo' not implemented!"
		event.Skip()

	def OnSelectAll(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnSelectAll' not implemented!"
		event.Skip()

	def OnCut(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnCut' not implemented!"
		event.Skip()

	def OnCopy(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnCopy' not implemented!"
		event.Skip()

	def OnPaste(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnPaste' not implemented!"
		event.Skip()

	def OnClear(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnClear' not implemented!"
		event.Skip()

	def OnOverview(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnOverview' not implemented!"
		event.Skip()


	def OnAbout(self, event): # wxGlade: LAFrame.<event_handler>
		description = """pyLilac Linguistic Laboratory is a graphic interface 
to pyLilac libraries to explore, classify and study languages."""

		licence = """pyLilac Linguistic Laboratory is free software: you can redistribute
it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the
License, or any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>."""


		info = wx.AboutDialogInfo()

		info.SetIcon(wx.Icon('ui/graphics/lilac.png', wx.BITMAP_TYPE_PNG))
		info.SetName('pyLilac Linguistic Laboratory')
		info.SetVersion('0.4')
		info.SetDescription(description)
		info.SetCopyright('(C) 2007-2009 Paolo Olmino')
		info.SetWebSite('http://pylilac.berlios.de')
		info.SetLicence(licence)

		wx.AboutBox(info)


	def OnLemmaSelect(self, event): # wxGlade: LAFrame.<event_handler>
		hw_key = event.GetClientData()
		hw = data.lect.lexicon.get_lemma_by_key(hw_key)
		self.frame.entry_form_ctrl.SetValue(hw.entry_form)
		self.frame.pos_ctrl.SetValue(hw.p_o_s)
		self.frame.lemma_category_ctrl.SetCategoryLabels(data.lect.get_categories(hw.p_o_s)[0])
		self.frame.lemma_category_ctrl.SetCategoryValues(hw.categories)
		if hasattr(hw, "gloss") and hw.gloss:
			self.frame.gloss_ctrl.SetValue(hw.gloss)
			c = data.interlingua.taxonomy.get(hw.gloss)
			self.frame.gloss_ctrl.SetToolTipString(`c`)
		else:
			self.frame.gloss_ctrl.SetValue("-")
		self.frame.word_category_ctrl.SetCategoryLabels(data.lect.get_categories(hw.p_o_s)[1])
		self.__load_word_grid(hw_key)
		
		

	def OnDoSearch(self, event): # wxGlade: LAFrame.<event_handler>
		entry_form = self.frame.search_lemma.GetValue()
		c = self.frame.lemma_ctrl
		for i in range(c.GetCount()):
			s = c.GetString(i)
			if s.upper().startswith(entry_form.upper()):
				c.SetSelection(i)
				break

	def OnDoNewLemma(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnDoNewLemma' not implemented"
		event.Skip()

	def OnDoDeleteLemma(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnDoDeleteLemma' not implemented"
		event.Skip()

	def OnWordSelect(self, event): # wxGlade: LAFrame.<event_handler>
		hw_key = self.frame.lemma_ctrl.GetClientData(self.frame.lemma_ctrl.GetSelection())
		words = data.lect.lexicon.retrieve_words(None, hw_key)
		row = event.GetRow()
		self.__selected_word_row = row
		w = words[row]
		self.frame.word_category_ctrl.SetCategoryValues(w.categories)
		self.frame.form_ctrl.SetValue(w.form)

	def OnDoNewWord(self, event): # wxGlade: LAFrame.<event_handler>
		hw_key = self.frame.lemma_ctrl.GetClientData(self.frame.lemma_ctrl.GetSelection())
		lemma = data.lect.lexicon.get_lemma_by_key(hw_key)
		word = Word(self.frame.form_ctrl.GetValue(), lemma ,self.frame.word_category_ctrl.GetCategoryValues())
		data.lect.lexicon.add_word(word)
		self.__load_word_grid(hw_key)

	def OnDoDeleteWord(self, event): # wxGlade: LAFrame.<event_handler>
		hw_key = self.frame.lemma_ctrl.GetClientData(self.lemma_ctrl.GetSelection())
		words = data.lect.lexicon.retrieve_words(None, hw_key)
		sel_t = self.frame.word_grid.GetSelectionBlockTopLeft()
		sel_b = self.frame.word_grid.GetSelectionBlockBottomRight()
		sel_cnt = len(sel_t)
		for sel_no in range(sel_cnt):
			for row in range(sel_t[sel_no][0], sel_b[sel_no][0] + 1):
				w = words[row]
				data.lect.lexicon.remove_word(w)
		self.__load_word_grid(hw_key)



class CBCodeBehind(FrameCodeBehind):

	def set_dirty(self, value = True):
		self.frame.reload_menu.Enable(value)
		self.frame.save_menu.Enable(value)

	def __init__(self, frame):
		FrameCodeBehind.__init__(self, frame)
		self.__do_tree()

		self.frame.pos_ctrl.AppendItems(data.interlingua.p_o_s)
		self.frame.arg_struct_combo.AppendItems(data.interlingua.arg_struct)

		self.set_dirty(False)
		self.current = None

	def __do_tree(self):
		"""Prepare the tree metadata"""
		tree = self.frame.concept_tree_ctrl

		isz = (16, 16)
		il = wx.ImageList(*isz)
		#wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz)
		self.__tree_icons = {
			"N": il.Add(graphics.ArtProvider.get_bitmap("idea", wx.ART_OTHER, isz)),
			"V": il.Add(graphics.ArtProvider.get_bitmap("action", wx.ART_OTHER, isz)),
			"A": il.Add(graphics.ArtProvider.get_bitmap("label", wx.ART_OTHER, isz)),
			"D": il.Add(graphics.ArtProvider.get_bitmap("brackets", wx.ART_OTHER, isz)),
			"C": il.Add(graphics.ArtProvider.get_bitmap("link", wx.ART_OTHER, isz))
		}

		self.frame.tree_image_list = il
		tree.SetImageList(il)

		# create columns
		tree.AddColumn("Interlingua")
		tree.AddColumn("A.S.")
		tree.AddColumn("Derivation")
		tree.AddColumn("Meaning")
		tree.SetMainColumn(0) # the one with the tree in it...
		tree.SetColumnWidth(0, 170)
		tree.SetColumnWidth(1, 50)
		tree.SetColumnWidth(2, 80)
		tree.SetColumnWidth(3, 200)

		root = tree.AddRoot("[Root]")
		tree.SetItemText(root, "0-n", 1)
		tree.SetItemText(root, "Root", 2)
		tree.SetItemText(root, "", 3)

		self.__load_tree()

	def __load_tree(self):
		def add_tree_children(tree, node, baseconcept):
			for s in data.interlingua.taxonomy.subconcepts(baseconcept):
				child = tree.AppendItem(node, s.interlingua)
				tree.SetItemText(child, s.arg_struct, 1)
				if s.derivation:
					tree.SetItemText(child, s.derivation, 2)
				tree.SetItemText(child, s.meaning, 3)
				tree.SetItemImage(child, self.__tree_icons.get(s.p_o_s))
				add_tree_children(tree, child, s.interlingua)

		concept_tree = self.frame.concept_tree_ctrl
		root = concept_tree.GetRootItem()
		add_tree_children(concept_tree, root, None)
		concept_tree.Expand(root)

	def __fill_controls(self):
		old_dirty = self.get_dirty()

		if self.current == "[Root]":
			concept = Concept("", "", "0-n", "")
		else:
			concept = data.interlingua.taxonomy.get(self.current)
		self.frame.baseconcept_text.SetValue(Utilities.nvl(concept.baseconcept, ""))
		self.frame.derivation_text.SetValue(Utilities.nvl(concept.derivation, ""))
		self.frame.interlingua_text.SetValue(concept.interlingua)
		self.frame.pos_ctrl.SetValue(concept.p_o_s)
		self.frame.arg_struct_combo.SetValue(concept.arg_struct)
		self.frame.meaning_text.SetValue(concept.meaning)
		self.frame.notes_text.SetValue(concept.notes)
		self.frame.reference_text.SetValue(Utilities.nvl(concept.reference, ""))

		self.set_dirty(old_dirty)
		self.frame.ok_button.Enable(False)

	def __find_tree_item(self, parent, value, column = 0, test = 0):
		if test == 1:
			test = lambda x, y: (x.lower() == y.lower())
		elif test == 2:
			test = lambda x, y: (x.lower().find(y.lower())>-1)
		elif test == 0:
			test = lambda x, y: (x == y)

		tree = self.frame.concept_tree_ctrl
		item, cookie = tree.GetFirstChild(parent)
		while item:
			if test(tree.GetItemText(item, column), value):
				tree.EnsureVisible(item)
				tree.SelectItem(item)
				return True
			if tree.ItemHasChildren(item):
				st = self.__find_tree_item(item, value, column, test)
				if st:
					return True
			item, cookie = tree.GetNextChild(parent, cookie)
		return False


	def __reload_tree(self):
		tree = self.frame.concept_tree_ctrl
		root = tree.GetRootItem()
		tree.DeleteChildren(root)
		self.__load_tree()
		self.__find_tree_item(root, self.current)



	#Tree events
	def OnRightUp(self, event): # wxGlade: CBFrame.<event_handler>
		pos = event.GetPosition()
		item, flags, col = self.frame.concept_tree_ctrl.HitTest(pos)
		self.concept_tree_ctrl.SelectItem(item)
		self.PopupMenu(self.edit_menu)

	def OnSelChanged(self, event): # wxGlade: CBFrame.<event_handler>
		item = event.GetItem()
		if item:
			key = self.frame.concept_tree_ctrl.GetItemText(item)
			self.current = key
			self.__fill_controls()

	#Control events
	def OnChange(self, event): # wxGlade: CBFrame.<event_handler>
		self.frame.ok_button.Enable(True)


	#Menu events
	def OnReload(self, event): # wxGlade: CBFrame.<event_handler>
		data.interlingua.load(self.FILENAME)
		self.__reload_tree()
		self.set_dirty(False)

	def OnSave(self, event): # wxGlade: CBFrame.<event_handler>
		wx.BeginBusyCursor()
		try:
			data.interlingua.save()
			self.set_dirty(False)
		finally:
			wx.EndBusyCursor()
		dlg = wx.MessageDialog(self.frame, "Data have been saved", "Save data", wx.ICON_INFORMATION|wx.OK)
		dlg.ShowModal()
		dlg.Destroy()


	def OnSaveAs(self, event): # wxGlade: CBFrame.<event_handler>
		dlg = wx.FileDialog(self.frame, "Save as...",
				 wildcard = "CSV files (*.csv)|*.csv|All files|*.*",
				 style = wx.SAVE)

		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			dlg.Destroy()
			data.interlingua.save(path)
		else:
			dlg.Destroy()


	def OnFind(self, event): # wxGlade: CBFrame.<event_handler>
		#dlg = wx.TextEntryDialog(self, "Interlingua key to find:", "Find", self.current)
		#if dlg.ShowModal() == wx.ID_OK:
			#self.__find_tree_item(self.concept_tree_ctrl.GetRootItem(), dlg.GetValue(), 0, 1)
		#dlg.Destroy()
		dlg = FindDialog(self.frame, -1)
		dlg.CenterOnScreen()
		if dlg.ShowModal() == wx.ID_OK:
			value, column, exact = dlg.GetValue()
			self.__find_tree_item(self.frame.concept_tree_ctrl.GetRootItem(), value, column, exact)
		dlg.Destroy()

	def OnUndo(self, event): # wxGlade: CBFrame.<event_handler>
		self.__fill_controls()
		self.frame.ok_button.Enable(False)

	def OnApply(self, event): # wxGlade: CBFrame.<event_handler>
		new_concept = Concept(
			self.frame.interlingua_text.GetValue(),
			self.frame.pos_ctrl.GetValue(),
			self.frame.arg_struct_combo.GetValue(),
			self.frame.meaning_text.GetValue(),
			self.frame.baseconcept_text.GetValue(),
			self.frame.derivation_text.GetValue())
		if len(self.frame.notes_text.GetValue())>0:
			new_concept.notes = self.notes_text.GetValue()
		if len(self.frame.reference_text.GetValue())>0:
			new_concept.reference = self.frame.reference_text.GetValue()
		if self.current is None: #new subconcept
			self.current = self.frame.interlingua_text.GetValue()
		if self.current:
			data.interlingua.taxonomy.set(new_concept)

			#self.__refresh_tree()
			self.set_dirty(True)

		self.frame.ok_button.Enable(False)
		self.__reload_tree()


	def OnNew(self, event): # wxGlade: CBFrame.<event_handler>
		old_dirty = self.get_dirty()

		baseconcept = data.interlingua.taxonomy.get(self.current)
		self.current = None

		self.frame.baseconcept_text.SetValue(baseconcept.interlingua)
		self.frame.derivation_text.SetValue("DERIVATION")
		self.frame.interlingua_text.SetValue("")
		self.frame.pos_ctrl.SetValue(baseconcept.p_o_s)
		self.frame.arg_struct_combo.SetValue(baseconcept.arg_struct)
		self.frame.meaning_text.SetValue("")
		self.frame.notes_text.SetValue("")
		self.frame.reference_text.SetValue("")

		self.set_dirty(old_dirty)
		self.frame.ok_button.Enable(False)


	def OnDelete(self, event): # wxGlade: CBFrame.<event_handler>
		baseconcept = data.interlingua.taxonomy.get(self.current).baseconcept
		data.interlingua.taxonomy.remove(self.current)
		self.current = baseconcept
		self.set_dirty(True)
		self.__reload_tree()



