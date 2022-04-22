#Use normalization and fluorescent ratio

#define function to normalize data based on quantiles
#this is more robust than min-max normalization
def norm_data(data, clip=[1E-3, 0.999], bounded=False):
    lims = np.quantile(data, clip)
    
    data_clipped = (data - lims[0]) / (lims[1] - lims[0])
        
    if bounded:
        data_clipped[data_clipped<0] = 0
        data_clipped[data_clipped>1] = 1
                
    return data_clipped
 
#normalize the red and green channel    
norm_red = norm_data(info_table_all["mean_intensity-0"])
norm_green = norm_data(info_table_all["mean_intensity-1"])

#create dataframe with normalized intensities
norm_fluor = pd.concat([norm_red,norm_green], keys=['norm_r','norm_g'], axis=1) 

#plot normalized intensities in scatter plot
fig, axs = plt.subplots(1,2, figsize=(12,6))
sns.histplot(ax=axs[0], data=norm_fluor)
sns.scatterplot(ax=axs[1], data=norm_fluor, x="norm_r", y="norm_g")

#add line x=y
axs[1].plot([0, 1.2], [0, 1.2], linewidth=2, color='k')
plt.show()

#classify cells based on highest normalized intensity
norm_fluor['is_red'] = norm_red > norm_green
norm_fluor['is_green'] = norm_red <= norm_green
norm_fluor['cell nr'] = 1
norm_fluor['frame'] = info_table_all['frame'] 

#create scatter plot, color points by classification
sns.scatterplot(x=norm_fluor['norm_r'], y=norm_fluor['norm_g'], hue=norm_fluor['is_red'])

#calculate number of red and green cells over time
cell_type_t = norm_fluor.groupby('frame').sum()

#calculate fraction of red cells
cell_type_t['red_fraction'] = cell_type_t['is_red'] / cell_type_t['cell nr']

#plot fraction of red cells over time
fig, axs = plt.subplots(1,2, figsize=(12,6))
sns.lineplot(ax=axs[0], data=cell_type_t[['is_red','is_green','cell nr']])
sns.lineplot(ax=axs[1], data=cell_type_t[['red_fraction']])
