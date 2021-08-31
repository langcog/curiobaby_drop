#load(here("models/model_data.RData")) # mdat, all_trials_mse, all_trials_mse_r, etc.
load(here("models/support_probability_fit_df.RData")) 

# r, R^2, SSE, SST, total variance / variance explained...oh, my!

# total variance in human (adult) data:
var(ad_df$chose_target) # .012
sd(ad_df$chose_target) # .109

# variance in model responses:
var(ad_df$Model_targ_prop) # .003
sd(ad_df$Model_targ_prop) # .056

# sum of squares total (SST)
SST = with(ad_df, sum((chose_target - 
       mean(chose_target))^2)) 
# 0.50

# AKA RSS (Residual Sum of Squares) - unexplained variability in the dataset
SSE = with(ad_df, sum((chose_target - Model_targ_prop)^2))

# SST = SSR + SSE, so SSR = SST - SSE


# Sum of Squares Regression (SSR)
# sum of the differences between the predicted value and the mean of the dependent variable
#SSR = SST - SSE # -.19..
# R^2 = SSR / SST
Rsq = SSR / SST # -.377
# compare to with(ad_df, cor(chose_target, Model_targ_prop)) # -.352..

#Fraction of Variance Unexplained:
#  FVU = VAR_err / VAR_tot


FVU = MSE(reg) / var(Y)

