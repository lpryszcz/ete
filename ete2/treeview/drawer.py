from ete_dev import Tree, PhyloTree, ClusterTree

# I currently use qt4 for both rendering and gui
from PyQt4  import QtGui
from qt4gui import _MainApp, _PropertiesDialog
from qt4render import _TreeScene

__all__ = ["show_tree", "render_tree", "TreeImageProperties"]

_QApp = None

class TreeImageProperties(object):
    def __init__(self):
        self.force_topology             = False
        self.tree_width                 = 200  # This is used to scale
                                               # the tree branches
        self.draw_aligned_faces_as_grid = True
        self.draw_guide_lines_to_aligned = False
        self.draw_image_border = False
        self.complete_branch_lines = True
        self.extra_branch_line_color = "#0000ff"
        self.show_legend = True
        self.min_branch_separation = 1 # pixels
        self.search_node_bg = "#cccccc"
        self.search_node_fg = "#ff0000"
        self.aligned_face_header = FaceHeader()
        self.aligned_face_foot = FaceHeader()
        self.title = None
        self.botton_line_text = None


class FaceHeader(dict):
    def add_face_to_aligned_column(self, column, face):
        self.setdefault(int(column), []).append(face)


def show_tree(t, style=None, img_properties=None):
    """ Interactively shows a tree."""
    global _QApp

    if not style:
        if t.__class__ == PhyloTree:
            style = "phylogeny"
        elif t.__class__ == ClusterTree:
            style = "large"
        else:
            style = "basic"

    if not _QApp:
        _QApp = QtGui.QApplication(["ETE"])

    scene  = _TreeScene()
    mainapp = _MainApp(scene)

    if not img_properties:
        img_properties = TreeImageProperties()
    scene.initialize_tree_scene(t, style, \
                                    tree_properties=img_properties)
    scene.draw()

    mainapp.show()
    _QApp.exec_()

def render_tree(t, imgName, w=None, h=None, style=None, \
                    img_properties = None, header=None):
    """ Render tree image into a PNG file."""

    if not style:
        if t.__class__ == PhyloTree:
            style = "phylogeny"
        elif t.__class__ == ClusterTree:
            style = "large"
        else:
            style = "basic"


    global _QApp
    if not _QApp:
        _QApp = QtGui.QApplication(["ETE"])

    scene  = _TreeScene()
    if not img_properties:
        img_properties = TreeImageProperties()
    scene.initialize_tree_scene(t, style,
                                tree_properties=img_properties)
    scene.draw()
    scene.save(imgName, w=w, h=h, header=header)
