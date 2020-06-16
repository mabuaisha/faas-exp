#!/bin/bash

faas-exp aggregate -s ~/Master/Third\ Year/Second\ Semster/Thesis/result/exp-result/k8s -d ~/Master/Third\ Year/Second\ Semster/Thesis/faas-exp/result/k8s
faas-exp aggregate -s ~/Master/Third\ Year/Second\ Semster/Thesis/result/exp-result/swarm -d ~/Master/Third\ Year/Second\ Semster/Thesis/faas-exp/result/swarm
faas-exp aggregate -s ~/Master/Third\ Year/Second\ Semster/Thesis/result/exp-result/nomad -d ~/Master/Third\ Year/Second\ Semster/Thesis/faas-exp/result/nomad -e warmfunction
