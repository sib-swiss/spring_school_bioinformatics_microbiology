from importlib.resources import path
from logging import exception
import numpy as np
import pandas as pd
from skimage.measure import regionprops
from delta.pipeline import Position as delta_pos
import pathlib

def add_segment_info(lin, label_stack):
    """Adds positional information of cells to lineage object

    Parameters
    ----------
    lin : delta lineage object
    label_stack : list
        list with label images, returned from delta

    Returns
    -------
    None 
        lineage is updated in place
    """
    #lin: delta linage object
    #label_stack: list of label images = pos.rois[0].label_stack
   
    #initialize new property keys:
    for cells in lin.cells:
        cells.setdefault('x_pos',[])
        cells.setdefault('y_pos',[])
   
    #loop frames
    for label_im in label_stack:
        #get region properties
        rp_list = regionprops(label_im)
        
        #assign cell phenotypes
        for idx, rp in enumerate(rp_list):
            #get lineage number of cell (note labels are 1 based, cell lineages are 0 based!)
            cell_idx = rp.label-1
            #assign phenotypes
            lin.cells[cell_idx]['x_pos'].append(rp.centroid[1]) #order in centroid is (y,x)
            lin.cells[cell_idx]['y_pos'].append(rp.centroid[0]) #order in centroid is (y,x)
                    
    return None

def split_lineages(lin):
    """converts delta lineage object, by splitting cell lineages at division

    Parameters
    ----------
    lin : delta lineage object

    Returns
    -------
    list
        list of dictionaries, each dictionary gives properties of cell from birth to division
    """
    new_lin = []
    lut = np.empty((0,5)) #id / first frame / last_frame / new_cell_id / colony_id
    id_cell = 0 
    
    firstcells = lin.cellnumbers[0]

    for id, cell in enumerate(lin.cells):
        #find division events
        div_time = [i for i, val in enumerate(cell['daughters']) if val != None]
        ndiv = len(div_time)
        
        for i in range(ndiv+1):
            
            if i==0:
                if cell['mother'] is not None:
                    corr_cell = lut[:,0] == cell['mother']
                    corr_frame = (lut[:,2] == cell['frames'][0]-1)
                    id_par = int(lut[np.all((corr_cell, corr_frame), axis=0),3])
                    id_colony = int(lut[np.all((corr_cell, corr_frame), axis=0),4])
                else: 
                    id_par = -1  
                    id_colony = id if  id in firstcells else -1             
            else: id_par = id_cell - 1
                
           
            if ndiv == 0:
                new_cell = cell.copy()
                cur_lut = [id, cell['frames'][0], cell['frames'][-1], id_cell, id_colony]
            else:
                start = div_time[i-1] if i>0 else 0
                end = div_time[i] if i<ndiv else len(cell['frames'])   
                cur_lut = [id, cell['frames'][start], cell['frames'][end-1], id_cell, id_colony]    
                        
                new_cell = {}
                for key, item in cell.items():
                    if isinstance(item, list):
                        new_cell[key] = item[start:end]
                    else:
                        new_cell[key] = item
                                            
            
            _ = new_cell.pop('mother')
            _ = new_cell.pop('daughters')
            new_cell['id_seg'] = new_cell.pop('id')
            new_cell['id_cell'] = id_cell 
            new_cell['id_par'] = id_par 
            new_cell['id_colony'] = id_colony 

                
            lut = np.concatenate((lut, np.array(cur_lut)[np.newaxis,:]))               
            new_lin.append(new_cell) 
            id_cell += 1   
    return new_lin

def lin_to_df(cell_list):
    """Convert list of dictionaries into dataframe

    Parameters
    ----------
    cell_list : list
        list of dictionaries, each dictionary gives properties of cell from birth to division

    Returns
    -------
    pandas dataframe
        dataframe with cell properties
    """
    #find vector based data (only vector based data is compatible with dataframe)
    vector_data = []
    [vector_data.append(key) for key in cell_list[0].keys() if isinstance(cell_list[0][key], list)]
    #create data frame
    df = pd.DataFrame(cell_list) 
    #this creates nested dataframe, we need to explode time into separate rows:
    df = df.explode(vector_data)
    #and reindex
    df = df.reset_index(drop=True)

    return df

def add_exra_lin_info(df):
    """Add extra lineage info of cell to dataframe

    Parameters
    ----------
    df : pandas dataframe

    Returns
    -------
    pandas dataframe
        input dataframe with additional columns added
    """
    #create look up table to link cells to parent, offspring, and siblings
    df_full = df.loc[df['id_par']>=0, ['id_par', 'id_cell']].reset_index(drop=True)
    dflin = df_full.groupby('id_par').agg([min, max]).rename(columns={"min" : "d1", "max" : "d2"})
    dflin.columns = dflin.columns.droplevel()
    dflin = dflin.reset_index()
    dflin.head()

    df["id_d1"] = -1
    df["id_d2"] = -1
    df["id_sib"] = -1

    #add offspring to parent
    for mom in np.unique(dflin["id_par"]):
        if mom >= 0:
            df.loc[df["id_cell"] == mom, "id_d1"] = int(dflin.loc[dflin["id_par"] == mom, "d1"])
            df.loc[df["id_cell"] == mom, "id_d2"] = int(dflin.loc[dflin["id_par"] == mom, "d2"])
    
    #add siblings to d1    
    for cell in np.unique(dflin["d1"]):
        df.loc[df["id_cell"] == cell, "id_sib"] = int(dflin.loc[dflin["d1"] == cell, "d2"])
        
    #add siblings to d2    
    for cell in np.unique(dflin["d2"]):
        df.loc[df["id_cell"] == cell, "id_sib"] = int(dflin.loc[dflin["d2"] == cell, "d1"])

    #rearange columns
    new_cols = [c for c in df.columns.tolist() if "id_" in c ]
    [new_cols.append(c) for c in df.columns.tolist() if not "id_" in c]
    df = df[new_cols] 
    
    return df


def delta_to_df(input):
    """create data frame with cell properties for delta position object

    Parameters
    ----------
    pos : (path to) delta position object 
        you can provide a delta position object
        
        a string to the path where the delta position object is saved
        
        or a pathlib path object to the path where the delta position object is saved

    Returns
    -------
    pandas dataframe 
        containing cell properties
    """
    
    if isinstance(input, delta_pos):
        pos = input
    elif isinstance(input, str):
        pos = delta_pos(None,None,None)
        pos.load(input)
    elif isinstance(input, pathlib.Path):
        pos = delta_pos(None,None,None)
        pos.load(str(input.resolve()))
    else:
        exception("Please input a delta position object or a valid path to a delta position object")
        
    
    #get lineage
    lin = pos.rois[0].lineage
    
    #add segment info
    add_segment_info(lin, pos.rois[0].label_stack)
    
    #split lineages:
    cell_list = split_lineages(lin)
        
    #convert to pandas dataframe
    df = lin_to_df(cell_list)
    
    #add extra lineage information
    df = add_exra_lin_info(df)
   
    return df