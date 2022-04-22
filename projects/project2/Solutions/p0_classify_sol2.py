#solution 2 using K-means clustering
from sklearn.cluster import KMeans 

#extract red and green intensities and create new data frame
norm_fluor = info_table_all[["mean_intensity-0","mean_intensity-1"]].copy()

#convert to numpy
norm_fluor_np = norm_fluor.to_numpy()

#do k-means clustering
kmeans_fit = KMeans(n_clusters=2, random_state=0).fit(norm_fluor_np)
cell_class = kmeans_fit.labels_

#show clustering outcome in plot
sns.scatterplot(x=norm_fluor_np[:,0], y=norm_fluor_np[:,1], hue=cell_class)

#classify cells 
norm_fluor['is_red'] = cell_class
norm_fluor['is_green'] = np.logical_not(cell_class)
norm_fluor['cell nr'] = 1
norm_fluor['frame'] = info_table_all['frame'] 

#calculate fraction of red cells over time 
cell_type_t2 = norm_fluor.groupby('frame').sum()
cell_type_t2['red_fraction'] = cell_type_t2['is_red'] / cell_type_t2['cell nr']

#plot fraction of red cells over time
fig, axs = plt.subplots(1,2, figsize=(12,6))
sns.lineplot(ax=axs[0], data=cell_type_t2[['is_red','is_green','cell nr']])
sns.lineplot(ax=axs[1], data=cell_type_t2[['red_fraction']])