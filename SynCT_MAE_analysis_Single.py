
# coding: utf-8

# # a) reads in a set of DICOM CT images
# # b) reads in a set of DICOM SynCT images
# # c) calculates MAE etc 
# 

# In[1]:


import dicom_numpy
import math
import dicom
import os
import numpy as np
import sys
import json
import nibabel as nib


# In[2]:


PatientID = 62


# In[3]:


CTDicomDirectory = "D:/CNNdata/SynCT_FINAL_EclipseTesting/1_CT/"
SynCTDicomDirectory = "D:/CNNdata/SynCT_FINAL_EclipseTesting/3_SynCT_deformed_resampled/"


# In[4]:


CTPathDicom = os.path.join(CTDicomDirectory + str(PatientID) + "/")
SynCTPathDicom = os.path.join(SynCTDicomDirectory + str(PatientID) + "/ordered_SynCT/")


# In[5]:


print(CTPathDicom)
print(SynCTPathDicom)


# In[6]:


#from pandas import DataFrame
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# In[7]:


def extract_voxel_data(list_of_dicom_files):
    datasets = [dicom.read_file(f) for f in list_of_dicom_files]
    try:
        voxel_ndarray, ijk_to_xyz = dicom_numpy.combine_slices(datasets)
    except dicom_numpy.DicomImportException as e:
        # invalid DICOM data
        raise
    return voxel_ndarray


# In[8]:


lstFilesDCM_CT = []  # create an empty list
for dirName, subdirList, fileList in os.walk(CTPathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file is DICOM
            lstFilesDCM_CT.append(os.path.join(dirName,filename))

CTarray = extract_voxel_data(lstFilesDCM_CT)
print(np.shape(CTarray))
NumSlices = np.size(CTarray,2)
print(NumSlices)


# In[9]:


lstFilesDCM_SynCT = []  # create an empty list
for dirName, subdirList, fileList in os.walk(SynCTPathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file is DICOM
            lstFilesDCM_SynCT.append(os.path.join(dirName,filename))

SynCTarray = extract_voxel_data(lstFilesDCM_SynCT)
print(np.shape(SynCTarray))
NumSlices = np.size(SynCTarray,2)
print(NumSlices)


# In[10]:


thresh = -900


# In[11]:


plt.pcolormesh(CTarray[:,:,30])
plt.colorbar()


# In[12]:


plt.pcolormesh(SynCTarray[:,:,30])
plt.colorbar()


# In[13]:


plt.plot(CTarray[:,280,30])
plt.plot(SynCTarray[:,280,30])


# In[14]:


CTarray[CTarray < thresh] = 'nan' # or use np.nan


# In[15]:


plt.pcolormesh(CTarray[:,:,30])
plt.colorbar()


# In[16]:


SynCTdiff = np.zeros((NumSlices,1,512,512), dtype=int)


# In[17]:


SynCTdiff = SynCTarray - CTarray


# In[18]:


np.shape(SynCTdiff)


# In[19]:


plt.pcolormesh(SynCTdiff[:,:,40])
plt.colorbar()


# In[20]:


plt.plot(CTarray[350:390,280,0])
plt.plot(SynCTarray[350:390,280,0])
plt.plot(SynCTdiff[350:390,280,0])


# In[21]:


print("mean error = ", np.nanmean(SynCTdiff))
print("stdev diff = ", np.nanstd(SynCTdiff))


# In[22]:


SynCTdiffABS = np.absolute(SynCTdiff)
print("MAE = ", np.nanmean(SynCTdiffABS))

