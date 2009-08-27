# -*- coding: utf-8 -*-

"""
A module to wrap the images used in wx graphical interface.

@author: Paolo Olmino
@license: U{GNU GPL GNU General Public License<http://www.gnu.org/licenses/gpl.html>}
@version: Alpha 0.1.5
"""

__docformat__ = "epytext en"

from wx import ImageFromStream, BitmapFromImage, EmptyIcon, ART_OTHER
import cStringIO

class ArtProvider(object):
	"""
	A factory for the graphical resources.
	
	Images can be estracted as bitmaps or icons.
	"""
	__data = {('lilac', ART_OTHER, (16,16)): \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01rIDAT8\x8d\x8d\x93\xb1K\xc3@\x14\x87\xbf(\xc2e\x08\xa4\xe0\x90\x80 \
\x19*\xd4\xc9\x1b;t\xe9\xe0\xd6\xa5C\xd1n\xf5O\x10\x04\xa1\x8bC;\t\x8e\x8e\
\xdd\xecP\xc1\xc5\xdd\xc5\xa1c\x85\x8a\x1d\x04\x95*\x9aAH\xc0\xa17\x14\xce\
\xa1\\\xd0\x92\x84\xfe\xe0\x86\xe3\xde{\xf7~\x1f\xefYZk\xb2\xd4=\xeak\x80v\
\xafie\x06i\xadSO\xa7u\xa5\x9f\xc63\xfd2\x9e\xe9N\xebJg\xc5\xade\xfd\\\xaeI&\
\xf7#\x00\xca5\x99t\xb3\xac\xd4\x02\x7f\x15\xc7\x8a\xd7Q\x9c\xf9\x9eY\xc0$E?\
*\xf7\x03\xcb@\\jq\x0fx\x10\xae\x00@\xc5\n\xa0\x01\x0cL\x80\x01ki\xad\xe9\
\x1e\xf5\xb5\xb7\x15$\xd9\xe1\xc7+\x113\x14C\x04e\n\xd8\x00x[\x01\xd5\x86\
\x04\xa0\x7fqC\xbb\xd7\xb4\xd67\xa6;\xba\\\x93X\x96\xc2v\xc0v\xe0\xf9\xf3\
\x0b\xc5\x90\xfa\xa1`\xfc\xf8\xc6\x1c\x8f\x82\xeb\xe0o;\x84\xd3\x90p\x1a\xb2\
\x7fP\xe5\xf2tp\xb6\x06\x10\x14\x03J\x15\x89\xacH\xc4\xa6\xf7\xcfc\xfdP\xa0\
\xe6\x93\xe4\xeez.\xa5\x8a\xc4\x90I,4\x8f\xeb\x8b\xf6\xdfc\xee\xae\xef\x12\
\x0b\x00|K\xfc\xcd\x02\xc6f ]\x86\xb7#\xda\xbd\xa6\x95\x0b1b\x06`\x18\x9c\
\x00\xe7\xa9\x10\x97e\xa0\xda\xbe@\xa0\x88\xbe\x16`\xd3F:w\x90<O\xe4=\xe7\
\x17\x08\xa4\x8b_\\x\xde\x95^VX\xfe2\xbd\xac\xb0L\xa9\x0c\x8cVY\xe7_\x97\xd8\
\xea^+\xe0\x89\x12\x00\x00\x00\x00IEND\xaeB`\x82', \
('idea', ART_OTHER, (16,16)): \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x02\x12IDAT8\x8d\x8d\x91\xcbk\x13a\x14\xc5\xef\xbd\xdf\xe4\xd56\tmb\xd3\
4\xc4\x07\x81\xbap\x15\xf0\x01\xb6\x9a\x84.\x05\x05\xdd\xba*.\xf4Op\xd5\xb4\
\xfe\x03.\\kAAA7nt\xd1E\x92\x82\x0f\x10Z|RK\xad!&1f\x9a\xa4\xc6q\x92\xce|\
\x0fW\xcaX\'\xea\xd9\xdd\xcb9?\xee\xe5 \x0c\xd0\xbb\xc2\xa5\xbc\xddhH?G\xa5\
\x8d\x851u\xe6\xce\xa2\x9b\x0f\xf7.Vn\x9d\xc8$\xc3\x91e\xff\xfe4\x1f\x1d= \
\xc9\xd3!\xa3\xbe\xce\xaa\x8dM\xe6k\xef\xcc\x1e\x9e{]\x1a\x08xro&;\x19\xa0\
\xe5x\xe6j\x1f)F\xd2\xb2\x98F:\xa2\xf5R(\xfd-\xfb\\\xde`\xad*\xcd\xa6\xaf\
\xbc\xf8\x05!\' \x00\x9d\xf9\xe8\xa1\x84\x14\xbdM\x02sUy\xb1\xcc\xd1\xac\xa1\
2\xac\x00\x80I\xd18*;\xa4\xe6\x9d\x19\xcd9\x04q(\xeb\x83\xa6\xe0\xadg\x0cG\
\xc6\x95\xec\x0eq\x90R\x81h\x81\x92\x025\x8fW\x05\xbd<\xe7\xcc\xfcvAS\x8a\
\xa2\xe0&\x82lQW/3\xe0[\xa4\xac\x0f\xc0{5\x00*\x13\xb7;H \x8b\x03\x01f?\xb2\
\xf0U\xaf\x93&\xebjwg\x03\xa5]c\xc2\xfe\xc8v\x8d:\x80\x10\xaa\xd3\x16dwp\xc1\
\x99a\xce\xe1\xf6\xc3\xad\xf2\xc5\xb3)\xf4k\xed\xacP\xdf\x81\x84"K\xf4Pj\x12\
\xa5@\xb5^\xe1\xd7\x8e\xcd\xbdY\x1a\xd8\xc2O\xbd\xba?SH\x8eW3\xc84\x94\xa8$\
\xa2\r\xba\x1e]\x99:\xb7\x9a\xdb\xeb%7@\xdf\x0e\x94\x94%\xd0\x16\x0cl.P*"o\
\xect\xc9\xcd\xab\xb9-\x1f=\xcf\xc1\xf4\x11\x01\xfb\xa2\x15 6\x81\x9f*IX\xdb\
\x9er\xb3\xba\x03\xde\xf7\x0f\xc2\x97\xb5\xcb`\x19\x02Bc\xc3\xe0!\x0b\xda\
\xc67W\x80\xeb\x0b\xa1\x9e\t\xcc7\x02\xf1\xc40\x04|\x00\x82k\x00\xb6\xef\xff\
\x01\xe1x\x04&b\x93p\xf4d\x1aR\xa9$\xf4,\x1b\x12\xa9\xa8+\xc0\xb5\x05\x00\
\x80\xeb7\x1e\x17\xba\xcd`\xd64\xb6\xe1\xf8t\xa4x\xfe\xc2\xa9?\x1a\xf8\xa7\
\x96n>\xcd?\xb8[\xcc\xff\xcd\xf3\x03\x9a\x01\xe7\x83Zzj\x89\x00\x00\x00\x00I\
END\xaeB`\x82', \
('action', ART_OTHER, (16,16)): \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x02`IDAT8\x8d\x8d\x92]HSa\x1c\xc6\x9f\xb3\x0f\xd7\x9c\x9b\xce\x8d\xc5\
\xca\xd0U\x9b\x9aIR\xd9\x97\x85gn\x8a\x94\xa36\x12\xc2h\x89\x11\xd6M\xe0E ^X\
!#\x82\xa2\x8b\xa4\x82 \xa2\x82"\xa8\xbc0\x91\x92\xce\x91\xd5\x85d\x81f\x13\
\x8f\xce\x0f\x18\xea4\xb7\xd8\xf7\xce>NW\x81ks\xf5\xdc\xbd\xbc\xfc~\xef\xf3\
\xbe\xff\x17\xf8\x8f4\xd6\x9b)C\xad\x89\xca\xb4\xc7\xfb\x17\xdc\xd5u\x93b\
\x93I\xf2\x97/H\x9a\x9b\xda\xd3$\xfcl\xb0\xe5d+u\xa5\xf3*\xa9\xd9S\x03AB\x01\
\xa1P^R\xbcUIL2ct\xd6S-&+\xd9{\xff9w\xae\xa5\x9bk2]\xe2\xde\x8f\xba\xb8\xaf\
\xe3N\xee\xcc\xe9\x8e\xb4\x06D&x\xa7\xee\x10\xd5`\xae\x85\x8f%0\xf8\xf2\rX\
\x16\x10\xf2\xbc\xf4\xa3\xc7w\xf4Y\xaf`1Y\xc9\x96\xb6\x8b\xd4\x94\xc3\x8d\
\xbe\xd7\xcf`<\xd1\x88\xcdr!\xbe\x8d\x0c\xeb\xbd~bX\xab\xadn\xd5j\xab1==:\
\x9f\xb1\xc1\x85\xd6\x1e\xae\xbe\xd9\x80\xe2\xed\xa5\xb8g\xbb\x066\xc0"\x1a\
\xe3h>_L\x1e\xa9;\x88\xba\xe3F\xdc\xea\xeeA\xd0\x97\xd0\x0f\x0c<\xa0\x81\xbf\
\xa6\xb0\xba\xe2\xc1\xed\xeb\x9d\xf0\xaf-\xa1LW\x81\xf2\xd2\x06\xd8\xee\xda\
\xc8S\xd6\xb3\x18\xea\xef\x83J&B4\x18\x07\x00\xf2\x0f\x93"XYe\x10\tD\xf0\xb4\
\xf7\x05\x9a\xdb\xcec\x82\x19\x043\xf1\x05Ksc8px?\x1c\xb3nH%y)o\x90"\xd8\xa2\
\xae\x80h\x93\x18\x91\x98\x13\xd1\x90\x17s\x0b\xdfQ^\xb5\x0f\xce\x19\x06\xcb\
\x8b\x8b\xf84H\xe1\x18i\xd8X\x10cc \x08\x11H\xa3\x114m\xc76\xb5\x1a\x1d\xed\
\x97Q \xc9\x85k\xc1\x85\x1a\x15\x87\x12q2E X\xbf\x08G\xd6PX\x98\x8f\xa1w\xfd\
\xd0hv@\xa7\xd5A\xae(\x82\xc7\xf3\x13eeG\x91#V /_\xb4\xb1 \x10\\C \xb0\x84\
\xca\xca]Xv\xaf\x82\x83\x08\x8b\xae(\xa42%$\x12)\xc6=\n\xcc\x8e\xcc\xa5\x08R\
\xc6\xb8\xb7J\xcf\xc9\xa4"\x08\x849\xe0\xf1\x04P)\x8b\xc0\xe3\x89\x11\nE\xe1\
\xf3\x05\xe1\xf1\xce\xde\x08\xb1\xdc\xbc\xe3\xc7\xc7\'\x19\x1b$\xe2,\x9d\x8c\
\x83\xcc\x95\x15\xc0\xef\x8f\x81\x99a\x10\x0e\x07{\xd9x\xd2>5\xf5\xf9\x152$\
\xed+\xef.\xafy\x08\x82H&8\xe2\xc3\xe4\xa4\xfdm&h}~\x03\x96|\xe9R\x9dL&\x92\
\x00\x00\x00\x00IEND\xaeB`\x82', \
('label', ART_OTHER, (16,16)): \
"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01PIDAT8\x8d\xcd\x93?K\x82Q\x14\x87\x9fs\xb9Je\xa5\x8bCCA\xa3%\x19\x0e\
-\x91\x92e\xd0\xd8\xe2\x18-}\x0e\t\x8a\xbeD\x83H\x8b\x0eNQXddS\x8b$h\xd2R[\
\x8bE\xe2\x10e\x7fn\x83\xefkI&\x81C\x1d\xb8\xdc\xc3\x81\xdfs~\xe7\x1e\xae\
\x18c\xe8%TO\xea\x7f\x01\xd0\x00\xe9-\t\xf9\x83\xd1S\xbb8\xb1|(\xb2\xb8>5\
\xb9\xbaQ\xec&.'\xe3\x01Im\xd2\x12\x97\nGa;\x8fU\x13\xcc\xce\x0c\xd1\xe8\x13\
\xfa\x95\xa0\x95\x00\xe0n^\xb8\xb5\x90\xc8> \xe5\xfd\xa8\xb1\xbb\x02\xf8\x93\
\xb7&\xed]\x03 \xee\xcb\xe0\xb5\xc4og\xedfF#Av\xb3\xf7\xcd\x11\xec\xb0l\x13\
\xf7e\x00\x18\xd1\n-\xc2\xab1\x8cG\xa6qZ\x1b\x7fQ\n\x87\xe5D\x95\nGa\x80\xcb\
\x83%\x93\x9a\xdf\xf1\x00T\xf2\xf5\x16\xd4\x85a\xcc!\xdc\xe4.\xb8:i\x9e\xeb\
\xe3\x02\x03\xd6Hb\x8ci{\xc4X5\x81/4L%_ge\xc1\x83K+4\x06\xa7\x01\x87V8E\xa1\
\xc5\xa0\x81\xed\xbd\xbb&\xa0\xc3\x18\xc5H\xc4C.W\xeb\xb6\x84O\x07\xdf\x8a\
\x16$87\xc8\xe3\xf3;Z\x14J\tZ\x04\x11\xe1I\t\xe5\x06p^\xeb\x0c\xf8\n\xe9\xd6\
\xbd\x9c\x8c\x07~\x04\xfc6\xfe\xfe/|\x00\rNv\x98\xc4\xcf\x80\xb9\x00\x00\x00\
\x00IEND\xaeB`\x82", \
('brackets', ART_OTHER, (16,16)): \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x00\xf1IDAT8\x8d\xc5\x921N\x02A\x18\x85\xbf\xcc\xc2\xc2.\x14\xba4XPX\
\x19\n\x1bh=\x03\xb1\xe0\x086&$\x96\x14\\\x01ZC\xc1\x01\xd6\xc6#XYSx\x00\xad\
\xb8\x02\t\x86\xe4\xd9\x0c\xcb\x9a\x99A)\x08\x7f5\xf3\xde\xff\xde\x9b\x7ff\
\xe0\x14\xa5(\x9a(\x8a\x1e\x8a}\x1c/\xd4n\xdf\xfdO\x9c$o\x02\xfd\xc2\xa0#\
\x90\xe0\xf1\xb0\xd8\x98\xa9m\xec;\x1c\xcc\x05R\xadv\xeb\x17\xefS\xe4\xe5+\
\x95\xa1\xe5_\xfc\x06i:\xb6\t\x1f\x81\x80\xfe.@\xd0\xdc\xe1\xa6\xe8X\xaf\xaf\
\x01\xd8l\xbe\x02\x13\xaeJ\xeb\x9ek\x00W\x01\xa1\xaf.|\x06\xdb#\x0c\xbe]\x83\
\xfd\xec\x97\x01Q\x19\x7fwX\xc1\xcd\xc1W\x80\x81\xbd\xe4e\xf0\\\xaaVsk\xd2u\
\xb88\x9e\t\xa4,\xbb\x0f\x1b@&\xf8\xf4\xfc\xc4\xa6@2\xe69(.5wT\xaf\xe7j4F\
\x05\xd6j\xbd\n\x9e\xfe\x14\x9f\xa5~\x00^\x01\\\xbff\xbb\x01\xf6\x00\x00\x00\
\x00IEND\xaeB`\x82',  \
('link', ART_OTHER, (16,16)): \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x00\xdcIDAT8\x8d\xedR\xbb\x0e\xc1`\x14\xfeN#5\xb11\x88\x89E\x1f\xa1f\
\xe9S\x98\xc4\x86\xc4\xfd)\x0c\x1e\xc0\x13\xd8\x84\xa55k#"HD-D\xa2\x84v\xc3\
\xa2\t\xbf\x89h\xda\xad\x9b8\xe3\xf9.\xe7J\x8c1\xf8\t\xce\x97\xfa7\x0c\x085>\
UkVuu\xdeu\x00\x9ab\x08\xacu_\x03\x00\xd5\x83\xa9b\xa3\xa0O\x17=\x17\x87\x8a\
\xa7\n\x9b-\xfax\xe2\xe9rW\xa5\r\x01@\xe9\\e\x93\xe1\x00\\\xf4\xe1\xc0Cf\x18\
T>d\xd8x\xb9uT,w,\xcf\xdb\xb6\xf3\x11zw$Jq=d\x86\x11\xb8\xe1\xe29\xdb\xee*{d\
\xb3\xee\x1d\x88r\xc2U\x8d\x0c\x1b\x000\xca\xed\t\x00\xd2J\x92E\xec\x18\x00\
\xc0\xe2\x8f\x0e\x0e\xa7)\x86\xe0\xd5\x81\xba2?yM1\x04\x8b?~\xc4\xdf\x1c\xfa\
\xbf\xb2\x7f\x83\x17D2Z\xd0\xb30\x9b\x9c\x00\x00\x00\x00IEND\xaeB`\x82' 
}

	@staticmethod
	def get_bitmap(id, client = ART_OTHER, size = (-1,-1)):
		"""
		Return a bitmap.
		@param id: The ID of the image.
		@type id: str
		@return: The image as a bitmap.
		@rtype: wx.Bitmap
		"""
		stream = cStringIO.StringIO(ArtProvider.__data[(id, client, size)])
		img = ImageFromStream(stream)
		return BitmapFromImage(img)

	@staticmethod
	def get_icon(id, client = ART_OTHER, size = (-1,-1)):
		"""
		Return an icon.
		@param id: The ID of the image.
		@type id: str
		@return: The image as an icon.
		@rtype: wx.Icon
		"""
		icon = EmptyIcon()
		icon.CopyFromBitmap(ArtProvider.get_bitmap(id, client, size))
		return icon

	@staticmethod
	def iter_keys():
		"""
		Return an iterator on images.
		@rtype: iterator of (ID, client, size)
		"""
		return ArtProvider.__data.iterkeys()