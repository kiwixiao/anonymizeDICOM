# created by QX at 2021/06/14
#!/usr/bin/env python3
import pydicom
import dicognito.anonymizer
import glob
import os
from pathlib import Path
#%% pop up window to select folder
from tkinter import Tk
from tkinter.filedialog import askdirectory

path = askdirectory(title='Select Folder')
print(path)
Path(path+'/anonymizedFolder').mkdir(parents=True, exist_ok=True)
#%%
def imageTag_names_callback(dataset, data_element):
    if data_element.VR == "PN":
        data_element.value = "anonymous"
    if data_element.VR == "DA":
        data_element.value = "this is date"
    if data_element.VR == "AS":
        data_element.value = "this is age"
    if data_element.VR == "AR":
        data_element.value = "this is attribute"
    if data_element.VR == "TM":
        data_element.value = "this is time"
#    if data_element.VR == "UI":   # apply this will cause image distortion sometimes.
#        data_element.value = "this is UID"
        
def curves_callback(dataset, data_element):
    if data_element.tag.group & 0xFF00 == 0x5000:
        del dataset[data_element.tag]

data_elements = ['Patient ID',
                 "Patient's Birth Date"]
anonymizer = dicognito.anonymizer.Anonymizer()

filename = []
i = 1 



#for filepath in sorted(glob.glob(r'/D/Dropbox/CCHMCProjects/OSAMRI/'+'OSAMRI22_3201_ForShare/*.dcm')):
for filepath in sorted(glob.glob(path+'/*.dcm')):
    
    print('this is file path' + filepath)
    filename.append(os.path.basename(filepath))
    with pydicom.dcmread(filepath) as dataset:
        print('data set read done')
                
        dataset.walk(imageTag_names_callback)
# individual tag call back
        dataset.PatientID = "id"
        dataset.OtherPatientIDs = "id2"
        dataset.PatientSex = "sex"
        dataset.SeriesDescription = "SD"
        dataset.StationName = "Station"
        dataset.ProtocolName = "ProtocalName"
        dataset.StudyID = "StudyID"
        dataset.PerformedStationAETitle = "anonymous"
        dataset.RequestedProcedureID = "ID"
                
#        dataset.walk(curves_callback)
#   remove private tags
        dataset.remove_private_tags()

        output_filename = path+'/anonymizedFolder/anonymizedImage-' + str(i).zfill(5)+'.dcm'
        dataset.save_as(output_filename)
        i = i+1

print('process done')