# -*- coding: utf-8 -*-
"""
Main:  Playground for testing implemented functions
@author: andre
"""
import pandas as pd
import os
os.chdir("C:/Users/andre/Documents/GitHub/Exploration-of-Learner-Data-with-VAEs")
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_color_codes("colorblind")
from Replication_main import Replication_of_Paper_Figures
from Experiment_table_Function import Experiment_table
from scipy.stats import pearsonr
import numpy as np


###############################################################################
#Data for Activation Testing
###############################################################################
df_raw, df_agg, dfa_list, dfb_list = Experiment_table(num_students= [10000], num_tests = [10], 
                                                      num_questions =[28], num_networks = 20, which_dists = ['norm'],
                                                      arches = [0], activations = ['sigmoid','tanh','relu'], dropouts = [0.0])
df_raw.to_csv('activation_testing.csv', index=False)
act = pd.read_csv('./Experiment_Data/activation_testing.csv')
act.groupby('activations').agg({'th_Corr':{'mean', 'std', 'count'}})#no difference whatsoever
act.groupby('activations').agg({'epochs':{'mean','std', np.min, np.max}})

g = sns.catplot(x= 'activations',y='th_Corr' ,  
                data =act, kind = 'bar', palette= 'muted')
sns.catplot(x= 'activations',y='th_Corr' , data =act)
g.set_ylabels("Correlation")
g.fig.suptitle('Differences in Correlations for Activations')
g.savefig('Activations')
###############################################################################
#Data for Architecture Testing
###############################################################################
df_raw, _,_,_ = Experiment_table(num_students= [10000], num_tests = [10], 
                                 num_questions =[28], num_networks = 20, which_dists = ['norm'],
                                 arches = [1,2,3], activations = ['relu'], 
                                 dropouts = [0.0])

#df_raw.to_csv('arch_testing_big.csv')
raw = pd.read_csv('./Experiment_Data/arch_testing_big.csv')
raw.groupby(['Arch_type','dropout_rate','activations']).agg({'th_Corr':{'mean','std', np.min, np.median}})#Very high std.  Why?  Early stopping too aggressive?
sns.catplot(x= 'Arch_type',y='th_Corr' , data =raw)
raw.groupby('Arch_type').agg({'epochs':{'mean','std', np.min, np.max}})
#does early stopping lead to worse correlation scores?  Graph correlation vs epochs
g = sns.catplot(x = 'epochs', y = 'th_Corr', data = raw, hue = 'Arch_type')

#Not obvious from the graph.  Get the actual correlations to be more certain
def get_pearson(df, arch_type):
        return pearsonr(raw[raw['Arch_type']==arch_type]['th_Corr'], raw[raw['Arch_type']==arch_type].epochs)
get_pearson(raw, 1)
get_pearson(raw,2)
get_pearson(raw,3)
#The longer a network runs, the worse its correlation with the real data.  Weird...
sns.catplot(x = 'epochs', y = 'th_Corr', data = raw[raw['Arch_type']==1], hue = 'Arch_type')
sns.catplot(x = 'epochs', y = 'th_Corr', data = raw[raw['Arch_type']==2], hue = 'Arch_type')
sns.catplot(x = 'epochs', y = 'th_Corr', data = raw[raw['Arch_type']==3], hue = 'Arch_type')
#Much more obvious now that the Architectures are plotted individually.  The 
#longer a network is running, the worse off it is.

#The strange part is that the difference between the variances with arch 0 and the 
# variances with arch 1 with no dropout. The only difference is that the arch 1
# has a batch norm layer.  I will test the two of them head to head to see if 
# the batch norm is what causes this dramatic increase in variance.  If it does,
# I will just remove the batch norm layer
df_raw, _,_,_ = Experiment_table(num_students= [10000], num_tests = [10], 
                                 num_questions =[28], num_networks = 20, which_dists = ['norm'],
                                 arches = [0,1], activations = ['relu'], 
                                 dropouts = [0.0])
df_raw.groupby('Arch_type').agg({'th_Corr':{'mean','std','min'}, 
              'epochs':{'mean','std'}})#Differences in Correlation

sns.catplot(x='Arch_type', y='th_Corr', data = df_raw) 
#Looks like the stinking batch norm caused the problem!!!!  


#Now testing this with batchnorm turned off
df_raw2, _,_,_ = Experiment_table(num_students= [10000], num_tests = [10], 
                                 num_questions =[28], num_networks = 20, which_dists = ['norm'],
                                 arches = [0,1], activations = ['relu'], 
                                 dropouts = [0.0])
df_raw2.groupby('Arch_type').agg({'th_Corr':{'mean','std','min'}, 
              'epochs':{'mean','std'}})#Differences in Correlation

sns.catplot(x='Arch_type', y='th_Corr', data = df_raw2) 
#standard deviations are totally normal!  I will henceforth turn off batchnorm

#Redoing the testing for the test of different Architectures
df_raw3, _,_,_ = Experiment_table(num_students= [10000], num_tests = [10], 
                                 num_questions =[28], num_networks = 20, which_dists = ['norm'],
                                 arches = [1,2,3], activations = ['relu'], 
                                 dropouts = [0.0])
df_raw3.groupby('Arch_type').agg({'th_Corr':{'mean','std','min'}, 
              'epochs':{'mean','std'}})#Differences in Correlation
sns.catplot(x='Arch_type', y='th_Corr', data = df_raw3) 
#Problem Solved

###############################################################################
#Data for Regularization Testing
###############################################################################
df_raw4,_,_,_ = Experiment_table(num_students= [10000], num_tests = [10], num_questions =[28], 
                                num_networks = 20, which_dists = ['norm'],
                                arches = [1,2,3], activations = ['relu'], dropouts = [0.05,.1,.2])
df_raw4.groupby(['Arch_type', 'dropout_rate']).agg({'th_Corr':{'mean','std','min'}, 
              'epochs':{'mean','std'}})#Differences in Correlation
sns.catplot(x='Arch_type', y='th_Corr', data = df_raw4 ) 

###############################################################################
#Testing the best architecture design and Dropout level.  This will be done by
# combining df_raw3 and df_raw4.  We will visually inspect the differences and 
# perform ANOVA within architecture groups to see if dropout does anything
###############################################################################
big_test = pd.concat([df_raw3,df_raw4])
big_test.groupby(['Arch_type', 'dropout_rate'], as_index = False).agg({'th_Corr':{'mean','std','min','count'}})
big_test.to_csv('Architectural_Big_Test.csv', index=False)
g = sns.catplot(x= 'Arch_type',y='th_Corr' ,  data =big_test, kind = 'bar', 
                hue= 'dropout_rate', palette= 'muted')
g.set_ylabels("Correlation")
g.fig.suptitle('Correlation for Different Architectures by Dropout Rate')
g.savefig('Architecture_Test')

data = big_test.groupby(['Arch_type', 'dropout_rate'], as_index = False).agg({'th_Corr':{'mean','std'}})
data.columns=['Architecture','Dropout_rate','std','mean']




###############################################################################
#Plot of fig3
###############################################################################
tab1, fig3, fig4, tab2, fig5, vae, ae, data_list = Replication_of_Paper_Figures()

fig, ax =plt.subplots(nrows = 1, ncols = 2, figsize = (15, 5))
sns.scatterplot(x = 'True_Values',y= 'Estimates_ae',  ax=ax[0], hue = 'skill_num', 
                palette = 'colorblind', data = fig3).set_title('AE Parameter Recovery')
sns.scatterplot(x = 'True_Values',y= 'Estimates_vae', ax=ax[1], hue = 'skill_num', 
                palette = 'colorblind', data= fig3).set_title('VAE Parameter Recovery')
ax[0].set_ylim([0.0,4])
ax[1].set_ylim([0.0,4])
fig.show()
fig.savefig('fig3.png')

###############################################################################
#Plot of fig 4
###############################################################################
fig, ax =plt.subplots(nrows = 1, ncols = 2, figsize = (15, 5))
sns.scatterplot(x = 'True_Values',y= 'Estimates_ae',  ax=ax[0],  
                data = fig4).set_title('AE Parameter Recovery')
sns.scatterplot(x = 'True_Values',y= 'Estimates_vae',  ax=ax[1],  
                data = fig4).set_title('VAE Parameter Recovery')
ax[0].set_ylim([-4.0,4.0])
ax[1].set_ylim([-4.0,4.0])
fig.show()
fig.savefig('fig4.png')

###############################################################################
#Making Table 2 pretty
###############################################################################
Table2 = pd.DataFrame({'Statistic': ['AVRB', 'AVRB', 'CORR','CORR', 'RMSE','RMSE'],
                       'Model': ['VAE','AE','VAE','AE','VAE','AE'],
                       'Theta1': tab2['Theta1'],
                       'Theta2': tab2['Theta2'],
                       'Theta3': tab2['Theta3'],})

###############################################################################
#Plot of fig 5
###############################################################################
fig, ax =plt.subplots(nrows = 1, ncols = 2, figsize = (15, 5))
sns.scatterplot(x = 'Theta1_true',y= 'Theta1_ae',  ax=ax[0],  
                data = fig5).set_title('AE prediction of 1st latent trait')
sns.scatterplot(x = 'Theta1_true',y= 'Theta1_vae',  ax=ax[1],  
                data = fig5).set_title('VAE prediction of 1st latent trait')
ax[0].set_ylim([-4.0,4.0])
ax[1].set_ylim([-4.0,4.0])
fig.show()
fig.savefig('fig5.png')


fig, ax =plt.subplots(nrows = 1, ncols = 2, figsize = (15, 5))
sns.scatterplot(x = 'Theta2_true',y= 'Theta2_ae',  ax=ax[0],  
                data = fig5).set_title('AE prediction of 2nd latent trait')
sns.scatterplot(x = 'Theta2_true',y= 'Theta2_vae',  ax=ax[1],  
                data = fig5).set_title('VAE prediction of 2nd latent trait')
ax[0].set_ylim([-4.0,4.0])
ax[1].set_ylim([-4.0,4.0])
fig.show()
#fig.savefig('fig5_2.png')

fig, ax =plt.subplots(nrows = 1, ncols = 2, figsize = (15, 5))
sns.scatterplot(x = 'Theta3_true',y= 'Theta3_ae',  ax=ax[0],  
                data = fig5).set_title('AE prediction of 3rd latent trait')
sns.scatterplot(x = 'Theta3_true',y= 'Theta3_vae',  ax=ax[1],  
                data = fig5).set_title('VAE prediction of 3rd latent trait')
ax[0].set_ylim([-4.0,4.0])
ax[1].set_ylim([-4.0,4.0])
fig.show()
#fig.savefig('fig5_3.png')


pearsonr(fig4['True_Values'], fig4['Estimates_vae'])