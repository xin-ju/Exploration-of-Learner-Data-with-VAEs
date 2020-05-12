# Exploration of Learner Data with VAEs
Given student test scores, can you know with granularity what a student knows?  If a student scores an 65 on a trig test, does the student not understand the trigonometry, or just the algebra?  "Autoencoders for Educational Assessment" by Converse, et al., found a way to automate the process using Variational Autoencoders.  Through integrating the variational autoencoder with some outside information, the authors were able to obtrain strong estimates for ground truth student knowledge.  Moreover, they were able to uncover exactly how the tests themselves were formed were great precision.  

This github repository is devoted to reproducing the findings of "Autoencoders for Educational Assessment" and extending the research of the paper.  As many additional questions can be asked about using VAEs for uncovering latent student knowledge, I will cover many of the questions in the following sections.  

Replication of the Study
I used Tensorflow to recreate the code of the paper.  

The author has 1) replicated the findings of “Autoencoders for Educational Assessment,” 2) created a function to test different a) data and b) architectural assumptions for the VAE than those provided by the paper, 3) written additional hidden distribution to test, and 4) written a multilevel vae for testing subject where knowledge of one subject affects knowledge of another.  

Introduction
Autoencoders for Educational Assessment showed the viability of using VAEs to uncover the student understanding in item response theory models.  The hidden knowledge of students highly correlated to the true hidden knowledge that was simulated.  Additionally, the VAE was able to estimate facts about the composition of the test itself with high correlation to the ground truth.  
In the experiments given by the paper, the architecture of the VAE was as follows:
1.	 28 dim input
2.	10 dim hidden layer with sigmoid activation
3.	3 dim normal stochastic layer outputting 
a.	Statics of the stochastic function
b.	The stochastic output
4.	28 dim output layer with sigmoid activation
a.	Q-matrix is multiplied by the weight matrix to give interpretability.

The input and output layer both had 28 layers because the tests fed into the network had 28 questions.  The stochastic layer had 3 dimensions because the assessment tested 3 hidden knowledge traits.  The paper gave room for several extensions.  The author chose to focus on the following:
1)	How does model architecture affect quality?
2)	How much data is necessary for the VAE uncover both test and student data with high correlation to ground truth?  
3)	Are the predictions invariant to the distribution of the activation function?  
a.	Double exponential vs Normal
b.	Quantiles of gamma vs Normal 
i.	Bin the gammas into quantiles and match correlation with normal quantiles
4)	What happens if the student knowledge is nested?
a.	Some hidden knowledge creates others, i.e. Using algebra to solve a trig problem	
b.	 Some components have covariance. i.e. reading skill affects writing skill
5)	A future direction would be what to do if only a partially defined Q matrix is available.  
a.	Semi supervised learning to determine rest of Q-matrix


Replication. 
 The author was able to replicate the paper.  While the RMSE and MAPE of the author were lower than the origenal paper, the correlations where worse.

 The aut  

