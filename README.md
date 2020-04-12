# Cake Cutting

## Introduction

An 🍰 cutting algorithm, basically used for FCN batch generation. 
During the quarantine I want to eat some cake for afternoon tee 😭

Because of the algorithm will run in realtime service, so it shouldn't be some expensive algorithm like GA.
It should be simple and have an acceptable utilizing ratio.

## Algorithm 

### Problem
The problem can be defined as: 

- We have sort of matrixes, size is xi x yi.
- We have to cut them in pieces and arrange them in N containers. 
- The size limitation of the container is m x n. 
- We shouldn't rotate the pieces. 
- After cut them out, you have to copy it's boundary which width is k.

Basically, the form of the problem can be defined as:

- Give sort of padded matrixes (And their size)
- Give container size and boundary size k
- Return q containers.
    - Each containers have a list, the element is:
        - The `[s1:s2,s3:s4]` mapped to `[t1:t2,t3:t4]` (without padding)