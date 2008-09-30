#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid
import wx.gizmos
import graphics
import os
from core.interlingua import Interlingua, Concept
from core.utilities import Utilities
from core.language import Language



class LexiconToolBar(wx.ToolBar):
    def __init__(self, *args, **kwds):
        # begin wxGlade: LexiconToolBar.__init__
        kwds["style"] = wx.TB_DOCKABLE|wx.TB_3DBUTTONS
        wx.ToolBar.__init__(self, *args, **kwds)
        self.AddLabelTool(wx.ID_ADD, "New headword", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.AddLabelTool(wx.ID_GO_FORWARD, "item", wx.NullBitmap, wx.NullBitmap, wx.ITEM_NORMAL, "", "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: LexiconToolBar.__set_properties
        self.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: LexiconToolBar.__do_layout
        pass
        # end wxGlade

# end of class LexiconToolBar


class LAFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: LAFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.la_notebook = wx.Notebook(self, -1, style=0)
		self.la_lexicon_pane = wx.Panel(self.la_notebook, -1)
		
		# Menu Bar
		self.la_frame_menubar = wx.MenuBar()
		self.file_menu = wx.Menu()
		self.open_menu = wx.MenuItem(self.file_menu, wx.ID_OPEN, "Open", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.open_menu)
		self.save_menu = wx.MenuItem(self.file_menu, wx.ID_SAVE, "Save", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.save_menu)
		self.saveas_menu = wx.MenuItem(self.file_menu, wx.ID_SAVEAS, "Save as...", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.saveas_menu)
		self.file_menu.AppendSeparator()
		self.exit_menu = wx.MenuItem(self.file_menu, wx.ID_EXIT, "Exit\tAlt+F4", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.exit_menu)
		self.la_frame_menubar.Append(self.file_menu, "&File")
		self.edit_menu = wx.Menu()
		self.undo_menu = wx.MenuItem(self.edit_menu, wx.ID_UNDO, "Undo\tCtrl+Z", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.undo_menu)
		self.redo_menu = wx.MenuItem(self.edit_menu, wx.ID_REDO, "Redo\tCtrl+Y", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.redo_menu)
		self.edit_menu.AppendSeparator()
		self.select_all_menu = wx.MenuItem(self.edit_menu, wx.ID_SELECTALL, "Select all\tCtrl+rAX", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.select_all_menu)
		self.cut_menu = wx.MenuItem(self.edit_menu, wx.ID_CUT, "Cut\tCtrl+X", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.cut_menu)
		self.copy_menu = wx.MenuItem(self.edit_menu, wx.ID_COPY, "Copy\tCtrl+C", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.copy_menu)
		self.paste_menu = wx.MenuItem(self.edit_menu, wx.ID_PASTE, "Paste\tCtrl+V", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.paste_menu)
		self.clear_menu = wx.MenuItem(self.edit_menu, wx.ID_CLEAR, "Clear", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.clear_menu)
		self.la_frame_menubar.Append(self.edit_menu, "&Edit")
		self.view_menu = wx.Menu()
		self.overview_menu = wx.MenuItem(self.view_menu, wx.NewId(), "Overview", "", wx.ITEM_NORMAL)
		self.view_menu.AppendItem(self.overview_menu)
		self.la_frame_menubar.Append(self.view_menu, "&View")
		self.tools_menu = wx.Menu()
		self.concept_browser_menu = wx.MenuItem(self.tools_menu, wx.NewId(), "Concept Browser", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.concept_browser_menu)
		self.filter_editor_menu = wx.MenuItem(self.tools_menu, wx.NewId(), "Filter Editor", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.filter_editor_menu)
		self.language_reader_menu = wx.MenuItem(self.tools_menu, wx.NewId(), "Language Reader", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.language_reader_menu)
		self.bilingual_interpreter_menu = wx.MenuItem(self.tools_menu, wx.NewId(), "Bilingual Interpreter", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.bilingual_interpreter_menu)
		self.la_frame_menubar.Append(self.tools_menu, "&Tools")
		self.help_menu = wx.Menu()
		self.about_menu = wx.MenuItem(self.help_menu, wx.ID_ABOUT, "About", "", wx.ITEM_NORMAL)
		self.help_menu.AppendItem(self.about_menu)
		self.la_frame_menubar.Append(self.help_menu, "&Help")
		self.SetMenuBar(self.la_frame_menubar)
		# Menu Bar end
		self.la_language_pane = wx.Panel(self.la_notebook, -1)
		self.button_2 = wx.Button(self.la_lexicon_pane, -1, "button_2")
		self.button_3 = wx.Button(self.la_lexicon_pane, -1, "button_3")
		self.la_grammar_pane = wx.Panel(self.la_notebook, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_MENU, self.OnOpen, self.open_menu)
		self.Bind(wx.EVT_MENU, self.OnSave, self.save_menu)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, self.saveas_menu)
		self.Bind(wx.EVT_MENU, self.OnExit, self.exit_menu)
		self.Bind(wx.EVT_MENU, self.OnUndo, self.undo_menu)
		self.Bind(wx.EVT_MENU, self.OnRedo, self.redo_menu)
		self.Bind(wx.EVT_MENU, self.OnSelectAll, self.select_all_menu)
		self.Bind(wx.EVT_MENU, self.OnCut, self.cut_menu)
		self.Bind(wx.EVT_MENU, self.OnCopy, self.copy_menu)
		self.Bind(wx.EVT_MENU, self.OnPaste, self.paste_menu)
		self.Bind(wx.EVT_MENU, self.OnClear, self.clear_menu)
		self.Bind(wx.EVT_MENU, self.OnOverview, self.overview_menu)
		self.Bind(wx.EVT_MENU, self.OnRunConceptBrowser, self.concept_browser_menu)
		self.Bind(wx.EVT_MENU, self.OnRunFilterEditor, self.filter_editor_menu)
		self.Bind(wx.EVT_MENU, self.OnRunLanguageReader, self.language_reader_menu)
		self.Bind(wx.EVT_MENU, self.OnRunBilingualInterpreter, self.bilingual_interpreter_menu)
		self.Bind(wx.EVT_MENU, self.OnAbout, self.about_menu)
		# end wxGlade

		# members
		self.__filename = ""
		self.__dirname = ""
		self.data =  Language()

		self.__cb_frame = None

	def __set_properties(self):
		# begin wxGlade: LAFrame.__set_properties
		self.SetTitle("Lilac - Language Architect")
		self.SetSize((737, 534))
		self.SetToolTipString("Lilac Language Architect")
		# end wxGlade
		icon = graphics.ArtProvider.get_icon("lilac", wx.ART_OTHER, (16,16))
		self.SetIcon(icon)

	def __do_layout(self):
		# begin wxGlade: LAFrame.__do_layout
		la_frame_sizer = wx.BoxSizer(wx.VERTICAL)
		sizer_6 = wx.BoxSizer(wx.VERTICAL)
		grid_sizer_3 = wx.FlexGridSizer(2, 1, 0, 0)
		grid_sizer_4 = wx.GridSizer(1, 2, 0, 0)
		sizer_8 = wx.BoxSizer(wx.VERTICAL)
		grid_sizer_3.Add(sizer_8, 1, wx.EXPAND, 0)
		grid_sizer_4.Add(self.button_2, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 20)
		grid_sizer_4.Add(self.button_3, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 20)
		grid_sizer_3.Add(grid_sizer_4, 1, wx.ALL|wx.EXPAND, 20)
		grid_sizer_3.AddGrowableRow(0)
		grid_sizer_3.AddGrowableCol(0)
		sizer_6.Add(grid_sizer_3, 1, wx.ALL|wx.EXPAND, 0)
		self.la_lexicon_pane.SetSizer(sizer_6)
		self.la_notebook.AddPage(self.la_language_pane, "Language")
		self.la_notebook.AddPage(self.la_lexicon_pane, "Lexicon")
		self.la_notebook.AddPage(self.la_grammar_pane, "Grammar")
		la_frame_sizer.Add(self.la_notebook, 1, wx.EXPAND, 0)
		self.SetSizer(la_frame_sizer)
		self.Layout()
		# end wxGlade

	def OnOpen(self, event): # wxGlade: LAFrame.<event_handler>
		fileType = "Lilac language files (.lg)|*.lg|Pickle files (.p)|*.p"
		dlg = wx.FileDialog(self, "Open a language file...", self.__dirname, "", fileType, wx.OPEN)

		if dlg.ShowModal() == wx.ID_OK:
			self.__filename = dlg.GetFilename()
			self.__dirname = dlg.GetDirectory()
			full_path =  os.path.join(self.__dirname, self.__filename)
			wx.BeginBusyCursor()
			try:
				self.data.load(full_path)
			finally:
				wx.EndBusyCursor()

		dlg.Destroy()

	def OnSave(self, event): # wxGlade: LAFrame.<event_handler>
		full_path =  os.path.join(self.__dirname, self.__filename)
		wx.BeginBusyCursor()
		try:
			self.data.save(full_path)
		finally:
			wx.EndBusyCursor()

	def OnSaveAs(self, event): # wxGlade: LAFrame.<event_handler>
		fileType = "Lilac language files (.lg)|*.lg|Pickle files (.p)|*.p"
		dlg = wx.FileDialog(self, "Save the language as...", self.__dirname, self.__filename, fileType, wx.SAVE | wx.OVERWRITE_PROMPT)

		if dlg.ShowModal() == wx.ID_OK:
			self.__filename = dlg.GetFilename()
			self.__dirname = dlg.GetDirectory()
			full_path =  os.path.join(self.__dirname, self.__filename)
			wx.BeginBusyCursor()
			try:
				self.data.save(full_path)
			finally:
				wx.EndBusyCursor()

		dlg.Destroy()

	def OnExit(self, event): # wxGlade: LAFrame.<event_handler>
		self.Close(True)

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

	def OnRunConceptBrowser(self, event): # wxGlade: LAFrame.<event_handler>
		if not self.__cb_frame:
			self.__cb_frame = CBFrame(self, -1, "")
		self.__cb_frame.Show()
		
	def OnRunFilterEditor(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRunFilterEditor' not implemented!"
		event.Skip()

	def OnRunLanguageReader(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRunLanguageReader' not implemented!"
		event.Skip()

	def OnRunBilingualInterpreter(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRunBilingualInterpreter' not implemented"
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
		info.SetVersion('0.3.0')
		info.SetDescription(description)
		info.SetCopyright('(C) 2007 Paolo Olmino')
		info.SetWebSite('http://pylilac.berlios.de')
		info.SetLicence(licence)

		wx.AboutBox(info)



# end of class LAFrame

class CBFrame(wx.Frame):
	FILENAME = "data/Latejami.ilt"

	def __init__(self, *args, **kwds):
		# begin wxGlade: CBFrame.__init__
		kwds["style"] = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.RESIZE_BORDER|wx.FRAME_FLOAT_ON_PARENT|wx.CLIP_CHILDREN
		wx.Frame.__init__(self, *args, **kwds)
		self.panel_1 = wx.Panel(self, -1)
		
		# Menu Bar
		self.cb_frame_menubar = wx.MenuBar()
		self.file_menu = wx.Menu()
		self.reload_menu = wx.MenuItem(self.file_menu, wx.ID_REVERT_TO_SAVED, "&Revert", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.reload_menu)
		self.save_menu = wx.MenuItem(self.file_menu, wx.ID_SAVE, "&Save", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.save_menu)
		self.export_menu = wx.MenuItem(self.file_menu, wx.NewId(), "E&xport", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.export_menu)
		self.file_menu.AppendSeparator()
		self.exit_menu = wx.MenuItem(self.file_menu, wx.ID_CLOSE, "Exit\tAlt+F4", "", wx.ITEM_NORMAL)
		self.file_menu.AppendItem(self.exit_menu)
		self.cb_frame_menubar.Append(self.file_menu, "&File")
		self.view_menu = wx.Menu()
		self.find_menu = wx.MenuItem(self.view_menu, wx.ID_FIND, "&Find...", "", wx.ITEM_NORMAL)
		self.view_menu.AppendItem(self.find_menu)
		self.view_menu.AppendSeparator()
		self.view_menu.Append(wx.ID_UNDO, "&Undo changes", "", wx.ITEM_NORMAL)
		self.apply_menu = wx.MenuItem(self.view_menu, wx.ID_APPLY, "&Apply changes", "", wx.ITEM_NORMAL)
		self.view_menu.AppendItem(self.apply_menu)
		self.cb_frame_menubar.Append(self.view_menu, "&View")
		self.edit_menu = wx.Menu()
		self.new_menu = wx.MenuItem(self.edit_menu, wx.ID_ADD, "&New subconcept", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.new_menu)
		self.delete_menu = wx.MenuItem(self.edit_menu, wx.ID_REMOVE, "&Delete concept", "", wx.ITEM_NORMAL)
		self.edit_menu.AppendItem(self.delete_menu)
		self.cb_frame_menubar.Append(self.edit_menu, "&Edit")
		self.SetMenuBar(self.cb_frame_menubar)
		# Menu Bar end
		self.concept_tree_ctrl = wx.gizmos.TreeListCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_LINES_AT_ROOT|wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)
		self.baseconcept_label = wx.StaticText(self.panel_1, -1, "Lineage")
		self.baseconcept_text = wx.TextCtrl(self.panel_1, -1, "")
		self.derivation_text = wx.TextCtrl(self.panel_1, -1, "")
		self.interlingua_label = wx.StaticText(self.panel_1, -1, "Interlingua")
		self.interlingua_text = wx.TextCtrl(self.panel_1, -1, "")
		self.pos_label = wx.StaticText(self.panel_1, -1, "Part of Speech")
		self.pos_combo = wx.ComboBox(self.panel_1, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.arg_struct_label = wx.StaticText(self.panel_1, -1, "Argument structure")
		self.arg_struct_combo = wx.ComboBox(self.panel_1, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_DROPDOWN)
		self.meaning_label = wx.StaticText(self.panel_1, -1, "Meaning")
		self.meaning_text = wx.TextCtrl(self.panel_1, -1, "")
		self.notes_label = wx.StaticText(self.panel_1, -1, "Notes")
		self.notes_text = wx.TextCtrl(self.panel_1, -1, "", style=wx.TE_MULTILINE|wx.TE_WORDWRAP)
		self.reference_label = wx.StaticText(self.panel_1, -1, "Reference")
		self.reference_text = wx.TextCtrl(self.panel_1, -1, "")
		self.cancel_button = wx.Button(self.panel_1, -1, "&Undo")
		self.ok_button = wx.Button(self.panel_1, -1, "&Apply")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_MENU, self.OnReload, self.reload_menu)
		self.Bind(wx.EVT_MENU, self.OnSave, self.save_menu)
		self.Bind(wx.EVT_MENU, self.OnExport, self.export_menu)
		self.Bind(wx.EVT_MENU, self.OnExit, self.exit_menu)
		self.Bind(wx.EVT_MENU, self.OnFind, self.find_menu)
		self.Bind(wx.EVT_MENU, self.OnUndo, id=wx.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.OnApply, self.apply_menu)
		self.Bind(wx.EVT_MENU, self.OnNew, self.new_menu)
		self.Bind(wx.EVT_MENU, self.OnDelete, self.delete_menu)
		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.concept_tree_ctrl)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.baseconcept_text)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.derivation_text)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.interlingua_text)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.pos_combo)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.arg_struct_combo)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.meaning_text)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.reference_text)
		self.Bind(wx.EVT_BUTTON, self.OnUndo, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnApply, self.ok_button)
		# end wxGlade
		
		#self.cb_frame_toolbar = wx.ToolBar(self, -1)
		#isz = (16, 16)
		#self.cb_frame_toolbar.AddLabelTool(wx.ID_NEW, "New", wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, isz), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
		#self.SetToolBar(self.cb_frame_toolbar)

		self.data = Interlingua("Latejami")
		self.data.load(self.FILENAME)
		self.__do_tree()
		self.concept_tree_ctrl.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)

		self.pos_combo.AppendItems(self.data.p_o_s)
		self.arg_struct_combo.AppendItems(self.data.arg_struct)

		self.__set_dirty(False)
		self.current = None


	def __set_properties(self):
		# begin wxGlade: CBFrame.__set_properties
		self.SetTitle("Concept browser")
		self.SetSize((850, 420))
		self.concept_tree_ctrl.SetMinSize((500,400))
		self.ok_button.Enable(False)
		self.ok_button.SetDefault()
		self.panel_1.SetMinSize((300,400))
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: CBFrame.__do_layout
		sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
		grid_sizer_1 = wx.FlexGridSizer(1, 2, 0, 0)
		sizer_3 = wx.FlexGridSizer(2, 1, 0, 0)
		sizer_4 = wx.GridSizer(1, 2, 0, 0)
		control_grid_sizer = wx.FlexGridSizer(7, 2, 4, 4)
		sizer_2 = wx.FlexGridSizer(1, 2, 0, 0)
		grid_sizer_1.Add(self.concept_tree_ctrl, 1, wx.EXPAND, 0)
		control_grid_sizer.Add(self.baseconcept_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_2.Add(self.baseconcept_text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_2.Add(self.derivation_text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_2.AddGrowableCol(0)
		sizer_2.AddGrowableCol(1)
		control_grid_sizer.Add(sizer_2, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.interlingua_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.interlingua_text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.pos_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.pos_combo, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.arg_struct_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.arg_struct_combo, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.meaning_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.meaning_text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.notes_label, 0, 0, 0)
		control_grid_sizer.Add(self.notes_text, 0, wx.EXPAND, 0)
		control_grid_sizer.Add(self.reference_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.Add(self.reference_text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		control_grid_sizer.AddGrowableCol(1)
		sizer_3.Add(control_grid_sizer, 1, wx.ALL|wx.EXPAND, 20)
		sizer_4.Add(self.cancel_button, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 20)
		sizer_4.Add(self.ok_button, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 0)
		sizer_3.Add(sizer_4, 1, wx.ALL|wx.EXPAND, 20)
		self.panel_1.SetSizer(sizer_3)
		sizer_3.AddGrowableRow(0)
		sizer_3.AddGrowableCol(0)
		grid_sizer_1.Add(self.panel_1, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 0)
		grid_sizer_1.AddGrowableRow(0)
		grid_sizer_1.AddGrowableCol(0)
		grid_sizer_1.AddGrowableCol(1)
		sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		self.Layout()
		# end wxGlade

	def __do_tree(self):
		"""Prepare the tree metadata"""
		tree = self.concept_tree_ctrl
		
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
	
		self.tree_image_list = il
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
		def add_tree_children(node, baseconcept):
			for s in self.data.taxonomy.subconcepts(baseconcept):
				child = tree.AppendItem(node, s.interlingua)
				tree.SetItemText(child, s.arg_struct, 1)
				if s.derivation:
					tree.SetItemText(child, s.derivation, 2)
				tree.SetItemText(child, s.meaning, 3)
				tree.SetItemImage(child, self.__tree_icons.get(s.p_o_s))
				add_tree_children(child, s.interlingua)

		tree = self.concept_tree_ctrl
		root = tree.GetRootItem()
	
		#tree.SetItemImage(root, icons["N"])
		#tree.SetItemImage(root, fldropenidx, wx.TreeItemIcon_Expanded)
	
		add_tree_children(root, None)
			
		tree.Expand(root)

	def __fill_controls(self):
		old_dirty = self.__get_dirty()

		if self.current == "[Root]":
			concept = Concept("", "", "0-n", "")
		else:
			concept = self.data.taxonomy.get(self.current)
		self.baseconcept_text.SetValue(Utilities.nvl(concept.baseconcept, ""))
		self.derivation_text.SetValue(Utilities.nvl(concept.derivation, ""))
		self.interlingua_text.SetValue(concept.interlingua)
		self.pos_combo.SetValue(concept.p_o_s)
		self.arg_struct_combo.SetValue(concept.arg_struct)
		self.meaning_text.SetValue(concept.meaning)
		self.notes_text.SetValue(concept.notes)
		self.reference_text.SetValue(Utilities.nvl(concept.reference, ""))
		
		self.__set_dirty(old_dirty)
		self.ok_button.Enable(False)
		
	def __find_tree_item(self, parent, value, column = 0, exact = 0):
		if exact == 1:
			test = lambda x, y: (x.lower() == y.lower())
		elif exact == 2:
			test = lambda x, y: (x.lower().find(y.lower())>-1)
		else:
			test = lambda x, y: (x == y)

		tree = self.concept_tree_ctrl
		item, cookie = tree.GetFirstChild(parent)
		while item:
			if test(tree.GetItemText(item, column), value):
				tree.EnsureVisible(item)
				tree.SelectItem(item)
				return True
			if tree.ItemHasChildren(item):
				return self.__find_tree_item(item, value, column, exact)
			item, cookie = tree.GetNextChild(parent, cookie)
		return False
		
	def __reload_tree(self):
		tree = self.concept_tree_ctrl
		root = tree.GetRootItem()
		tree.DeleteChildren(root)
		self.__load_tree()
		self.__find_tree_item(root, self.current)
		
	def __set_dirty(self, value = True):
		self.reload_menu.Enable(value)
		self.save_menu.Enable(value)
		
	def __get_dirty(self):
		return self.save_menu.IsEnabled()
		
		
	#Tree events
	def OnRightUp(self, event): # wxGlade: CBFrame.<event_handler>
		pos = event.GetPosition()
		item, flags, col = self.concept_tree_ctrl.HitTest(pos)
		self.concept_tree_ctrl.SelectItem(item)
		self.PopupMenu(self.edit_menu)

	def OnSelChanged(self, event): # wxGlade: CBFrame.<event_handler>
		item = event.GetItem()
		if item:
			key = self.concept_tree_ctrl.GetItemText(item)
			self.current = key
			self.__fill_controls()

	#Control events
	def OnChange(self, event): # wxGlade: CBFrame.<event_handler>
		self.ok_button.Enable(True)


	#Menu events
	def OnReload(self, event): # wxGlade: CBFrame.<event_handler>
		self.data.load(self.FILENAME)
		self.__reload_tree()
		self.__set_dirty(False)

	def OnSave(self, event): # wxGlade: CBFrame.<event_handler>
		self.data.save(self.FILENAME)
		dlg = wx.MessageDialog(self, "Data have been saved", "Save data", wx.ICON_INFORMATION|wx.OK)
		dlg.ShowModal()
		dlg.Destroy()
		self.__set_dirty(False)


	def OnExport(self, event): # wxGlade: CBFrame.<event_handler>
		def csv_format(x):
			if x is None:
				return ""
			else:
				return "\"" + str(x).replace("\"", "\"\"") + "\""
		#dlg = wx.FileDialog(self, message="Save file as ...", defaultDir=os.getcwd(), defaultFile="", wildcard=wildcard, style=wx.SAVE)
		dlg = wx.FileDialog(self, "Export taxonomy as...", wildcard = "CSV files (*.csv)|*.csv|All files|*.*"
, style = wx.SAVE)

		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			try:
				out = open(path, "w")
				for c in self.data.taxonomy:
					out.write("%s,%s,%s,%s,%s,%s,%s,%s\n" %
					(csv_format(c.interlingua), csv_format(c.p_o_s), csv_format(c.arg_struct), csv_format(c.meaning), csv_format(c.baseconcept), csv_format(c.derivation), csv_format(c.notes), csv_format(c.reference))
					)
				out.flush()
			finally:
				out.close()
		dlg.Destroy()


	def OnExit(self, event): # wxGlade: CBFrame.<event_handler>
		confirm = True
		if self.__get_dirty():
			d= wx.MessageDialog( self, "Are you sure you want to lose all changes?", "Close", wx.ICON_EXCLAMATION|wx.OK|wx.CANCEL)
			# Create a message dialog box
			answer = (d.ShowModal() == wx.ID_OK)
			d.Destroy() # finally destroy it when finished.
		if confirm:
			self.Close(True)

	def OnFind(self, event): # wxGlade: CBFrame.<event_handler>
		#dlg = wx.TextEntryDialog(self, "Interlingua key to find:", "Find", self.current)
		#if dlg.ShowModal() == wx.ID_OK:
			#self.__find_tree_item(self.concept_tree_ctrl.GetRootItem(), dlg.GetValue(), 0, 1)
		#dlg.Destroy()
		dlg = FindDialog(self, -1)
		dlg.CenterOnScreen()
		if dlg.ShowModal() == wx.ID_OK:
			value, column, exact = dlg.GetValue()
			self.__find_tree_item(self.concept_tree_ctrl.GetRootItem(), value, column, exact)
		dlg.Destroy()

	def OnUndo(self, event): # wxGlade: CBFrame.<event_handler>
		self.__fill_controls()
		self.ok_button.Enable(False)

	def OnApply(self, event): # wxGlade: CBFrame.<event_handler>
		new_concept = Concept(
			self.interlingua_text.GetValue(),
			self.pos_combo.GetValue(),
			self.arg_struct_combo.GetValue(),
			self.meaning_text.GetValue(),
			self.baseconcept_text.GetValue(),
			self.derivation_text.GetValue())
		if len(self.notes_text.GetValue())>0:
			new_concept.notes = self.notes_text.GetValue()
		if len(self.reference_text.GetValue())>0:
			new_concept.reference = self.reference_text.GetValue()
		if self.current is None: #new subconcept
			self.current = self.interlingua_text.GetValue()
		if self.current:
			self.data.taxonomy.set(new_concept)
			
			#self.__refresh_tree()
			self.__set_dirty(True)
	
		self.ok_button.Enable(False)
		self.__reload_tree()


	def OnNew(self, event): # wxGlade: CBFrame.<event_handler>
		old_dirty = self.__get_dirty()
		
		baseconcept = self.data.taxonomy.get(self.current)
		self.current = None

		self.baseconcept_text.SetValue(baseconcept.interlingua)
		self.derivation_text.SetValue("DERIVATION")
		self.interlingua_text.SetValue("")
		self.pos_combo.SetValue(baseconcept.p_o_s)
		self.arg_struct_combo.SetValue(baseconcept.arg_struct)
		self.meaning_text.SetValue("")
		self.notes_text.SetValue("")
		self.reference_text.SetValue("")

		self.__set_dirty(old_dirty)
		self.ok_button.Enable(False)
		

	def OnDelete(self, event): # wxGlade: CBFrame.<event_handler>
		baseconcept = self.data.taxonomy.get(self.current).baseconcept
		self.data.taxonomy.remove(self.current)
		self.current = baseconcept
		self.__set_dirty(True)
		self.__reload_tree()



# end of class CBFrame

class FindDialog(wx.Dialog):
	def __init__(self, *args, **kwds):
		# begin wxGlade: FindDialog.__init__
		kwds["style"] = wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.field_label = wx.StaticText(self, -1, "Field to search:")
		self.field_combo = wx.ComboBox(self, -1, choices=["Interlingua", "Meaning"], style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.value_label = wx.StaticText(self, -1, "Find what:")
		self.value_text = wx.TextCtrl(self, -1, "")
		self.exact_check = wx.CheckBox(self, -1, "Partial match")
		self.panel_3 = wx.Panel(self, -1)
		self.cancel_button = wx.Button(self, wx.ID_CANCEL, "")
		self.ok_button = wx.Button(self, wx.ID_FIND, "")

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_BUTTON, self.OnUndo, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnApply, self.ok_button)
		# end wxGlade


	def __set_properties(self):
		# begin wxGlade: FindDialog.__set_properties
		self.SetTitle("Find concept")
		self.SetSize((450, 188))
		self.field_combo.SetSelection(0)
		self.ok_button.Enable(False)
		self.ok_button.SetDefault()
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: FindDialog.__do_layout
		sizer_5 = wx.FlexGridSizer(1, 2, 0, 0)
		sizer_4 = wx.GridSizer(2, 1, 0, 0)
		grid_sizer_2 = wx.FlexGridSizer(3, 2, 5, 0)
		grid_sizer_2.Add(self.field_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		grid_sizer_2.Add(self.field_combo, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		grid_sizer_2.Add(self.value_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		grid_sizer_2.Add(self.value_text, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 0)
		grid_sizer_2.Add(self.exact_check, 0, wx.ALIGN_BOTTOM, 0)
		grid_sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)
		grid_sizer_2.AddGrowableCol(1)
		sizer_5.Add(grid_sizer_2, 1, wx.ALL|wx.EXPAND, 20)
		sizer_4.Add(self.cancel_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_4.Add(self.ok_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_5.Add(sizer_4, 1, wx.ALL|wx.EXPAND, 20)
		self.SetSizer(sizer_5)
		sizer_5.AddGrowableCol(0)
		self.Layout()
		# end wxGlade
	
	def GetValue(self):
		field = self.field_combo.GetValue()
		if field[0] == "M":
			column = 3
		else:
			column = 0
		value = self.value_text.GetValue()
		test_mode = self.exact_check.IsChecked()
		if test_mode:
			exact = 2
		else:
			exact = 1
		return (value, column, exact)
	
	def OnUndo(self, event): # wxGlade: FindDialog.<event_handler>
		print "Event handler `OnUndo' not implemented"
		event.Skip()
	
	def OnApply(self, event): # wxGlade: FindDialog.<event_handler>
		print "Event handler `OnApply' not implemented"
		event.Skip()

# end of class FindDialog


class LAApp(wx.App):
	def OnInit(self):
		wx.InitAllImageHandlers()
		la_frame = LAFrame(None, -1, "")
		self.SetTopWindow(la_frame)
		la_frame.Show()
		return 1

# end of class LAApp

if __name__ == "__main__":
	language_architect = LAApp(0)
	language_architect.MainLoop()
