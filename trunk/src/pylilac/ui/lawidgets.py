#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A module for the wx widgets used in the Language Architect.


@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.5
"""

__docformat__ = "epytext en"

import wx
import wx.combo

# begin wxGlade: extracode
# end wxGlade


class StockBitmapButton(wx.BitmapButton):
	def __init__(self, parent, id = wx.ID_ANY, label=u""):
		bitmap = wx.ArtProvider.GetBitmap(label, wx.ART_TOOLBAR, (16,16))
		wx.BitmapButton.__init__(self, parent, id, bitmap)

class CategoryPanelComboCtrl(wx.combo.ComboCtrl):
	class PanelComboPopup(wx.combo.ComboPopup):

		# overridden ComboPopup methods
		def __init__(self, labels):
			wx.combo.ComboPopup.__init__(self)
			self.__rows = len(labels)
			self.__labels = labels

		def Init(self):
			self.value = None
			self.curitem = None


		def Create(self, parent):
			panel = wx.Panel(parent, wx.ID_ANY, style = wx.TAB_TRAVERSAL|wx.RAISED_BORDER)
			self.panel = panel
			self.labels = [wx.StaticText(panel, -1, lbl.replace("_"," ").replace("-"," ").capitalize() + ":") for lbl in self.__labels]
			self.text_ctrls = [wx.TextCtrl(panel, -1, "") for lbl in self.__labels]
			self.button_area = wx.Panel(panel, -1)
			self.ok_button = wx.Button(panel, -1, "OK")

			self.__set_properties()
			self.__do_layout()

			panel.Bind(wx.EVT_BUTTON, self.OnOkButton, self.ok_button)


		def GetControl(self):
			return self.panel

		def GetStringValue(self):
			if self.value:
				return self.value
			else:
				return " ".join(self.__get_popup_values())

		def SetStringValue(self, value):
			self.value = value
			self.__set_popup_values(value.split(" "))

		def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
			if self.__rows == 0:
				w, h = minWidth, min(55, maxHeight)
			else:
				max_len = reduce(max, map(len, self.__labels))
				w, h = max(max_len*9+55, minWidth), min(self.__rows*30+25, maxHeight)
			return wx.Size(w, h)


		def __set_properties(self):
			self.ok_button.SetMinSize((23, 23))
			for r in range(self.__rows):
				ps = self.labels[r].GetFont().GetPointSize()
				self.labels[r].SetFont(wx.Font(ps, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

		def __do_layout(self):
			category_sizer = wx.FlexGridSizer(2, 1, 0, 0)
			button_sizer = wx.FlexGridSizer(1, 3, 0, 0)
			ctrl_sizer = wx.BoxSizer(wx.VERTICAL)

			if self.__rows == 0:
				caption = wx.StaticText(self.panel, -1, "No categories associated.")
				caption.SetFont(wx.Font(8, wx.FONTFAMILY_SWISS, wx.ITALIC, wx.NORMAL, 0, ""))
				ctrl_sizer.Add(caption, 1, wx.EXPAND, 0)
			for r in range(self.__rows):
				sizer = wx.BoxSizer(wx.HORIZONTAL)
				sizer.Add(self.labels[r], 3, wx.LEFT|wx.ALIGN_CENTER_VERTICAL, 2)
				sizer.Add(self.text_ctrls[r], 2, wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 2)
				ctrl_sizer.Add(sizer, 1, wx.EXPAND, 0)


			category_sizer.Add(ctrl_sizer, 1, wx.EXPAND, 0)

			button_sizer.Add(self.button_area, 1, wx.EXPAND, 0)
			button_sizer.Add(self.ok_button, 0, 0, 0)
			button_sizer.AddGrowableCol(0)

			category_sizer.Add(button_sizer, 1, wx.EXPAND, 0)

			self.panel.SetSizer(category_sizer)
			category_sizer.Fit(self.panel)
			category_sizer.AddGrowableRow(0)
			category_sizer.AddGrowableCol(0)


		def __set_popup_values(self, values):
			for i, s in enumerate(values):
				if i == self.__rows: break
				self.text_ctrls[i].SetValue(s)

		def __get_popup_values(self):
			vs = []
			for v in self.text_ctrls:
				s = v.GetValue()
				if s == "":
					vs.append("0")
				else:
					vs.append(s)
			return tuple(vs)


		def OnOkButton(self, event):
			self.curitem = self.__get_popup_values()
			self.value = " ".join(self.curitem)
			self.Dismiss()
			event.Skip()

	# overridden ComboCtrl methods
	def __init__(self, parent, id = wx.ID_ANY, choices = [], style = 0):
		wx.combo.ComboCtrl.__init__(self, parent, id, style = style)
		self.__panel = self.PanelComboPopup(choices)
		self.SetPopupControl(self.__panel)
	def SetSelection(self, n):
		if n == -1:
			self.__panel.SetStringValue("")
	def SetCategoryLabels(self, labels):
		self.__panel = self.PanelComboPopup(labels)
		self.SetPopupControl(self.__panel)
	def SetCategoryValues(self, values):
		value = " ".join(values)
		self.SetValue(value)
	def GetCategoryValues(self):
		value = self.GetValue()
		return tuple(value.split(" "))


class TestFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: TestFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.sizer_2_staticbox = wx.StaticBox(self, -1, "Test")
		self.combo_box_1 = wx.ComboBox(self, -1, choices = [], style = wx.CB_DROPDOWN)
		self.combo_box_2 = CategoryPanelComboCtrl(self, -1, choices=["Case", "Number"], style = wx.CB_DROPDOWN)

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: TestFrame.__set_properties
		self.SetTitle("frame_1")
		self.combo_box_2.SetSelection(-1)
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: TestFrame.__do_layout
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.StaticBoxSizer(self.sizer_2_staticbox, wx.VERTICAL)
		sizer_2.Add(self.combo_box_1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_2.Add(self.combo_box_2, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
		sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		self.Layout()
		# end wxGlade

# end of class TestFrame


if __name__ == "__main__":
	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	frame_1 = TestFrame(None, -1, "")
	app.SetTopWindow(frame_1)
	frame_1.Show()
	app.MainLoop()
