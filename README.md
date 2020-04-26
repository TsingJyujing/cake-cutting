# Cake Cutting

[![CircleCI](https://circleci.com/gh/TsingJyujing/cake-cutting.svg?style=svg)](https://circleci.com/gh/TsingJyujing/cake-cutting)

## Introduction

An 🍰 cutting algorithm, basically used for FCN batch generation. 
(During the quarantine I want to eat some cake for afternoon tee 😭)

Because of the algorithm will run in realtime service, so it shouldn't be some expensive algorithm like GA.
It should be simple and have an acceptable utilizing ratio, finally we only used greedy algorithm.

## Algorithm 

1. Corp the images which size larger than container by container's size
2. Get some bars fit width or height, and try to combine them together.
3. For the rest pieces: 
    1. try to fill them in rest part of fit width/height containers
    2. Create new containers to place them

### Visualization

Here's an [example](visualization.ipynb) of how it works.
