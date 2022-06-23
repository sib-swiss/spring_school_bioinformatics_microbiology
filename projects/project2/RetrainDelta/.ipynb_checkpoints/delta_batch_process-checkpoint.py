
import pathlib
import delta.config as cfg
from delta.utilities import xpreader
from delta.pipeline import Pipeline
import tensorflow as tf

dev = tf.config.list_physical_devices()
print(dev)

def to_str(posixpath):
    return str(posixpath.resolve())   

#set paths
root = pathlib.Path(pathlib.Path.home(), 'home', 'Delta2_Caulobacter')
data_dir = root / 'data' / 'rawdata'

#create output dir
output_root = root / 'processed_data'
(output_root).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

#get config file
config_file = root / 'config_2D_caulobacter.json'
cfg.load_config(config_file)
cfg.save_format = ('pickle','movie')

#find subfolders
folder_names = [f.name for f in sorted(data_dir.glob('AKS*'))]

for folder in folder_names:
    #get images in subfolder
    movie_names = [f.name for f in sorted((data_dir / folder).glob('*.tif*'))]

    #create output subfolder
    output_path = output_root / folder
    (output_path).mkdir(exist_ok=True) #create output data folder,  each position will be placed in a subfolder

    for movie in movie_names:        
        #path to current position
        movie_dir = data_dir / folder / movie
        
        #make nickname of movei (adapt to file name structure, here we take the part starting at TL and stopping before __R3D)
        start = movie.find('TL')
        end = movie.find('_R3D', start)
        movie_name_short = movie[start:end]
        
        #make subfolder for current position
        output_dir = output_path / movie_name_short
        (output_dir).mkdir(exist_ok=True)

        try:  
            print('starting with movie %s->%s' %(folder,movie_name_short)) 
            # Init reader (use bioformats=True if working with nd2, czi, ome-tiff etc):
            im_reader = xpreader(movie_dir, use_bioformats=True)

            # Print experiment parameters to make sure it initialized properly:
            print("""Initialized experiment reader:
                - %d positions
                - %d imaging channels
                - %d timepoints"""%(im_reader.positions, im_reader.channels, im_reader.timepoints)
            )

            # Init pipeline:
            xp = Pipeline(im_reader, resfolder=to_str(output_dir))   

            # Run pipeline
            xp.process()
            
        except:
            print('error with movie %s->%s, skipping to next' %(folder,movie_name_short)) 



