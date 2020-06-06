#!/bin/bash

set +xe

faas-exp get-stdev -s ~/Master/Third\ Year/Second\ Semster/Thesis/result/exp-result/nomad -e warmfunction
faas-exp get-stdev -s ~/Master/Third\ Year/Second\ Semster/Thesis/result/exp-result/swarm
