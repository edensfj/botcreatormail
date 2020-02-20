for (( i = 0; i < 7; i++ )); do
	xterm -e 'while true; do python ./test.py; done'&
done
