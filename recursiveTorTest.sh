for (( i = 0; i < 12; i++ )); do
	xterm -e 'while true; do python ./test.py; done'&
done
