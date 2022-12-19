#!/bin/bash

curl -F "file=@./test_files/11sec.wav" localhost:8000/files/
curl -F "file=@./test_files/24bit.wav" localhost:8000/files/
curl -F "file=@./test_files/32bit_float.wav" localhost:8000/files/
curl -F "file=@./test_files/adpcm.wav" localhost:8000/files/
curl -F "file=@./test_files/correct.wav" localhost:8000/files/
curl -F "file=@./test_files/unsigned8bit.wav" localhost:8000/files/
