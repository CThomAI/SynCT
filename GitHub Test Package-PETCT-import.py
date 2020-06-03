
# coding: utf-8

# 1. Import CTpet and PET data

# In[ ]:


## https://gist.github.com/somada141/8dd67a02e330a657cf9e


# In[ ]:


## note that the PET and CT will have different number of slices and will be of different dimensions


# In[ ]:


from matplotlib import pyplot as plt


# In[ ]:


import dicom
import os
import numpy as np


# In[ ]:


Patients= ((0,41,120,154),
           (1,25,80,125),
           (2,41,101,133),
           (3,43,93,152),
           (4,44,129,176),
           (5,68,134,172),
           (6,39,104,139),
           (7,41,97,116),
           (8,43,102,140),
           (9,50,149,192),
           (10,51,129,176),
           (11,28,80,128))


# In[ ]:


np.shape(Patients)


# In[ ]:


Patients[2][0]


# In[ ]:


baseCT = "D:/CNNdata/Bowel_Segmentation/RATHL_Data_for_Testing/CT"
basePET = "D:/CNNdata/Bowel_Segmentation/RATHL_Data_for_Testing/PT"

TestData = 10

ID = Patients[TestData][0]
BBinf = Patients[TestData][1]
BBsup = Patients[TestData][2]

PathDicomCT = os.path.join(str(baseCT) + str(ID))
lstFilesDCM_CT = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicomCT):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM_CT.append(os.path.join(dirName,filename))

PathDicomPET = os.path.join(str(basePET) + str(ID))
lstFilesDCM_PET = []  # create an empty list
for dirName, subdirList, fileList in os.walk(PathDicomPET):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM_PET.append(os.path.join(dirName,filename))
            


# In[ ]:


# basePET = "D:/CNNdata/Bowel_Segmentation/RATHL_Data_for_Testing/PT"

# PathDicomPET = os.path.join(str(basePET) + str(ID))
# lstFilesDCM_PET = []  # create an empty list
# for dirName, subdirList, fileList in os.walk(PathDicomPET):
#     for filename in fileList:
#         if ".dcm" in filename.lower():  # check whether the file's DICOM
#             lstFilesDCM_PET.append(os.path.join(dirName,filename))


# In[ ]:


print(TestData)
print(BBinf)
print(BBsup)


# In[ ]:


# Get ref file
RefCT = dicom.read_file(lstFilesDCM_CT[0])
# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefCT.Rows), int(RefCT.Columns), len(lstFilesDCM_CT))
# Load spacing values (in mm)
ConstPixelSpacing = (float(RefCT.PixelSpacing[0]), float(RefCT.PixelSpacing[1]), float(RefCT.SliceThickness))
CTReconDiameter = round((RefCT.PixelSpacing[0]) * (RefCT.Rows))
CTReconDiameter


# In[ ]:


# Get ref file
RefPET = dicom.read_file(lstFilesDCM_PET[0])
# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims_PET = (int(RefPET.Rows), int(RefPET.Columns), len(lstFilesDCM_PET))
# Load spacing values (in mm)
ConstPixelSpacing_PET = (float(RefPET.PixelSpacing[0]), float(RefPET.PixelSpacing[1]), float(RefPET.SliceThickness))

PETReconDiameter = round((RefPET.PixelSpacing[0]) * (RefPET.Rows))
PETReconDiameter


# In[ ]:


#print(RefCT)


# In[ ]:


RescaleIntercept = int(RefCT.RescaleIntercept)
print(RescaleIntercept)


# In[ ]:


# The array is sized based on 'ConstPixelDims'
a_CT = np.zeros(ConstPixelDims[2])
i=0
# loop through all the DICOM files, reading the slice numbers to array
for filenameDCM in lstFilesDCM_CT:
    dsCT = dicom.read_file(filenameDCM)
    sliceNumber = dsCT.ImagePositionPatient[2]
    a_CT[i] = sliceNumber
    i=i+1


# In[ ]:


a_CT


# In[ ]:


b_CT = np.sort(a_CT, axis=-1, kind='quicksort', order=None) #element 0 is inf-most slice


# In[ ]:


b_CT


# In[ ]:


# The array is sized based on 'ConstPixelDims'
ArrayCT = np.zeros(ConstPixelDims, dtype=RefCT.pixel_array.dtype)
ArrayCTNew = np.zeros(ConstPixelDims, dtype=RefCT.pixel_array.dtype)
# loop through all the DICOM files and place data in the correct place according to slice position
for filenameDCM in lstFilesDCM_CT:
    # read the file
    dsCT = dicom.read_file(filenameDCM)
    sliceNumber = dsCT.ImagePositionPatient[2]
    result = np.where(b_CT == sliceNumber) #to print this number use result[0][0]
    print(result[0][0])
    
    # store the raw image data
    ArrayCT[:, :, result[0][0]] = dsCT.pixel_array

#ArrayCTNew = ArrayCTNew + RescaleIntercept # This is important as it converts back to HU using RescaleIntercept
#Think this is done later ...


# In[ ]:


np.shape(ArrayCT)


# In[ ]:


plt.pcolormesh(ArrayCT[:,:,100])
plt.colorbar()


# In[ ]:


np.min(ArrayCT)


# In[ ]:


plt.plot(ArrayCT[250,:,100])


# In[ ]:


ArrayCT = ArrayCT+RescaleIntercept


# In[ ]:


plt.plot(ArrayCT[300,:,100])


# In[ ]:


ArrayCT[ArrayCT < -1000] = -1000


# In[ ]:


plt.plot(ArrayCT[300,:,100])


# In[ ]:


plt.pcolormesh(ArrayCT[:,:,100])
plt.colorbar()


# In[ ]:


# The array is sized based on 'ConstPixelDims'
a_PET = np.zeros(ConstPixelDims_PET[2])
i=0
# loop through all the DICOM files, reading the slice numbers to array
for filenameDCM in lstFilesDCM_PET:
    dsPET = dicom.read_file(filenameDCM)
    sliceNumber = dsPET.ImagePositionPatient[2]
    a_PET[i] = sliceNumber
    i=i+1


# In[ ]:


a_PET


# In[ ]:


b_PET = np.sort(a_PET, axis=-1, kind='quicksort', order=None) #element 0 is inf-most slice


# In[ ]:


b_PET


# In[ ]:


# The array is sized based on 'ConstPixelDims'
ArrayPET = np.zeros(ConstPixelDims_PET, dtype=RefPET.pixel_array.dtype)

# loop through all the DICOM files and place data in the correct place according to slice position
for filenameDCM in lstFilesDCM_PET:
    # read the file
    dsPET = dicom.read_file(filenameDCM)
    sliceNumber = dsPET.ImagePositionPatient[2]
    result = np.where(b_PET == sliceNumber) #to print this number use result[0][0]
    print(result[0][0])
    
    # store the raw image data
    ArrayPET[:, :, result[0][0]] = dsPET.pixel_array


# In[ ]:


np.shape(ArrayPET)


# In[ ]:


ArrayCT[250,250,55]


# In[ ]:


ArrayCT.dtype


# In[ ]:


fig = plt.figure(figsize=(16, 8))
plt.subplot(1,2,1)
plt.pcolormesh(ArrayCT[:,:,55])
plt.colorbar()
plt.subplot(1,2,2)
plt.pcolormesh(ArrayPET[:,:,55])
plt.colorbar()


# In[ ]:


ArrayCTNew = np.zeros((ConstPixelDims[2],1,ConstPixelDims[0],ConstPixelDims[1]), dtype=ArrayCT.dtype)

for i in range(0,ConstPixelDims[2]):
    ArrayCTNew[i,0,:,:] =  ArrayCT[:,:,i]
    ArrayCTNewRot = np.rot90(ArrayCTNew[i,0,:,:],2)
    ArrayCTNewRotFlip = np.fliplr(ArrayCTNewRot)
    ArrayCTNew[i,0,:,:] = ArrayCTNewRotFlip


# In[ ]:


ArrayPETNew = np.zeros((ConstPixelDims_PET[2],1,ConstPixelDims_PET[0],ConstPixelDims_PET[1]), dtype=ArrayPET.dtype)

for i in range(0,ConstPixelDims_PET[2]):
    ArrayPETNew[i,0,:,:] =  ArrayPET[:,:,i]
    ArrayPETNewRot = np.rot90(ArrayPETNew[i,0,:,:],2)
    ArrayPETNewRotFlip = np.fliplr(ArrayPETNewRot)
    ArrayPETNew[i,0,:,:] = ArrayPETNewRotFlip


# In[ ]:


fig = plt.figure(figsize=(16, 8))
plt.subplot(1,2,1)
plt.pcolormesh(ArrayCTNew[55,0,:,:])
plt.colorbar()
plt.subplot(1,2,2)
plt.pcolormesh(ArrayPETNew[55,0,:,:])
plt.colorbar()

