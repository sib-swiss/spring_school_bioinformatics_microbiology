# Project 4B: A syntrophic bacterial consortium
## Project assignment
Develop a coarse-grained model that

 - Quantitatively reproduces batch growth on glucose of the glucose specialist,
 - Qualitatively reproduces batch growth on acetate of the acetate specialist,
 - Qualitatively reproduces the behavior of a consortium of glucose and acetate specialists growing on glucose in a chemostat.
 
## Biological question to be answered
What are the conditions for (i) the co-existence of the two strains and (ii) the occurrence of synthrophy, when the consortium is grown in a chemostat on glucose?

##Quantitative data and qualitative observations to account for

 - Growth curves of the glucose specialist in standard batch conditions on glucose,
 - Overflow of acetate by the glucose specialist in standard batch conditions on glucose,
 ![](../../assets/images/project4/glucose.png)
 - Toxic effect of acetate on growth rate.
 ![](../../assets/images/project4/acetate_growthrate.png)
 - Optional: dependence of acetate overflow on the glucose uptake rate 
 ![](../../assets/images/project4/overlow_growth_rate.png)
 
##Model structure
Environment described by concentrations of biomass (B, gdW/L), glucose (G, g/L) and acetate (A, g/L) in a continuous culture of constant volume.

$$\frac{dB_{C}}{dt} = \mu_C B_C - DB_C $$

$$\frac{dB_{P}}{dt} = \mu_P B_P - DB_P $$

$$\frac{dA}{dt} = (r^a_{overP} - r^a_{upP}) B_P + (r^a_{overC} - r^a_{upC}) B_C - DA$$

$$\frac{dG}{dt} = -r^g_{upP} B_P - r^g_{upC} B_C + D (G_{in} - G)$$

where $\mu$ is the growth rate (h⁻¹), D is the dilution rate (h⁻¹), $r_{over}$ is the acetate overflow rate (g/gDW/h) and $r_{up}$ (g/gDW/h) is the uptake rate. 

##Available data

The following data are available as [csv files](https://www.dropbox.com/sh/ojqkl4yvtc7m2ee/AADHj8WDWm7JfglG_ejSHFzva?dl=0):
 
 - Growth of the glucose specialist on glucose in batch,
 - The effect of acetate on the growth rate of the glucose specialist.
 
The units are the same as described in the [Model structure](#model-structure). Time is in hours.

 


 
    
 
 
 
