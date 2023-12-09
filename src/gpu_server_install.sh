#!/bin/bash

mkdir /hy-tmp/LibriTTS
oss cp oss://LibriTTS/train-clean-100.tar.gz /hy-tmp/
oss cp oss://LibriTTS/dev-clean.tar.gz /hy-tmp/
cd /hy-tmp
tar -zxvf train-clean-100.tar.gz
tar -zxvf dev-clean.tar.gz
oss cp oss://LibriTTS/nltk_data.tar.gz /root/