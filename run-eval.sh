echo "evaluate Eddy"
echo "unzip files"
python process_large_files.py decompress

python ./evaluation/run_eval.py --eval-reversed-code
python ./evaluation/run_eval.py --eval-lifting
python ./evaluation/run_eval.py --eval-name-inference
python ./evaluation/run_eval.py --eval-scalability
