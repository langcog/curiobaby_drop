require(here)
require(tidyverse)
require(tidyboot)

#hdp = read.csv2("human-data/curiobaby_drop-data - drop pilot.csv", sep=',', header=T)
hd = read.csv2("human-data/curiobaby_drop-data - drop exp.csv", sep=',', header=T)

#length(unique(hdp$SID)) # 8 subjects
length(unique(hd$SID)) # 53

#cols = intersect(names(hdp), names(hd))
#hum = rbind(hdp[,cols], hd[,cols]) # 609

hum = subset(hd, Exclude!="Y") # 577 trials

length(unique(hum$SID)) # 51 subjects

md <- hum %>% group_by(SID) %>% summarise(max=max(Trial)) %>% arrange(max)


hum$DropChoice = as.character(hum$DropChoice)
hum$DropLocation = as.character(hum$DropLocation)

hum$Age = as.numeric(as.character(hum$Age))


ch_tr <- hum %>% 
  group_by(Trial, DropChoice) %>%
  summarise(n = n()) %>%
  mutate(freq = n / sum(n)) %>%
  filter(Trial < 13) # 1 incorrectly-coded trial - fixing
  #group_by(Trial, DropChoice) %>% 
  #tidyboot_mean(freq) 

ch_tr$DropChoice <- as.factor(ch_tr$DropChoice)
g <- ggplot(ch_tr, aes(x=Trial, y=freq, shape=DropChoice, color=DropChoice, size=n)) + geom_point(alpha=.8) +
  scale_shape_manual(values=10:19) +
  #geom_linerange(aes(ymin = ci_lower, ymax = ci_upper)) +
  xlab("Trial") + ylab("Drop Choice") +
  langcog::scale_fill_solarized() + ggthemes::theme_few()
ggsave("drop_choice_by_trial.pdf", width=4.5, height=4.5)

loc_tr <- hum %>% group_by(Trial, DropLocation) %>% 
  summarise(n = n()) %>%
  mutate(freq = n / sum(n)) %>%
  filter(Trial < 13)

g <- ggplot(loc_tr, aes(x=Trial, y=freq, shape=DropLocation, color=DropLocation, size=n)) + geom_point(alpha=.8) + 
  xlab("Trial") + ylab("Drop Location") +
  scale_shape_manual(values=10:22) +
  langcog::scale_fill_solarized() + ggthemes::theme_few()
ggsave("drop_location_by_trial.pdf", width=4.5, height=4.5)


ch_age <- hum %>% group_by(Age, DropChoice) %>% 
  summarise(n = n()) %>%
  mutate(freq = n / sum(n)) 

g <- ggplot(ch_age, aes(x=Age, y=freq, color=DropChoice)) + 
  geom_line() + geom_point(alpha=.8, aes(size=n, shape=DropChoice)) + 
  scale_shape_manual(values=10:19) +
  xlab("Age") + ylab("Proportion Drop Choice") + ylim(0,.6) +
  langcog::scale_fill_solarized() + ggthemes::theme_few()
ggsave("drop_choice_by_age.pdf", width=4.5, height=4.5)


# Drop Choice x Location heatmap
ch_loc <- hum %>% group_by(DropChoice, DropLocation) %>% 
  summarise(n = n()) %>%
  mutate(freq = n / sum(n))

g <- ggplot(ch_loc, aes(x=DropLocation, y=DropChoice)) + geom_tile(aes(fill=freq)) + 
  scale_fill_gradient(low = "white", high = "steelblue") +
  xlab("Drop Location") + ylab("Drop Choice") +
  ggthemes::theme_few()
ggsave("drop_choice_by_location.pdf", width=10, height=7.0)


# look at sequence of choices, and 
# try also to look at drop==target across ages

sort(table(hum$DropChoice), decreasing=T)
#    bigblock      golf   pingpong smallblock 
#        52         84         56         46 
table(hum$DropChoice) / sum(table(hum$DropChoice))

sort(table(hum$DropLocation), decreasing=T)
# space   bowl   cone  dumbbell   pipe trig prism  pyramid  octahedron  torus  pentagon  boundary  dumbbell   outside
#  308     38     31       31      30         30      28         27      24       22      6          1          1 
table(hum$DropLocation) / sum(table(hum$DropLocation)) # 53% space

table(hum$DropChoice, hum$DropLocation)