import zipfile
import adsk.core, adsk.fusion, traceback
import tempfile, os
from zipfile import ZipFile

handlers = []

def run(context):
    
    app = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        onCommandTerminated = MyCommandTerminatedHandler()
        ui.commandTerminated.add(onCommandTerminated)
        handlers.append(onCommandTerminated)

    except:
        if app:
            app.log('Fusion Connector Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    app = adsk.core.Application.get()
    app.log('Fusion Connector Stopped')

class MyCommandTerminatedHandler(adsk.core.ApplicationCommandEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args: adsk.core.ApplicationCommandEventArgs):
        #https://help.autodesk.com/view/fusion360/ENU/?guid=GUID-B801DDA8-9A0C-42AD-AC06-F8244CA08D65
        app = None
        try:
            app = adsk.core.Application.get()
            product = app.activeProduct
            design = adsk.fusion.Design.cast(product)

            allComps = design.allComponents

            exportMgr = design.exportManager

            for comp in allComps:
                compName = comp.name

                #export a usdz to a tmp directory
                with tempfile.TemporaryDirectory() as tmpDirName:
                    fileName = tmpDirName + '/' + compName.split()[0]                

                    usdOptions = exportMgr.createUSDExportOptions(fileName, comp)
                    exportMgr.execute(usdOptions)

                    fullFileName = fileName + '.usdz'
                    extractedFileName = fileName + '.zip'

                    #change file extension to .zip
                    os.rename(fullFileName, fileName + '.zip')
                    

                    #extract the usdz to the permanent file path  
                    with ZipFile(extractedFileName, 'r') as zip_ref:
                        zip_ref.extractall('O:/Library')

  
        
        except:
            if app:
                app.log('Failed:\n{}'.format(traceback.format_exc()))