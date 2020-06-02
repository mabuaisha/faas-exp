#!/bin/bash

set +xe

faas-exp get-stdev -s $1 -e warmfunction
faas-exp get-stdev -s $1
faas-exp get-stdev -s $1
