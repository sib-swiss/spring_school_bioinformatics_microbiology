
import pathlib
import delta

import delta.config as cfg
from delta.utils import xpreader

import tensorflow as tf
tf.config.list_physical_devices()

def to_str(posixpath):
    return str(posixpath.resolve())   

#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'Delta2_Caulobacter')
data_dir = root / 'data' / 'raw'

#create output dir
output_root = root / 'processed_data'
(output_root).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder


#get config file
config_file = root / 'config_2D_caulobacter.json'
cfg.load_config(config_file)
delta.config.save_format = ('pickle','movie')

#find subfolders
folder_names = [f.name for f in sorted(data_dir.glob('AKS*'))]

for folder in folder_names:
    
    #get images in subfolder
    movie_names = [f.name for f in sorted((data_dir / folder).glob('*.tif*'))]

    #create output subfolder
    output_path = output_root / folder
    (output_path).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

    for movie in movie_names:
        


        posname = folder.name
        print('running position ', movie)
        
        #path to current position
        data_dir = data_dir / folder / movie
        
        #make subfolder for current position
        output_dir = output_path / posname
        (output_dir).mkdir(exist_ok=True)

        try:            
            # Load config ('2D' or 'mothermachine'):
            

            # Init reader (use bioformats=True if working with nd2, czi, ome-tiff etc):
            im_reader = xpreader(
                        data_dir,
                        prototype = 'Pos%03i_Frm%03i_Ch%02i.tif',
                        fileorder = 'ptc',
                        filenamesindexing=1
                        )

            # Print experiment parameters to make sure it initialized properly:
            print("""Initialized experiment reader:
                - %d positions
                - %d imaging channels
                - %d timepoints"""%(im_reader.positions, im_reader.channels, im_reader.timepoints)
            )

            # Init pipeline:
            xp = delta.pipeline.Pipeline(xpreader, resfolder=output_dir)   

            # Run it (you can specify which positions, which frames to run etc):
            xp.process()
            
        except:
            print('skipping postion', posname)