# -*- coding: utf-8 -*-
import InfraRed as IR
import GetPTW as PTW
import skimage.io as io
import numpy as np
#import SimpleITK as sitk

# # # # Parameters :

sigma = 5.6704*(10**(-8)) # sigma is use in the boltzman equation
BB_Emissivity = 0.97
directory= "/home/corentin/CERVIFER/essai_bi-emissivite 24-09-14/calib-" # directory of th BB images for calibration
#directory= "/home/corentin/Bureau/Lien vers CERVIFER/essai_thermique-reel/essai_couple_12-06-14/essai_oligocristal_alu_12-06-14_donnees_IR/Calibration/" # directory of th BB images for calibration
#result_directory="/home/corentin/Bureau/Lien vers CERVIFER/essai_thermique-reel/essai_couple_12-06-14/essai_oligocristal_alu_12-06-14_donnees_IR/Calibration/results2/" #directory for storage of the coefficients
result_directory="/home/corentin/CERVIFER/essai_bi-emissivite 24-09-14/Results/" #directory for storage of the coefficients
video_directory="/home/corentin/CERVIFER/essai_bi-emissivite 24-09-14/"
Tmin=20 
Tmax=35
Tstep=1
polynomial_degree=5
bad_pix_critere=3
area_size=30 # size, in pixels, of the side of the square area used for the mean(DL) in the NUC 
NUC=True # set True if you want to use the NUC (DL=>DL) function
save_tif=True #set to True is you want a visualization of every image in the video. Activate this option only when calibration is sure, as it takes some time to run.
extension="ptw"  # the correct parameters are "ptm" or "ptw"
camera="jade" # the correct parameters are "jade" or "titanium"

 

# # # # Routine :

if __name__ == '__main__':

#Creating a calibration class:
  cal=IR.Calibration(sigma,BB_Emissivity,directory,result_directory,video_directory,Tmin,Tmax,Tstep,polynomial_degree,bad_pix_critere,area_size,NUC,extension,camera)

#Calling the calibration class functions:

  imageBB=cal.import_imageBB() #import the BB images
  
  matrice, DL_mean, shape=cal.reshape(imageBB) # reshape images as a matrix of vectors

  if NUC==True: # First apply a NUC(DL=>DL), then calculate the calibration coefficient 
    DLC_NUC=cal.NUC_DL(matrice,DL_mean)
    DLC_Calibrated=cal.DL2Flux(DLC_NUC)
  else: # Calibrate (DL=>Flux), without NUC
    DLC_Calibrated=cal.DL2Flux(matrice)

  DL_final,mouchard_final,last_nbr_BP=cal.bad_pixels(DLC_Calibrated,shape) # look for bad pixels and mask them

  cal.verif_calibration(imageBB)

  #cal.apply_to_essay(save_tif,video_directory+"Dep-0.ptw") #uncomment only when you are sure, it's a long function.
  
  #for j in range(0:18):
    #cal.apply_to_essay_mean(save_tif,video_directory+str(j)+".ptw",j) #uncomment only when you are sure, it's a long function.








# # # # Debug functions

"""
def verif_calibration(calibration_class):  # This loop evaluate and show every BB-image imported 
    T_map_reshaped={}
    for i in range(Tmin,Tmax+Tstep,Tstep):  
      T_map_reshaped[i]=calibration_class.apply_coeffs(imageBB[i])
      calibration_class.heat_map(T_map_reshaped[i])

def apply_to_essay(calibration_class,video_directory):  #Apply the coefficients to every images in the video, and save them as .tiff
  test1=PTW.GetPTW(video_directory)
  frame_nbr=test1.number_of_frames
  frame_rate=test1.frame_rate
  for i in range (0,frame_nbr):
    test1.get_frame(i)
    frame=(test1.frame_data)
    T_map=np.asarray(calibration_class.apply_coeffs(frame),dtype=np.float16)
    np.save((result_directory+"IR_images/"+"frame_"+str(i)),T_map) # Save the current image in the file
    #if i%600==0:
      #calibration_class.heat_map(T_map)
      
      
  
calibration_class=Cal.Calibration(sigma,BB_Emissivity,directory,result_directory,video_directory,Tmin,Tmax,Tstep,polynomial_degree,bad_pix_critere,area_size,NUC)
i=100
test1=PTW.GetPTW(video_directory)
frame_nbr=test1.number_of_frames
frame_rate=test1.frame_rate
test1.get_frame(i)
frame=(test1.frame_data)
T_map=calibration_class.apply_coeffs(frame)
    
img = sitk.GetImageFromArray(T_map.astype(np.int16))
sitk.WriteImage(img,result_directory+"IR_images/"+"SaveThatImg.tif")

io.imsave(result_directory+"SaveThatImg.tif",T_map.astype(np.int16))



img=io.imread(result_directory+"IR_images/"+"img_0_io.tiff")
import matplotlib.pyplot as plt
plt.imshow(img)
plt.clim(img.mean()-3*img.std(),img.mean()+3*img.std())
plt.colorbar()
plt.show()

  """    

#for i in range (15):
  #fig = plt.figure()
  #ax = fig.add_subplot(1,1,1)
  #plt.imshow(imageBB[i])
  #plt.clim(imageBB[i].mean()-3*imageBB[i].std(),imageBB[i].mean()+3*imageBB[i].std())
  #plt.colorbar()
  #plt.show(block=False)
