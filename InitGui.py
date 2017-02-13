
import FreeCAD as App

rev_number = int(App.Version()[2].replace("(Git)",""))
if rev_number >= 9933:
    import PartOMagic
    PartOMagic.importAll()
    if App.GuiUp:
        Gui.addModule("PartOMagic")
        PartOMagic.Gui.Observer.start()
else:
    App.Console.PrintError("Part-o-magic requires FreeCAD at least v0.17.9933. Yours appears to have a rev.{rev}, which is less. Part-o-magic is disabled.\n".format(rev= str(rev_number)))

# substitute TempoVis's isContainer with a more modern one
import Show.TempoVis 
Show.TempoVis = PartOMagic.Gui.TempoVis.TempoVis

class PartOMagicWorkbench (Workbench):
    MenuText = 'Part-o-magic'
    ToolTip = "Part-o-magic: experimental group and Part and Body automation"

    def __init__(self):
        # Hack: obtain path to POM by loading a dummy Py module
        import os
        import PartOMagic
        self.__class__.Icon = os.path.dirname(PartOMagic.__file__) + u"/Gui/PyResources/icons/PartOMagic.svg".replace("/", os.path.sep)

    def Initialize(self):
        import PartOMagic as POM
        POM.importAll()
        
        cmdsNewContainers = ([]
            + ["PartDesign_Part"]            
            + ["PartDesign_Body"]            
            + POM.Features.exportedCommands()
        )
        self.appendToolbar('POMContainers', cmdsNewContainers)
        self.appendMenu('Part-o-Magic', cmdsNewContainers)

        cmdsTools = ([]
            + POM.Gui.Tools.exportedCommands()
        )
        self.appendToolbar('POMTools', cmdsTools)
        self.appendMenu('Part-o-Magic', cmdsTools)
        
    def Activated(self):
        pass


Gui.addWorkbench(PartOMagicWorkbench())



