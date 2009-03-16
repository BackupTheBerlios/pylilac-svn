#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.grid
import wx.gizmos
import graphics
import os
import sys
from ui.lacodebehind import LACodeBehind, CBCodeBehind
from ui.lawidgets import StockBitmapButton, CategoryPanelComboCtrl


class LAFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: LAFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.la_notebook = wx.Notebook(self, -1, style=0)
		self.la_lexicon_pane = wx.Panel(self.la_notebook, -1)
		self.la_language_pane = wx.Panel(self.la_notebook, -1)
		self.language_sizer_2_staticbox = wx.StaticBox(self.la_language_pane, -1, "Properties:")
		self.language_sizer_3_staticbox = wx.StaticBox(self.la_language_pane, -1, "Blabla:")
		self.word_panel_staticbox = wx.StaticBox(self.la_lexicon_pane, -1, "Words:")
		self.language_sizer_1_staticbox = wx.StaticBox(self.la_language_pane, -1, "Language:")
		
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
		self.overview_menu = wx.MenuItem(self.view_menu, wx.ID_ANY, "Overview", "", wx.ITEM_NORMAL)
		self.view_menu.AppendItem(self.overview_menu)
		self.la_frame_menubar.Append(self.view_menu, "&View")
		self.tools_menu = wx.Menu()
		self.concept_browser_menu = wx.MenuItem(self.tools_menu, wx.ID_ANY, "Concept Browser", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.concept_browser_menu)
		self.filter_editor_menu = wx.MenuItem(self.tools_menu, wx.ID_ANY, "Filter Editor", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.filter_editor_menu)
		self.language_reader_menu = wx.MenuItem(self.tools_menu, wx.ID_ANY, "Language Reader", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.language_reader_menu)
		self.bilingual_interpreter_menu = wx.MenuItem(self.tools_menu, wx.ID_ANY, "Bilingual Interpreter", "", wx.ITEM_NORMAL)
		self.tools_menu.AppendItem(self.bilingual_interpreter_menu)
		self.la_frame_menubar.Append(self.tools_menu, "&Tools")
		self.help_menu = wx.Menu()
		self.about_menu = wx.MenuItem(self.help_menu, wx.ID_ABOUT, "About", "", wx.ITEM_NORMAL)
		self.help_menu.AppendItem(self.about_menu)
		self.la_frame_menubar.Append(self.help_menu, "&Help")
		self.SetMenuBar(self.la_frame_menubar)
		# Menu Bar end
		self.label_1 = wx.StaticText(self.la_language_pane, -1, "Code:")
		self.code_ctrl = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_4 = wx.StaticText(self.la_language_pane, -1, "label_4")
		self.text_ctrl_4 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_2 = wx.StaticText(self.la_language_pane, -1, "Name:")
		self.name_ctrl = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_5 = wx.StaticText(self.la_language_pane, -1, "label_5")
		self.text_ctrl_5 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_3 = wx.StaticText(self.la_language_pane, -1, "English Name:")
		self.english_ctrl = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_6 = wx.StaticText(self.la_language_pane, -1, "label_6")
		self.text_ctrl_6 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_11 = wx.StaticText(self.la_language_pane, -1, "Separator:")
		self.separator_ctrl = wx.ComboBox(self.la_language_pane, -1, choices=["None (\"\")", "Space (\" \")"], style=wx.CB_DROPDOWN)
		self.label_13 = wx.StaticText(self.la_language_pane, -1, "label_13")
		self.text_ctrl_13 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_12 = wx.StaticText(self.la_language_pane, -1, "Capitalization:")
		self.capitalization_ctrl = wx.ListBox(self.la_language_pane, -1, choices=["Initial", "Lexical"], style=wx.LB_MULTIPLE)
		self.label_14 = wx.StaticText(self.la_language_pane, -1, "label_14")
		self.text_ctrl_14 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_21 = wx.StaticText(self.la_language_pane, -1, "label_21")
		self.text_ctrl_21 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_24 = wx.StaticText(self.la_language_pane, -1, "label_24")
		self.text_ctrl_24 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_22 = wx.StaticText(self.la_language_pane, -1, "label_22")
		self.text_ctrl_22 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_25 = wx.StaticText(self.la_language_pane, -1, "label_25")
		self.text_ctrl_25 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_23 = wx.StaticText(self.la_language_pane, -1, "label_23")
		self.text_ctrl_23 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.label_26 = wx.StaticText(self.la_language_pane, -1, "label_26")
		self.text_ctrl_26 = wx.TextCtrl(self.la_language_pane, -1, "")
		self.language_sizer_right = wx.Panel(self.la_language_pane, -1)
		self.search_lemma = wx.SearchCtrl(self.la_lexicon_pane, -1, "", style=wx.TE_PROCESS_ENTER)
		self.clear_search_button = wx.Button(self.la_lexicon_pane, wx.ID_CLEAR, "")
		self.lemma_ctrl = wx.ListBox(self.la_lexicon_pane, -1, choices=[], style=wx.LB_SINGLE|wx.LB_SORT)
		self.entry_form_label = wx.StaticText(self.la_lexicon_pane, -1, "Entry Form")
		self.entry_form_ctrl = wx.TextCtrl(self.la_lexicon_pane, -1, "")
		self.entry_id_spin = wx.SpinCtrl(self.la_lexicon_pane, -1, "", min=0, max=100)
		self.pos_label = wx.StaticText(self.la_lexicon_pane, -1, "Part of Speech")
		self.pos_ctrl = wx.ComboBox(self.la_lexicon_pane, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.lemma_categories_label = wx.StaticText(self.la_lexicon_pane, -1, "Categories")
		self.lemma_category_ctrl = CategoryPanelComboCtrl(self.la_lexicon_pane, -1, choices=[], style=wx.CB_DROPDOWN)
		self.gloss_label = wx.StaticText(self.la_lexicon_pane, -1, "Gloss")
		self.gloss_ctrl = wx.TextCtrl(self.la_lexicon_pane, -1, "")
		self.generate_words_button = StockBitmapButton(self.la_lexicon_pane, -1, "wxART_NEW")
		self.new_word_button = StockBitmapButton(self.la_lexicon_pane, -1, "wxART_NEW")
		self.delete_word_button = StockBitmapButton(self.la_lexicon_pane, -1, "wxART_DELETE")
		self.xxx_button = StockBitmapButton(self.la_lexicon_pane, -1, "wxART_DELETE")
		self.word_grid = wx.grid.Grid(self.la_lexicon_pane, -1, size=(1, 1))
		self.word_category_label = wx.StaticText(self.la_lexicon_pane, -1, "Categories")
		self.word_category_ctrl = CategoryPanelComboCtrl(self.la_lexicon_pane, -1, choices=[], style=wx.CB_DROPDOWN)
		self.form_label = wx.StaticText(self.la_lexicon_pane, -1, "Form")
		self.form_ctrl = wx.TextCtrl(self.la_lexicon_pane, -1, "")
		self.cancel_button = wx.Button(self.la_lexicon_pane, wx.ID_CANCEL, "")
		self.apply_button = wx.Button(self.la_lexicon_pane, wx.ID_APPLY, "")
		self.la_flexion_pane = wx.Panel(self.la_notebook, -1)
		self.la_grammar_pane = wx.Panel(self.la_notebook, -1)
		self.la_translation_pane = wx.Panel(self.la_notebook, -1)

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
		self.Bind(wx.EVT_TEXT_ENTER, self.OnDoSearch, self.search_lemma)
		self.Bind(wx.EVT_LISTBOX, self.OnLemmaSelect, self.lemma_ctrl)
		self.Bind(wx.EVT_BUTTON, self.OnDoGenerateWords, self.generate_words_button)
		self.Bind(wx.EVT_BUTTON, self.OnDoNewWord, self.new_word_button)
		self.Bind(wx.EVT_BUTTON, self.OnDoDeleteWord, self.delete_word_button)
		self.Bind(wx.EVT_BUTTON, self.OnDoDeleteWord, self.xxx_button)
		self.Bind(wx.grid.EVT_GRID_CMD_SELECT_CELL, self.OnWordSelect, self.word_grid)
		self.Bind(wx.EVT_BUTTON, self.OnUndo, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnApply, self.apply_button)
		# end wxGlade

		# members
		self.code_behind = LACodeBehind(self)
		
		self.word_grid.SetColSize(1, 300)
		self.search_lemma.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnDoSearch, self.search_lemma)		

	def __set_properties(self):
		# begin wxGlade: LAFrame.__set_properties
		self.SetTitle("Lilac - Language Architect")
		self.SetSize((1068, 674))
		self.SetToolTipString("Lilac Language Architect")
		self.separator_ctrl.SetSelection(-1)
		self.capitalization_ctrl.SetSelection(0)
		self.generate_words_button.SetMinSize((25, 25))
		self.new_word_button.SetMinSize((25, 25))
		self.delete_word_button.SetMinSize((25, 25))
		self.xxx_button.SetMinSize((25, 25))
		self.word_grid.CreateGrid(0, 2)
		self.word_grid.SetRowLabelSize(0)
		self.word_grid.SetColLabelSize(0)
		self.word_grid.EnableEditing(0)
		self.word_grid.EnableDragRowSize(0)
		self.word_grid.EnableDragGridSize(0)
		self.word_grid.SetSelectionMode(wx.grid.Grid.wxGridSelectRows)
		self.word_grid.SetColLabelValue(0, "Categories")
		self.word_grid.SetColLabelValue(1, "Form")
		self.apply_button.Enable(False)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: LAFrame.__do_layout
		la_frame_sizer = wx.BoxSizer(wx.VERTICAL)
		la_lexicon_sizer = wx.BoxSizer(wx.HORIZONTAL)
		lemma_sizer = wx.FlexGridSizer(3, 1, 0, 0)
		lemma_button_sizer = wx.GridSizer(1, 2, 0, 0)
		word_panel = wx.StaticBoxSizer(self.word_panel_staticbox, wx.HORIZONTAL)
		word_field_sizer = wx.FlexGridSizer(2, 2, 5, 0)
		word_list_sizer = wx.FlexGridSizer(2, 1, 0, 0)
		word_list_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		lemma_field_sizer = wx.FlexGridSizer(4, 2, 5, 0)
		entry_form_sizer = wx.BoxSizer(wx.HORIZONTAL)
		lemma_list_sizer = wx.FlexGridSizer(2, 1, 0, 0)
		lemma_search_sizer = wx.BoxSizer(wx.HORIZONTAL)
		language_sizer = wx.GridSizer(1, 2, 0, 10)
		language_sizer_left = wx.BoxSizer(wx.VERTICAL)
		language_sizer_3 = wx.StaticBoxSizer(self.language_sizer_3_staticbox, wx.HORIZONTAL)
		language_grid_sizer_3 = wx.FlexGridSizer(3, 4, 2, 5)
		language_sizer_2 = wx.StaticBoxSizer(self.language_sizer_2_staticbox, wx.HORIZONTAL)
		language_grid_sizer_2 = wx.FlexGridSizer(2, 4, 2, 5)
		language_sizer_1 = wx.StaticBoxSizer(self.language_sizer_1_staticbox, wx.HORIZONTAL)
		language_grid_sizer_1 = wx.FlexGridSizer(3, 4, 2, 5)
		language_grid_sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_1.Add(self.code_ctrl, 0, wx.EXPAND, 0)
		language_grid_sizer_1.Add(self.label_4, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_1.Add(self.text_ctrl_4, 0, wx.EXPAND, 0)
		language_grid_sizer_1.Add(self.label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_1.Add(self.name_ctrl, 0, wx.EXPAND, 0)
		language_grid_sizer_1.Add(self.label_5, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_1.Add(self.text_ctrl_5, 0, wx.EXPAND, 0)
		language_grid_sizer_1.Add(self.label_3, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_1.Add(self.english_ctrl, 0, wx.EXPAND, 0)
		language_grid_sizer_1.Add(self.label_6, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_1.Add(self.text_ctrl_6, 0, wx.EXPAND, 0)
		language_grid_sizer_1.AddGrowableCol(1)
		language_grid_sizer_1.AddGrowableCol(3)
		language_sizer_1.Add(language_grid_sizer_1, 1, wx.EXPAND, 0)
		language_sizer_left.Add(language_sizer_1, 1, wx.EXPAND, 0)
		language_grid_sizer_2.Add(self.label_11, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_2.Add(self.separator_ctrl, 0, wx.EXPAND, 0)
		language_grid_sizer_2.Add(self.label_13, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_2.Add(self.text_ctrl_13, 0, wx.EXPAND, 0)
		language_grid_sizer_2.Add(self.label_12, 0, 0, 0)
		language_grid_sizer_2.Add(self.capitalization_ctrl, 0, wx.EXPAND, 0)
		language_grid_sizer_2.Add(self.label_14, 0, 0, 0)
		language_grid_sizer_2.Add(self.text_ctrl_14, 0, wx.SHAPED, 0)
		language_grid_sizer_2.AddGrowableCol(1)
		language_grid_sizer_2.AddGrowableCol(3)
		language_sizer_2.Add(language_grid_sizer_2, 1, wx.EXPAND, 0)
		language_sizer_left.Add(language_sizer_2, 1, wx.EXPAND, 0)
		language_grid_sizer_3.Add(self.label_21, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_3.Add(self.text_ctrl_21, 0, wx.EXPAND, 0)
		language_grid_sizer_3.Add(self.label_24, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_3.Add(self.text_ctrl_24, 0, wx.EXPAND, 0)
		language_grid_sizer_3.Add(self.label_22, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_3.Add(self.text_ctrl_22, 0, wx.EXPAND, 0)
		language_grid_sizer_3.Add(self.label_25, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_3.Add(self.text_ctrl_25, 0, wx.EXPAND, 0)
		language_grid_sizer_3.Add(self.label_23, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_3.Add(self.text_ctrl_23, 0, wx.EXPAND, 0)
		language_grid_sizer_3.Add(self.label_26, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		language_grid_sizer_3.Add(self.text_ctrl_26, 0, wx.EXPAND, 0)
		language_grid_sizer_3.AddGrowableCol(1)
		language_grid_sizer_3.AddGrowableCol(3)
		language_sizer_3.Add(language_grid_sizer_3, 1, wx.EXPAND, 0)
		language_sizer_left.Add(language_sizer_3, 1, wx.EXPAND, 0)
		language_sizer.Add(language_sizer_left, 1, wx.EXPAND, 0)
		language_sizer.Add(self.language_sizer_right, 1, wx.EXPAND, 0)
		self.la_language_pane.SetSizer(language_sizer)
		lemma_search_sizer.Add(self.search_lemma, 3, wx.EXPAND, 0)
		lemma_search_sizer.Add(self.clear_search_button, 1, 0, 0)
		lemma_list_sizer.Add(lemma_search_sizer, 1, wx.EXPAND, 0)
		lemma_list_sizer.Add(self.lemma_ctrl, 1, wx.EXPAND, 0)
		lemma_list_sizer.AddGrowableRow(1)
		la_lexicon_sizer.Add(lemma_list_sizer, 1, wx.EXPAND, 0)
		lemma_field_sizer.Add(self.entry_form_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		entry_form_sizer.Add(self.entry_form_ctrl, 4, 0, 0)
		entry_form_sizer.Add(self.entry_id_spin, 0, wx.EXPAND, 0)
		lemma_field_sizer.Add(entry_form_sizer, 1, wx.EXPAND, 0)
		lemma_field_sizer.Add(self.pos_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		lemma_field_sizer.Add(self.pos_ctrl, 0, 0, 0)
		lemma_field_sizer.Add(self.lemma_categories_label, 0, 0, 0)
		lemma_field_sizer.Add(self.lemma_category_ctrl, 0, 0, 0)
		lemma_field_sizer.Add(self.gloss_label, 0, 0, 0)
		lemma_field_sizer.Add(self.gloss_ctrl, 0, wx.EXPAND, 0)
		lemma_field_sizer.AddGrowableCol(1)
		lemma_sizer.Add(lemma_field_sizer, 1, wx.ALL|wx.EXPAND, 5)
		word_list_button_sizer.Add(self.generate_words_button, 0, 0, 0)
		word_list_button_sizer.Add(self.new_word_button, 0, 0, 0)
		word_list_button_sizer.Add(self.delete_word_button, 0, 0, 0)
		word_list_button_sizer.Add(self.xxx_button, 0, 0, 0)
		word_list_sizer.Add(word_list_button_sizer, 1, wx.EXPAND, 0)
		word_list_sizer.Add(self.word_grid, 0, wx.EXPAND, 0)
		word_list_sizer.AddGrowableRow(1)
		word_list_sizer.AddGrowableCol(0)
		word_panel.Add(word_list_sizer, 2, wx.EXPAND, 0)
		word_field_sizer.Add(self.word_category_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		word_field_sizer.Add(self.word_category_ctrl, 0, 0, 0)
		word_field_sizer.Add(self.form_label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
		word_field_sizer.Add(self.form_ctrl, 0, wx.EXPAND, 0)
		word_field_sizer.AddGrowableCol(1)
		word_panel.Add(word_field_sizer, 1, wx.ALL|wx.EXPAND, 5)
		lemma_sizer.Add(word_panel, 1, wx.EXPAND, 0)
		lemma_button_sizer.Add(self.cancel_button, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 20)
		lemma_button_sizer.Add(self.apply_button, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER_HORIZONTAL, 0)
		lemma_sizer.Add(lemma_button_sizer, 1, wx.ALL|wx.EXPAND, 20)
		lemma_sizer.AddGrowableRow(1)
		lemma_sizer.AddGrowableCol(0)
		la_lexicon_sizer.Add(lemma_sizer, 3, wx.EXPAND, 0)
		self.la_lexicon_pane.SetSizer(la_lexicon_sizer)
		self.la_notebook.AddPage(self.la_language_pane, "Language")
		self.la_notebook.AddPage(self.la_lexicon_pane, "Lexicon")
		self.la_notebook.AddPage(self.la_flexion_pane, "Flexion")
		self.la_notebook.AddPage(self.la_grammar_pane, "Grammar")
		self.la_notebook.AddPage(self.la_translation_pane, "Translation")
		la_frame_sizer.Add(self.la_notebook, 1, wx.EXPAND, 0)
		self.SetSizer(la_frame_sizer)
		self.Layout()
		# end wxGlade


	def OnOpen(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnOpen(event)

	def OnSave(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnSave(event)

	def OnSaveAs(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnSaveAs(event)

	def OnExit(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnExit(event)

	def OnUndo(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behindOnUndo(event)

	def OnRedo(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnRedo(event)

	def OnSelectAll(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnSelectAll(event)

	def OnCut(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnCut(event)

	def OnCopy(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnCopy(event)

	def OnPaste(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnPaste(event)

	def OnClear(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnClear(event)

	def OnOverview(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnOverview(event)

	def OnRunConceptBrowser(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.show_child(CBFrame)

	def OnRunFilterEditor(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRunFilterEditor' not implemented!"
		event.Skip()

	def OnRunLanguageReader(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRunLectReader' not implemented!"
		event.Skip()

	def OnRunBilingualInterpreter(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnRunBilingualInterpreter' not implemented"
		event.Skip()

	def OnAbout(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnAbout(event)

	def OnLemmaSelect(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnLemmaSelect(event)

	def OnDoSearch(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnDoSearch(event)

	def OnDoNewLemma(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnDoNewLemma(event)

	def OnDoDeleteLemma(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnDoDeleteLemma(event)

	def OnWordSelect(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnWordSelect(event)

	def OnDoNewWord(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnDoNewWord(event)

	def OnDoDeleteWord(self, event): # wxGlade: LAFrame.<event_handler>
		self.code_behind.OnDoDeleteWord(event)

	def OnCancel(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnCancel' not implemented"
		event.Skip()
		
	def OnApply(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnApply' not implemented"
		event.Skip()

	def OnDoGenerateWords(self, event): # wxGlade: LAFrame.<event_handler>
		print "Event handler `OnDoGenerateWords' not implemented"
		event.Skip()

# end of class LAFrame

class CBFrame(wx.Frame):

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
		self.export_menu = wx.MenuItem(self.file_menu, wx.ID_ANY, "E&xport", "", wx.ITEM_NORMAL)
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
		self.pos_ctrl = wx.ComboBox(self.panel_1, -1, choices=[], style=wx.CB_DROPDOWN|wx.CB_READONLY)
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
		self.Bind(wx.EVT_TEXT, self.OnChange, self.pos_ctrl)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.arg_struct_combo)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.meaning_text)
		self.Bind(wx.EVT_TEXT, self.OnChange, self.reference_text)
		self.Bind(wx.EVT_BUTTON, self.OnUndo, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnApply, self.ok_button)
		# end wxGlade

		self.concept_tree_ctrl.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)


	def __set_properties(self):
		# begin wxGlade: CBFrame.__set_properties
		self.SetTitle("Concept browser")
		self.SetSize((850, 420))
		self.concept_tree_ctrl.SetMinSize((500,400))
		self.ok_button.Enable(False)
		self.ok_button.SetDefault()
		self.panel_1.SetMinSize((300,400))
		# end wxGlade
		self.code_behind = CBCodeBehind(self)

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
		control_grid_sizer.Add(self.pos_ctrl, 0, wx.ALIGN_CENTER_VERTICAL, 0)
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

	#Tree events
	def OnRightUp(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnRightUp(event)

	def OnSelChanged(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnSelChanged(event)

	#Control events
	def OnChange(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnChange(event)


	#Menu events
	def OnReload(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnReload(event)

	def OnSave(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnSave(event)


	def OnExport(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnExport(event)


	def OnExit(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnExit(event)

	def OnFind(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnFind(event)

	def OnUndo(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnUndo(event)

	def OnApply(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnOpen(event)


	def OnNew(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnNew(event)


	def OnDelete(self, event): # wxGlade: CBFrame.<event_handler>
		self.code_behind.OnDelete(event)
		
		
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

		self.Bind(wx.EVT_TEXT, self.OnText, self.value_text)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.cancel_button)
		self.Bind(wx.EVT_BUTTON, self.OnFind, self.ok_button)
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


	def OnCancel(self, event): # wxGlade: FindDialog.<event_handler>
		self.EndModal(wx.ID_CANCEL)

	def OnFind(self, event): # wxGlade: FindDialog.<event_handler>
		self.EndModal(wx.ID_OK)

	def OnText(self, event): # wxGlade: FindDialog.<event_handler>
		self.ok_button.Enable(True)

# end of class FindDialog


class LAApp(wx.App):
	def OnInit(self):
		wx.InitAllImageHandlers()
		la_frame = LAFrame(None, -1, "Linguistic Laboratory")
		self.SetTopWindow(la_frame)
		la_frame.Show()
		return 1

# end of class LAApp

