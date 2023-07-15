import wx
import pandas as pd
import requests
from io import BytesIO
from PIL import Image

class MyPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.list_ctrl = list_ctrl = wx.ListCtrl(
            self,
            size=(-1,-1),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        list_ctrl.InsertColumn(0, 'Image/Search Date')
        list_ctrl.InsertColumn(1, 'ASIN')
        list_ctrl.InsertColumn(2, 'Name')
        list_ctrl.InsertColumn(3, 'Price')
        list_ctrl.InsertColumn(4, 'Rating')
        list_ctrl.InsertColumn(5, 'Amazon Prime')
        list_ctrl.InsertColumn(6, 'Sale')
        list_ctrl.InsertColumn(7, 'Brand')
        list_ctrl.InsertColumn(8, 'URL')

        df = pd.read_csv('amazon_products.csv')

        self.img_list = wx.ImageList(100, 100)

        for index, row in df.iterrows():
            response = requests.get(row['Image'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((100, 100), Image.LANCZOS)
            img_wx = pil_to_wx(img)  # Convert PIL.Image to wx.Bitmap
            img_index = self.img_list.Add(img_wx)
            list_ctrl.InsertItem(index, row['Search Date'])
            list_ctrl.SetItem(index, 1, row['ASIN'])
            list_ctrl.SetItem(index, 2, row['Name'])
            list_ctrl.SetItem(index, 3, str(row['Price']))
            list_ctrl.SetItem(index, 4, str(row['Rating']))
            list_ctrl.SetItem(index, 5, str(row['Amazon Prime']))
            list_ctrl.SetItem(index, 6, str(row['Sale']))
            list_ctrl.SetItem(index, 7, str(row['Brand']))
            list_ctrl.SetItem(index, 8, row['URL'])
            list_ctrl.SetItemImage(index, img_index)

        list_ctrl.SetImageList(self.img_list, wx.IMAGE_LIST_SMALL)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 1, wx.EXPAND)
        self.SetSizer(sizer)

# Function to convert PIL.Image to wx.Bitmap
def pil_to_wx(image):
    width, height = image.size
    buffer = image.convert('RGBA').tobytes()
    bitmap = wx.Bitmap.FromBufferRGBA(width, height, buffer)
    return bitmap

class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="wxPython ListCtrl Tutorial", size=(800,600))
        panel = MyPanel(frame)
        frame.Show()
        return True

app = MyApp()
app.MainLoop()
