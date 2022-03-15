
from myPy import im,mything,me

    



class TessMap(im.Imaginable):
    #override
    def __writeToFile__(self,C,V,filename):
        with open(filename, 'w') as f:
            c=0
            for k in C:
                f.write(f'{k[0]} {k[1]} {k[2]}  {V[c]}\n')
                c=c+1

    def writeMapToFileAs(self,filename=None,mask=None):
        """Save the pixels values in the map as txt file with coordinates and value
        using the pattern defined un __writeTofile

        Args:
            filename (str, optional): Txt output filename.
            mask (_type_, optional): If a mask is set the output file will contains only the voxels in the map. Defaults to None.

        Returns:
            _type_: Bool
        """        
        return self.writeVoxelsCloudAs(filename,mask)

    

    
    



import os

class Tess(object):
    
    def __init__(self):
        self.conf={'bin':os.getenv('TESS_BIN')}
        self.parameters={}
        self.parametersFilename=None
        self.TList=[[]]
        self.Mask=None
        self.maps={
        'W':TessMap(), #Blood Perfusion,
        'R':TessMap(), #Material Density,
        'C':TessMap(), #Heat Capacity,
        'k':TessMap(), #Termal Conductivity,
        'Q':TessMap(), #Heat Generated by the metabolism,
        'SAR':TessMap(), #Specific energy Absorption Rate
        'TOld':TessMap(), #TOld
        'Output':TessMap(), #Output
                        }
        self.__reset__()

    def __reset__(self):
        self.parameters={
        "Nx" :179, 
        "Ny":179,
        "Nz":460,
        "dx":0.005,
        "dy":0.005,
        "dz":0.005,
        "dt":[0.2],
        "zmin":20,
        "zmax":459,
        "maxsavetime":-1,
        "DeltaSave":10,
        "heatingtime":[60],
        "eps":1e-9,
        "Cblood":1057,
        "Rblood":3600,
        "Tblood":310,
        "Wair":0.0,
        "Rair":1.3,
        "Cair":1006.0,
        "Kair":0.026,
        "Qair":0.0,
        "Tair":296,
        "T0V":14738860,
        "Toldfile":"Told.dat", # can this have path?
        "SARfile":"SAR.dat",# can this have path?
        "Wfile":"W.dat",# can this have path?
        "Rfile":"R.dat",# can this have path?
        "Qfile":"Q.dat",# can this have path?
        "Cfile":"C.dat",# can this have path?
        "Kfile":"K.dat",# can this have path? voxel clouds + values
        "outputfile":"Toutput.dat",# can this have path?
        "Posxfile":"uniform",
        "Posyfile":"uniform",
        "Poszfile":"uniform",
        "Tbloodfile":"constant",
        "scaleSARfile":"constant",
        }
        self.parametersFileStatus=False
        self.parametersFilename='Parameters.dat'
        self.maps["Output"]=TessMap()
        self.TList=[[]]

    def __readOutput__(self):
        with open(self.getOutputFilename(), 'r') as f:
            lines = [line.rstrip('\n') for line in f]
            f.close()
        return lines
    def __createMapFromPointList__(self,lines=[]):
        IM = self.getMask().getDuplicate()
        O=IM.createZerosNumpyImageSameDimensionOfImaginable()
        # read the file
       
        for line in lines:
            coords, value = line.split("  ")
            x,y,z=coords.split(" ")
            try:
                O[int(z),int(y),int(x)]=float(value) #numpy is ZYX
            except:
                print("no")
        
        IM.setImageArray(O)
        return IM
    def __writeParamsFile__(self):
        with open(self.getParameterFilename(), 'w') as the_file:
            for key in self.parameters:
                the_file.write(f'{key} = {self.parameters[key]}\n')
        the_file.close()
    def __calculateTemperature__(self):
        b=mything.BashIt()
        b.setCommand(self.conf["bin"] +" "+  self.getParameterFilename())
        print("start")
        b.run()
        print("finished")
        return True

    def getParameterFilename(self):
        return self.parametersFilename

    def setParameterFilename(self,s):
        self.parametersFilename=s

    def getParameterFileStatus(self):
        return self.parametersFileStatus

    def setParameterFileStatus(self,s=True):
        self.parametersFileStatus=s
    
    def __canIStartTheCalculation(self):
        return True

    def setBloodPerfusionOutputFilename(self,filename):
        self.parameters["Wfile"]=filename
    
    def getBloodPerfusionOutputFilename(self):
        return self.parameters["Wfile"]

    def setBloodPerfusionMap(self,filename):
        """set the W term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["W"].takeThisImage(filename)
        self.maps["W"].writeMapToFileAs(self.getBloodPerfusionOutputFilename(),mask=self.getMask())
    
    def getBloodPerfusionMap(self):
        return self.maps["W"]
        




    

    def setMask(self,filename):
        """set a Mask

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.Mask=TessMap()
        self.Mask.takeThisImage(filename)


    def getMask(self):
        return self.Mask






    def setMaterialDensityOutputFilename(self,filename):
        self.parameters["Rfile"]=filename
    
    def getMaterialDensityOutputFilename(self):
        return self.parameters["Rfile"]

    def setMaterialDensityMap(self,filename):
        """set the R term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["R"].takeThisImage(filename)
        self.maps["R"].writeMapToFileAs(self.getMaterialDensityOutputFilename(),mask=self.getMask())

    def getMaterialDensityMap(self):
        return self.maps["R"]

    def setHeatCapacityOutputFilename(self,filename):
        self.parameters["Cfile"]=filename
    
    def getHeatCapacityOutputFilename(self):
        return self.parameters["Cfile"]

    def setHeatCapacityMap(self,filename):
        """set the C term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["C"].takeThisImage(filename)
        self.maps["C"].writeMapToFileAs(self.getHeatCapacityOutputFilename(),mask=self.getMask())
    
    
    def setMetabolismHeatOutputFilename(self,filename):
        self.parameters["Qfile"]=filename
    
    def getMetabolismHeatOutputFilename(self):
        return self.parameters["Qfile"]

    def setMetabolismHeatMap(self,filename):
        """set the Q term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["Q"].takeThisImage(filename)
        self.maps["Q"].writeMapToFileAs(self.getMetabolismHeatOutputFilename(),mask=self.getMask())
      
   
   
    def setTermalConductivityOutputFilename(self,filename):
        self.parameters["Kfile"]=filename
    
    def getTermalConductivityOutputFilename(self):
        return self.parameters["Kfile"]

    def setTermalConductivityMap(self,filename):
        """set the k term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["k"].takeThisImage(filename)
        self.maps["k"].writeMapToFileAs(self.getTermalConductivityOutputFilename(),mask=self.getMask())


    def setSAROutputFilename(self,filename):
        self.parameters["SARfile"]=filename
    
    def getSAROutputFilename(self,):
        return self.parameters["SARfile"]

    def setSARMap(self,filename):
        """set the SAR term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["SAR"].takeThisImage(filename)
        self.maps["SAR"].writeMapToFileAs(self.getSAROutputFilename(),mask=self.getMask())

        
    def setTOldOutputFilename(self,filename):
        # I know seems strange but it's like that
        self.parameters["Toldfile"]=filename
    
    def getTOldOutputFilename(self):
        return self.parameters["Toldfile"]

    def setTOldMap(self,filename):
        """set the T Old term of the bioheat equations

        Args:
            filename ('str,sitk.image,im.Imaginable): a 3d map
        """        
        self.maps["TOld"].takeThisImage(filename)
        self.maps["TOld"].writeMapToFileAs(self.getTOldOutputFilename(),mask=self.getMask())

    def setOutputFilename(self,filename):
        # I know seems strange but it's like that
        self.parameters["outputfile"]=filename
    
    def getOutputFilename(self):
        return self.parameters["outputfile"]
    
    def getOuput(self):
        if len(self.TList[0])==0:
            F=me.Pathable(self.getOutputFilename())
            if F.exists():
                self.TList=self.__readOutput__()
            else:
                P=me.Pathable(self.getParameterFilename())
                if (P.exists()):
                    self.__writeParamsFile__()
                    if(self.__calculateTemperature__()):
                        self.TList=self.__readOutput__()
        return self.TList     


        # check if theres a parameter file
        # check if the parameter file exists 
        # start Giuseppe's Code
        # read giuseppe output
        # and store it

        return True

    def getOuputMap(self):
        if (not self.maps["Output"].isImageSet()):
            PVlist=self.getOuput()
            O=self.__createMapFromPointList__(PVlist)
            self.maps["Output"].takeThisImage(O.getImage())
        return self.maps["Output"]
    
    def saveOutputMapAs(self,filename):
        O=self.getOuputMap()
        O.writeImageAs(filename)

    def writeOutputMapAs(self,filename):
        self.saveOutputMapAs(filename)

    



        






