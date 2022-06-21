
from delta.data import seg_weights
import pathlib
import h5py
import numpy as np
import tifffile

root = pathlib.Path(pathlib.Path.home(), 'home', 'Delta2_Caulobacter')
data_dir = root / 'data'

training_file = data_dir /  'training_data_delta.hdf5'

with h5py.File(training_file, 'r') as f:
    mask_train = np.array(f['mask_train'])
    mask_valid = np.array(f['mask_valid'])
    image_train = np.array(f['image_train'])
    image_valid = np.array(f['image_valid'])    
    
training_set = data_dir / 'training'
validation_set = data_dir / 'validation'
    
training_set.mkdir(exist_ok=True)
validation_set.mkdir(exist_ok=True)

(training_set / 'img').mkdir(exist_ok=True)
(training_set / 'seg').mkdir(exist_ok=True)
(training_set / 'wei').mkdir(exist_ok=True)

(validation_set / 'img').mkdir(exist_ok=True)
(validation_set / 'seg').mkdir(exist_ok=True)
(validation_set / 'wei').mkdir(exist_ok=True)


#export training data to tiff    
for idx, (mask, im) in enumerate(zip(mask_train, image_train)):
    im_name = training_set / 'img' / ('img_%04i' % idx)
    lab_name = training_set / 'seg' / ('img_%04i' % idx)
    wei_name = training_set / 'wei' / ('img_%04i' % idx)
    
    tifffile.imwrite(im_name, im)
    tifffile.imwrite(lab_name, mask)
    tifffile.imwrite(wei_name, seg_weights(mask))    


for idx, (mask, im) in enumerate(zip(mask_valid, image_valid)):
    im_name = validation_set / 'img' / ('img_%04i' % idx)
    lab_name = validation_set / 'seg' / ('img_%04i' % idx)
    wei_name = validation_set / 'wei' / ('img_%04i' % idx)
    
    tifffile.imwrite(im_name, im)
    tifffile.imwrite(lab_name, mask)
    tifffile.imwrite(wei_name, seg_weights(mask))    
                