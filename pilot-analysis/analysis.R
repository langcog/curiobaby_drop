
d = read.csv2("curiobaby_drop-pilot-7-22-2019.csv", sep=',', header=T)
require(tidyverse)
require(tidyboot)

# not parsing DropOrientation and Notes correctly (last two columns)

dd = subset(d, Exclude=="N" & TrialType=="Normal") #  
length(unique(dd$SID)) # 23 subjects

md <- dd %>% group_by(SID) %>% summarise(max=max(Trial))
pdf("hist_trials_completed.pdf", width=4, height=4)
hist(md$max, main='', xlab="Number of Trials Completed", col="lightblue")
abline(v=median(md$max), lty='dashed') # 11
dev.off()

dd$DropChoice = as.character(dd$DropChoice)
dd$DropLocation = as.character(dd$DropLocation)

dd$Age = as.numeric(as.character(dd$Age))
dd$AgeYr = round(dd$Age)


ch_tr <- dd %>% 
  group_by(Trial, DropChoice) %>%
  summarise(n = n()) %>%
  mutate(freq = n / sum(n))# %>%
  #group_by(Trial, DropChoice) %>% 
  #tidyboot_mean(freq) 

g <- ggplot(ch_tr, aes(x=Trial, y=freq, shape=DropChoice, color=DropChoice, size=n)) + geom_point(alpha=.8) + 
  #geom_linerange(aes(ymin = ci_lower, ymax = ci_upper)) +
  xlab("Trial") + ylab("Drop Choice") +
  langcog::scale_fill_solarized() + ggthemes::theme_few()
ggsave("drop_choice_by_trial.pdf", width=4.5, height=4)

loc_tr <- dd %>% group_by(Trial, DropLocation) %>% 
  summarise(n = n()) %>%
  mutate(freq = n / sum(n))

g <- ggplot(loc_tr, aes(x=Trial, y=freq, shape=DropLocation, color=DropLocation, size=n)) + geom_point(alpha=.8) + 
  xlab("Trial") + ylab("Drop Location") +
  langcog::scale_fill_solarized() + ggthemes::theme_few()
ggsave("drop_location_by_trial.pdf", width=4.5, height=4)


ch_age <- dd %>% group_by(AgeYr, DropChoice) %>% 
  summarise(n = n()) %>%
  mutate(freq = n / sum(n)) 

g <- ggplot(ch_age, aes(x=AgeYr, y=freq, color=DropChoice)) + 
  geom_line() + geom_point(alpha=.8, aes(size=n, shape=DropChoice)) + 
  xlab("Age") + ylab("Proportion Drop Choice") + ylim(0,.6) +
  langcog::scale_fill_solarized() + ggthemes::theme_few()
ggsave("drop_choice_by_age.pdf", width=4.5, height=4)


# Drop Choice x Location heatmap
ch_loc <- dd %>% group_by(DropChoice, DropLocation) %>% 
  summarise(n = n()) %>%
  mutate(freq = n / sum(n))

g <- ggplot(ch_loc, aes(x=DropLocation, y=DropChoice)) + geom_tile(aes(fill=freq)) + 
  scale_fill_gradient(low = "white", high = "steelblue") +
  xlab("Drop Location") + ylab("Drop Choice") +
  ggthemes::theme_few()
ggsave("drop_choice_by_location.pdf", width=5.5, height=4.0)


# look at sequence of choices, and 
# try also to look at drop==target across ages

table(dd$DropChoice)
#    bigblock      golf   pingpong smallblock 
#        52         84         56         46 
table(dd$DropChoice) / sum(table(dd$DropChoice))

table(dd$DropLocation)
# bigblock   golf   pingpong   smallblock   space 
#      29     21        32         19        137  (58% space)
table(dd$DropLocation) / sum(table(dd$DropLocation)) 

table(dd$DropChoice, dd$DropLocation)
#             bigblock golf pingpong smallblock space
#bigblock         11    3        6          2    30
#golf              6   14       11          5    48
#pingpong          7    1       10          2    36
#smallblock        5    3        5         10    23