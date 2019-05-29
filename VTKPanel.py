import wx
import vtk
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor

class VTKPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        #to interact with the scene using the mouse use an instance of vtkRenderWindowInteractor.
        self.widget = wxVTKRenderWindowInteractor(self, -1)
        self.widget.Enable(1)
        self.widget.AddObserver("ExitEvent", lambda o,e,f=self: f.Close())
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.widget, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()
        self.ren = vtk.vtkRenderer()
        self.filename=""
        self.isploted = False
        self.xObject = 0
        self.yObject = 0
        self.zObject = 0

    def renderthis(self, filename):
        # open a window and create a renderer
        self.widget.GetRenderWindow().AddRenderer(self.ren)
        # file to open
        self.filename = filename
        # render the data
        reader = vtk.vtkSTLReader()
        reader.SetFileName(self.filename)

        # To take the polygonal data from the vtkConeSource and
        # create a rendering for the renderer.
        coneMapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            coneMapper.SetInput(reader.GetOutput())
        else:
            coneMapper.SetInputConnection(reader.GetOutputPort())

        # create an actor for our scene
        if self.isploted:
            coneActor=self.ren.GetActors().GetLastActor()
            self.ren.RemoveActor(coneActor)

        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        # Add actor
        self.ren.AddActor(coneActor)
        # print self.ren.GetActors().GetNumberOfItems()

        if not self.isploted:
            axes = vtk.vtkAxesActor()
            self.marker = vtk.vtkOrientationMarkerWidget()
            self.marker.SetInteractor( self.widget._Iren )
            self.marker.SetOrientationMarker( axes )
            self.marker.SetViewport(0.75,0,1,0.25)
            self.marker.SetEnabled(1)

        self.ren.ResetCamera()
        self.ren.ResetCameraClippingRange()
        cam = self.ren.GetActiveCamera()
        cam.Elevation(10)
        cam.Azimuth(70)
        self.isploted = True

        # Calculate object sizer
        minx = maxx = miny = maxy = minz = maxz = None
        points = reader.GetOutput()
        for pointId in range(points.GetNumberOfPoints()):
            p = points.GetPoint(pointId)
            # p contains (x, y, z)
            if minx is None:
                minx = p[0]
                maxx = p[0]
                miny = p[1]
                maxy = p[1]
                minz = p[2]
                maxz = p[2]
            else:
                maxx = max(p[0], maxx)
                minx = min(p[0], minx)
                maxy = max(p[1], maxy)
                miny = min(p[1], miny)
                maxz = max(p[2], maxz)
                minz = min(p[2], minz)

        self.xObject = maxx - minx
        self.yObject = maxy - miny
        self.zObject = maxz - minz

        # Enable user interface interactor
        self.widget.Initialize()
        self.ren.Render()
        self.widget.Start()

    def getObjectSize(self):
        return self.xObject, self.yObject, self.zObject
