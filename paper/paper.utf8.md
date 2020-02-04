---
#title: "Modeling children's intrinsically-motivated curiosity about object interactions"
#title: "Drop it like it's hot: Modeling children's curiosity about physical interactions"
#title: "A drop in the bucket: Progress towards modeling children's curiosity about physical interactions"
title: "What if you drop that? Modeling children's curiosity about physical interactions"
bibliography: library.bib
csl: apa6.csl
document-params: "10pt, letterpaper"

author-information: > 
    \author{{\large \bf Morton Ann Gernsbacher (MAG@Macc.Wisc.Edu)} \\ Department of Psychology, 1202 W. Johnson Street \\ Madison, WI 53706 USA
    \AND {\large \bf Sharon J.~Derry (SDJ@Macc.Wisc.Edu)} \\ Department of Educational Psychology, 1025 W. Johnson Street \\ Madison, WI 53706 USA}

abstract: >
     Curiosity is a fundamental driver of human behavior, and yet because of its open-ended nature 
     and the wide variety of behaviors it inspires in different contexts, it is remarkably difficult 
     to study in a laboratory context. A promising approach to developing and testing theories of 
     curiosity is to instantiate them in artificial agents that are able to act and explore in a 
     simulated environment, and then compare the behavior of these agents to humans exploring the 
     same stimuli. Here we propose a new experimental paradigm for examining children's--and curious
     AI agents'--curiosity about objects' physical interactions, using a task that is both open-ended
     enough to allow room for curiosity, but also constrained enough to make detailed behavioral 
     comparisons. We compare the choices of 51 children (2-6 years of age) to those of agents implementing 
     different types of curiosity, and find broad exploration, but also systematic preferences ...
    
keywords: >
    curiosity; novel objects; object interactions; intuitive physics
    
output: cogsci2016::cogsci_paper
#    includes:
#      in_header: preamble.tex
#final-submission: \cogscifinalcopy
---







# Introduction 

<!-- Curiosity is important... end with core question about what gives rise to curiosity. -->
Curiosity is a hallmark aspect of human intelligence. From infants exploring the objects in their environment to scientists exploring the frontiers of our solar system, humans are highly motivated to seek out new knowledge and experiences. However, although such exploratory behavior has long been recognized as a critical component of human learning [@james1983talks] and cognitive development [@Gopnik2009;@Piaget1952], formal theories that explain human curiosity and how it drives exploratory behavior have remained elusive [@Kidd2015]. Moreover, extant theories have rarely provided quantitatively precise enough predictions to be directly compared to empirical measurements of curiosity-driven behavior in humans.

The goal of the current paper is to help close this gap by proposing a framework for advancing our theoretical understanding of curiosity that combines three key ingredients: _first_, we present a computational theory of how a learner's knowledge state interacts with ongoing perceptual experiences to give rise to curiosity-driven exploratory behavior; _second_, we present an empirical investigation of the pattern of actions taken by children in a novel physical exploration task; and _third_, we evaluate the quantitative correspondence between the exploratory actions taken by an artificial agent that instantiates our computational theory and those taken by human children on the same set of tasks. 

Our computational theory is inspired by classic descriptive theories that posited that curiosity-driven behavior was the consequence of attentional capture by novel stimuli [e.g., @Berlyne1954; @Fantz1964], as well as theories providing qualitative explanations for curiosity-driven behavior as the result of learners' preferences for stimuli that are "moderately discrepant" in relation to their current knowledge state, and thereby provide opportunities to learn [@Kinney1976]. Recent studies have provided empirical support for this basic idea: XX-old infants are sensitive to stimulus complexity and prefer to look at moderately complex stimuli rather than overly simple or overly complex stimuli; @Kidd2012; @Kidd2014].
According to these theories, curiosity-driven behavior reflects a gap between the learner's knowledge and the state of the world [@Loewenstein1994], and thus they predict that as a learner gains additional knowledge, their preferences will shift toward more complex stimuli [@Dember1957].
Although these theories have provided important qualitative insights, one of their major limitations is that they do not provide precise ways to characterize a learner's current knowledge state, how physical states of the world are represented in their mind, nor how discrepancies between a learner's knowledge and such states are compared.  
Our approach leverages theory and insights from reinforcement learning (RL), including the value of mechanisms that equip RL agents with "intrinsic motivation" — a drive to explore the state space even when rewards are sparse or absent, and favor actions with uncertain outcomes, because they may result in the discovery of new policies with high expected values [@Schmidhuber2010].
Our modeling approach is resonant with recent work that has instantiated such intrinsic-motivation mechanisms in robots to help them learn robust ways to predict physical events in the world world [@Oudeyer2007; @Oudeyer2013], although this work typically involves pretraining models on a separate physical prediction task before implementing curosity-driven learning, and has not yet been directly compared to human behavior in the same prediction tasks.

Our empirical study is motivated by a large body of prior work in developmental psychology investigating the development of knowledge about physical objects, their properties, and how they interact (CITE), thus making exploration of physical objects a natural choice of domain to explore the implications of our theory. However, the measures used in this literature have typically been coarse-grained with respect to infant's and children's physical knowledge, and thus do not specify or constrain which events might moderately discrepant from this knowledge. For instance, a typical measure of physical curiosity has been longer looking times to surprising events than to expected events (e.g., objects appearing to pass through a wall; @Stahl2015; @Baillargeon2007). Other work that has investigated exploratory behavior in children have used more granular measures, such as counting the number of functions discovered while playing with novel and complex toy [e.g., @Cook2011; @Bonawitz2012; @Gweon2014]. Moreover, these studies have yet to directly constrain theories that predict which functions children will discover, and in what sequence. What both of the standard looking-time and toy-exploration measures fail to capture when characterizing children's curiosity are the ways in which children actively learn by intervening on the world and observing the consequences of their actions [@Gopnik2009; @gureckis2012self]. To address these limitations, we developed a novel physical exploration task in which children choose which series of physical experiments to perform and observe the results of each in real time. 

<!-- High-level statement of our approach -->
In sum, this paper presents a unified paradigm for advancing theories of curiosity and its role in guiding the development of knowledge about the physical world. We present: (1) a computational theory of intrinsic motivation instantiated in an artificial reinforcement-learning agent that explores a simulated 3D environment; (2) a novel dataset that measures children's actions in a novel physical exploration task; and (3) quantitative comparisons between the actions taken by the artificial agent and children on the same set of tasks. Overall, our approach of coordinating the development of task-performing computational models and detailed measurement of human action selection on the same tasks has the promise to lead to more robust and precise theories of how curiosity guides cognitive development.

<!-- presents learners (children or the agent) with a set of objects from which they can select one to drop in a bin containing a set of target objects, with the potential to create one or more collisions during the drop. -->

<!-- What we've learned from prior theoretical work, and how it falls short -->

<!-- A limitation of past theories of curiosity is that they are large part verbal descriptions, without formal, testable, mechanisms. -->
<!-- An exception to this: @Schmidhuber2010 and @Oudeyer2013 --similar but different, and critically not evaluated against same children's behavior in the same situations -->

<!-- What we've learned from prior behavioral work, and how our approach is different -->

<!-- Looking time people: @Baillargeon2007 and other studies of infants' surprisal at physical events (occlusion, containment,  -->
<!-- Ullman -- not about curiosity, but about intuitive physics learning from observation in simplified 2D domains (e.g., colliding hockey pucks)  -->


<!-- Highlight main contributions of the paper -->

<!-- One rich domain that young children are in the midst of learning about is the properties and affordances of physical objects.  -->
<!-- A study of 9- to 16-month-olds found that infants' violation of expectations about a novel toy's hidden properties (e.g., making a sound) drives them to explore similar toys for longer [@Baldwin1993]. -->

## Computational Models of Curiosity

Building on prior work that showed deep neural networks are capable of learning forward and inverse physical dynamics (i.e., "intuitive physics") from images when given the ability to "poke" the objects in the scene [@Agrawal2016], we use and extend a deep RL architecture for constructing intrinsically-motivated artificial agents introduced in @Haber2018learning.
This agent's behavior is driven by two interacting neural networks: a *world-model* and a *self-model*, which are trained simultaneously. 
The problem of the world-model is to predict the consequences of the agent's actions, through estimation of either the forward or inverse dynamics. 
The self-model attempts to learn to predict the errors of the world-model. 
The agent can use the predictions of the self-model to implement a variety of curiosity policies for choosing actions, for example to pick actions that it believes will adversarially challenge the state of its world-model.

(Full model description here, or just a teaser? Maybe also make the below a joint "Paradigm" section, then human behavior, model behavior and comparison)

# Experiment

## Method

### Participants
Participants were 53 children recruited from the Children's Discovery Museum of San Jose and Bing Nursery School.
Participant exclusions were made based on cases where i) the participant did not complete more than half of the study play session or ii) the parent did not consent for video recording of study. 
After exclusions, results from 51 were analyzed, including 6 2-year-olds, 18 3-year-olds, 14 4-year-olds, 12 5-year-olds, and 2 6-year-olds.\footnote{The collected sample differed from our planned sample size of 16 each of 3-, 4-, and 5-year-olds due to availability of participants (see preregistration: https://osf.io/37qvb/).}

### Materials



Stimuli were 3D-printed plastic objects produced using Blender 3D-modeling software. 
The nine objects, depicted in Figure 1, were bowl, cone, dumbbell, octahedron, pentagon (pentagonal prism), pipe, pyramid, torus, and triangular prism.
The printed objects were all yellow, rigid plastic material and designed to fit comfortably in a child's hand (dimension range: 3.8-10.1 cm). 

The set of 9 objects were divided into 3 subsets (A = {pyramid, torus, triangular prism}, B = {cone, octahedron, pipe}, and C = {bowl, dumbbell, pentagon}). 
These subsets served as sets (A, B, C) of target or drop objects in six successive blocks of 2 trials, making a total of 12 trials per participant.
For example, in Order 1, in the first block of 2 trials, set A served as the target objects from which the child chose to drop on the target objects (set B).
The target:drop block sequence for Order 1 was A:B, B:C, C:A, A:C, B:A, C:B. The sequence for Order 2 was the reverse of Order 1: C:B, B:A, A:C, C:A, B:C, A:B. Participants were assigned to condition in counterbalanced order.

Target objects were placed in a circular bin (25 in diameter x 10 in height). 
The bin was divided with tape into sections of equal area, and one target object from the appropriate set was placed in the center of each third. 
Drop objects were presented to participants on a table at approximately eye level.

\begin{CodeChunk}
\begin{figure}[h]

{\centering \includegraphics{figs/fig1-sets-1} 

}

\caption[Sets of 3D objects used for dropping and as targets]{Sets of 3D objects used for dropping and as targets.}\label{fig:fig1-sets}
\end{figure}
\end{CodeChunk}

### Procedure

After the parent provided informed consent, children were assigned to Order 1 or Order 2. Participants were assigned to condition in counterbalanced order.
We introduced children to a set of 3D-printed toy objects ("blocks"). 
The child played a game where they could pick which of three blocks to drop in a bin containing three other blocks, to see what happens. 
An example trial is illustrated in Figure 2.
We then swapped target/drop blocks, based on assigned order sequence, and asked the child to do the same selection and dropping a dozen times. 
Finally, we asked the child to build a "cool" tower with any of the toy blocks for about one minute.

Based on piloting, we estimated the activity would would only require five minutes to complete. 
In both conditions, a video camera was used to record the play session from an angle above the bin, to show child's block selection and drop location as well as child's completed tower. 
After child notified the researcher that they were finished building their tower, the session was completed and camera was turned off. 

\begin{CodeChunk}
\begin{figure}[h]

{\centering \includegraphics{figs/fig2-task-1} 

}

\caption[Example trial in which the participant chose to drop the pyramid from set A on the pentagonal prism in the target set (B)]{Example trial in which the participant chose to drop the pyramid from set A on the pentagonal prism in the target set (B).}\label{fig:fig2-task}
\end{figure}
\end{CodeChunk}

### Drop Coding Procedure

Each session's video was manually coded for drop object choice and target location per trial.
Drop choice was defined as the participant's selection of one of the three available drop set objects, to be dropped into the bin containing the set of the three potential target objects. 
The bin was divided into three wedge-shaped sections of equal area, demarcated with a thin black line.
One of the target set's objects was placed in the middle of each section of the bin. 
Target location was defined as either i) the object the dropped object collided with, ii) a collision with empty space inside the bin, or iii) falling outside the bin.
If the dropped object collided with empty space, we also recorded the target object it landed closest to. 
We also recorded events where the dropped object bounced from empty space or a target object then collided with other target object(s), including the number of collisions and identity of the target(s) hit.

Trials were excluded if the child i) dropped an object outside the bin, ii) touched target object(s) prior to a drop, iii) dropped an object during set change, iv) selected more than one object to drop, or iv) dropped (or threw) object from too high (>1.5 m). 
Trials were also excluded if the experimenter made a mistake (e.g., used the wrong stimulus set or repeated a trial more than twice).


## Results



We first examine children's choice of drop objects and target objects to determine if children were choosing randomly, or had consistent preferences for some objects. 
We used chi-square test of independence on participants' drop choices from each set of objects (A, B, C).
Participants' drop choices from set A significantly differed from chance ($X^2$(2, N=189) = 19.17, p<.001), as did drop choices from set B ($X^2$(2, N=201) = 8.27, p=0.016).
Participants' drop choices from set C did not significantly differ from chance ($X^2$(2, N=194) = 5.76, p=0.056).
Table 1 shows a summary of participants' choice of drop objects per set.
It is apparent that from set A, participants preferentially chose to drop the torus rather than the triangular prism (trig prism) or pyramid. 
For set B, children more often avoided the octahedron, and instead chose the pipe or cone.
Set C showed more equal rates of drop choice, but the dumbbell was somewhat more popular than the pentagonal prism (pentagon).

What objects did children target with their drops?
First, we noted that children very often did not hit any target object: on 57% of trials, participants' dropped over empty space.
It is not possible to determine whether children intentionally missed the available target objects, or whether their misses were errors due to noise in fine motor control.
If the misses were just due to poor motor control, one might expect the number of misses by age to decrease, as older children should have better motor control.
However, there was no significant correlation between children's individual proportion of "missed" targets and their age (*r*(51) = .20, *p* = .141), which may suggest that dropping objects on empty space may be of interest to children of all ages, and not solely determined by a lack of fine motor control.
Thus, we first analyze drops where participants' dropped objects directly hit the target objects.
Chi-square tests of children's target collisions revealed that they did not significantly differ from chance for set A ($X^2$(2, N=76) = 0.34, p=0.843), B ($X^2$(2, N=84) = 1.14, p=0.565), or C ($X^2$(2, N=92) = 1.98, p=0.372).
Table 2 shows a summary of participants' choice of target objects per set.

Finally, we examine a more lenient analysis children's choice of target location (i.e., the identity of the closest target), regardless of whether there was a collision of drop and target objects.
Chi-square tests of children's target collisions once more found that they did not significantly differ from chance for set A ($X^2$(2, N=194) = 2.3, p=0.317), B ($X^2$(2, N=186) = 0.23, p=0.893), or C ($X^2$(2, N=193) = 2, p=0.368).
Table 3 shows a summary of participants' choice of target locations per set.

In summary, children showed some consistent preferences in their choice of objects to drop from each set, but no systematic preference for targeting particular objects.
We now investigate whether there were interactions of drop objects and targets that children found particularly appealing. [ToDo: big chisq test?]

Finally, we analyze how exploratory children were in their responses: across the 12 trials, what proportion of the 9 available objects did each child utilize as drop objects? What proportion of the objects were targeted?

\begin{table}[H]
\centering
\begin{tabular}{rll}
  \hline
 & Set & Drop Object (N) \\ 
  \hline
1 & A & trig prism (45), pyramid (53), torus (91) \\ 
  2 & B & octahedron (48), pipe (74), cone (79) \\ 
  3 & C & pentagon (50), bowl (67), dumbbell (77) \\ 
   \hline
\end{tabular}
\caption{Children's drop object choices by set.} 
\end{table}


\begin{table}[H]
\centering
\begin{tabular}{rll}
  \hline
 & Set & Target Object (N) \\ 
  \hline
1 & A & pyramid (23), trig prism (26), torus (27) \\ 
  2 & B & cone (24), octahedron (28), pipe (32) \\ 
  3 & C & pentagon (27), dumbbell (28), bowl (37) \\ 
   \hline
\end{tabular}
\caption{Children's target object choices by set.} 
\end{table}


\begin{table}[H]
\centering
\begin{tabular}{rll}
  \hline
 & Set & Target Location (N) \\ 
  \hline
1 & A & trig prism (57), torus (63), pyramid (74) \\ 
  2 & B & octahedron (60), pipe (61), cone (65) \\ 
  3 & C & dumbbell (56), bowl (65), pentagon (72) \\ 
   \hline
\end{tabular}
\caption{Children's target location choices by set.} 
\end{table}










\begin{CodeChunk}
\begin{figure*}[h]

{\centering \includegraphics{figs/combined-fig-1} 

}

\caption[Relative frequency of objects 1) chosen as objects for dropping, 2) hit as targets (pink dots represent hitting empty space), and 3) whose drop location was closest to a target object, as a function of target/drop set pairing]{Relative frequency of objects 1) chosen as objects for dropping, 2) hit as targets (pink dots represent hitting empty space), and 3) whose drop location was closest to a target object, as a function of target/drop set pairing.}\label{fig:combined-fig}
\end{figure*}
\end{CodeChunk}


Figure 4 shows participants' mean proportion of unique objects dropped as a function of age.
Children of all ages sampled approximately equal proportions of the objects for dropping--roughly 70%, which is close to the 75% that would be expected if they were selected by chance (9 unique object occurring across 12 trials).

\begin{CodeChunk}
\begin{figure}[H]

{\centering \includegraphics{figs/unique-drop-objects-1} 

}

\caption[Proportion of unique objects selected by participants]{Proportion of unique objects selected by participants. Error bars show boostrapped 95\% confidence intervals.}\label{fig:unique-drop-objects}
\end{figure}
\end{CodeChunk}





### Tower Task Results

\begin{CodeChunk}
\begin{CodeOutput}
[1] 61
\end{CodeOutput}
\begin{CodeOutput}
[1] 51
\end{CodeOutput}
\end{CodeChunk}

1. height x continuous age
First we examine tower height as a function of age. Yes we find tower height increases with age.
\begin{CodeChunk}
\begin{CodeOutput}

	Pearson's product-moment correlation

data:  hum$height_tallest and hum$age_rounded
t = 2.2751, df = 44, p-value = 0.02783
alternative hypothesis: true correlation is not equal to 0
95 percent confidence interval:
 0.03768535 0.56181861
sample estimates:
      cor 
0.3244341 
\end{CodeOutput}
\end{CodeChunk}

\begin{CodeChunk}

\includegraphics{figs/unnamed-chunk-2-1} \end{CodeChunk}

2. support x supported (counts)
\begin{CodeChunk}
\begin{CodeOutput}
[1] "bowl"       "octahedron"
[1] "pipe"     "pentagon" "cone"    
[1] "octahedron" "pentagon"   "bowl"      
[1] "bowl"     "torus"    "dumbbell"
[1] "bowl"       "torus"      "cone"       "pipe"       "trig prism"
[1] "torus"    "pentagon"
[1] "pentagon"   "pipe"       "pyramid"    "trig prism" "cone"      
[1] "torus"      "pipe"       "trig prism"
[1] "pipe"    "torus"   "pyramid" "bowl"   
[1] "pentagon" "pyramid" 
[1] "pipe"       "octahedron" "cone"       "torus"      "bowl"      
[1] "octahedron" "torus"      "bowl"      
[1] "torus" "pipe"  "cone" 
[1] "cone" "pipe" "bowl"
[1] "bowl"    "pyramid" "cone"   
[1] "pipe"     "pentagon" "cone"     "torus"    "bowl"     "pyramid" 
[1] "torus"      "cone"       "pipe"       "pentagon"   "trig prism"
[1] "pipe"     "pentagon" "cone"     "torus"    "bowl"     "pyramid" 
[1] "pentagon" "cone"     "bowl"     "torus"    "dumbbell"
[1] "pentagon"   "trig prism" "torus"      "pyramid"   
[1] "pipe"       "octahedron"
[1] "pentagon" "pipe"     "cone"    
[1] "pentagon" "pipe"     "torus"    "bowl"     "cone"    
[1] "torus" "bowl" 
[1] "pipe"    "torus"   "bowl"    "pyramid"
[1] "pipe"     "pentagon" "torus"    "bowl"    
[1] "pipe"     "torus"    "bowl"     "dumbbell"
[1] "torus"    "pipe"     "dumbbell"
[1] "pentagon" "cone"    
[1] "torus" "bowl" 
[1] "pipe"       "torus"      "bowl"       "pentagon"   "octahedron"
[6] "pyramid"   
[1] "pentagon" "pipe"     "torus"   
[1] "pentagon"   "torus"      "pipe"       "trig prism"
[1] "torus"      "trig prism" "pentagon"   "pyramid"    "torus"     
[6] "octahedron" "bowl"      
[1] "torus" "cone"  "bowl" 
[1] "cone"     "torus"    "bowl"     "pentagon"
[1] "pipe"     "torus"    "dumbbell"
[1] "bowl"  "pipe"  "torus" "cone" 
[1] "pipe"       "torus"      "pentagon"   "trig prism"
[1] "pentagon" "bowl"     "pipe"     "torus"    "pyramid" 
[1] "trig prism" "pyramid"   
[1] "pipe"     "torus"    "cone"     "pentagon"
[1] "torus"    "pipe"     "pentagon" "bowl"     "cone"    
[1] "octahedron" "pipe"       "dumbbell"  
[1] "torus"    "pipe"     "dumbbell"
[1] "cone"       "torus"      "pipe"       "octahedron"
[1] "pipe" "bowl" "cone"
[1] "pipe"       "trig prism"
[1] "pipe" "cone"
[1] "torus" "pipe"  "cone"  "bowl" 
[1] "torus"      "bowl"       "pipe"       "pentagon"   "trig prism"
[6] "cone"      
[1] "bowl" "cone"
[1] "trig prism" "pentagon"  
[1] "octahedron" "bowl"       "dumbbell"  
[1] "pentagon"   "pipe"       "trig prism"
\end{CodeOutput}

\includegraphics{figs/unnamed-chunk-3-1} \end{CodeChunk}

3. support x supported (probabilities)
pr (supported object | support object)
\begin{CodeChunk}
\begin{CodeOutput}
[1] "bowl"       "octahedron"
[1] "pipe"     "pentagon" "cone"    
[1] "octahedron" "pentagon"   "bowl"      
[1] "bowl"     "torus"    "dumbbell"
[1] "bowl"       "torus"      "cone"       "pipe"       "trig prism"
[1] "torus"    "pentagon"
[1] "pentagon"   "pipe"       "pyramid"    "trig prism" "cone"      
[1] "torus"      "pipe"       "trig prism"
[1] "pipe"    "torus"   "pyramid" "bowl"   
[1] "pentagon" "pyramid" 
[1] "pipe"       "octahedron" "cone"       "torus"      "bowl"      
[1] "octahedron" "torus"      "bowl"      
[1] "torus" "pipe"  "cone" 
[1] "cone" "pipe" "bowl"
[1] "bowl"    "pyramid" "cone"   
[1] "pipe"     "pentagon" "cone"     "torus"    "bowl"     "pyramid" 
[1] "torus"      "cone"       "pipe"       "pentagon"   "trig prism"
[1] "pipe"     "pentagon" "cone"     "torus"    "bowl"     "pyramid" 
[1] "pentagon" "cone"     "bowl"     "torus"    "dumbbell"
[1] "pentagon"   "trig prism" "torus"      "pyramid"   
[1] "pipe"       "octahedron"
[1] "pentagon" "pipe"     "cone"    
[1] "pentagon" "pipe"     "torus"    "bowl"     "cone"    
[1] "torus" "bowl" 
[1] "pipe"    "torus"   "bowl"    "pyramid"
[1] "pipe"     "pentagon" "torus"    "bowl"    
[1] "pipe"     "torus"    "bowl"     "dumbbell"
[1] "torus"    "pipe"     "dumbbell"
[1] "pentagon" "cone"    
[1] "torus" "bowl" 
[1] "pipe"       "torus"      "bowl"       "pentagon"   "octahedron"
[6] "pyramid"   
[1] "pentagon" "pipe"     "torus"   
[1] "pentagon"   "torus"      "pipe"       "trig prism"
[1] "torus"      "trig prism" "pentagon"   "pyramid"    "torus"     
[6] "octahedron" "bowl"      
[1] "torus" "cone"  "bowl" 
[1] "cone"     "torus"    "bowl"     "pentagon"
[1] "pipe"     "torus"    "dumbbell"
[1] "bowl"  "pipe"  "torus" "cone" 
[1] "pipe"       "torus"      "pentagon"   "trig prism"
[1] "pentagon" "bowl"     "pipe"     "torus"    "pyramid" 
[1] "trig prism" "pyramid"   
[1] "pipe"     "torus"    "cone"     "pentagon"
[1] "torus"    "pipe"     "pentagon" "bowl"     "cone"    
[1] "octahedron" "pipe"       "dumbbell"  
[1] "torus"    "pipe"     "dumbbell"
[1] "cone"       "torus"      "pipe"       "octahedron"
[1] "pipe" "bowl" "cone"
[1] "pipe"       "trig prism"
[1] "pipe" "cone"
[1] "torus" "pipe"  "cone"  "bowl" 
[1] "torus"      "bowl"       "pipe"       "pentagon"   "trig prism"
[6] "cone"      
[1] "bowl" "cone"
[1] "trig prism" "pentagon"  
[1] "octahedron" "bowl"       "dumbbell"  
[1] "pentagon"   "pipe"       "trig prism"
\end{CodeOutput}

\includegraphics{figs/unnamed-chunk-4-1} \end{CodeChunk}

4. base and top distribution
\begin{CodeChunk}

\includegraphics{figs/unnamed-chunk-5-1} \end{CodeChunk}

<!-- We find that towers vary in i) height, ii) stacks, and iii) components. -->

<!-- 1. height x age -->
<!-- -First we examine tower height, of the tallest stack, as a function of age. We find tower height increases with age (cor.test). -->

<!-- 2a. number stacks x age -->
<!-- -Number of stacks y/ n correlate with age. -->
<!-- -what is "cool": younger and use of horizontal/adjacent tower building -->

<!-- 2b. number collapses x age = intuitive physics (tower stability) -->
<!-- -Hight and number of stacks due to stability issue. -->
<!-- -Number of collapses -->

<!-- 3. The structural components of the towers -->
<!-- -support x supported -->
<!-- -drop object probabilities correlate with objects used in tower? -->
<!-- -first base selection as proxy of most interesting object -->
<!-- -base and top distribution -->



# Model


## Random Policy


## Noncurious Policy


## Antagonistic Curiosity Policy


## Results


\begin{CodeChunk}
\begin{figure*}[h]

{\centering \includegraphics{figs/combined-model-fig-1} 

}

\caption[Relative frequency of objects chosen by each model as objects for dropping (first row), and objects hit as targets (second row]{Relative frequency of objects chosen by each model as objects for dropping (first row), and objects hit as targets (second row; pink dots represent hitting empty space), as a function of target/drop set pairing.}\label{fig:combined-model-fig}
\end{figure*}
\end{CodeChunk}

## Comparison with Children



# Discussion 



# Acknowledgements

This work was funded by HAI seed grant #. 
We thank X and Y for helpful comments.

# References 



\setlength{\parindent}{-0.1in} 
\setlength{\leftskip}{0.125in}
\noindent
