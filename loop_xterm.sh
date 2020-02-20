for (( i = 0; i < 12; i++ )); do
	xterm -e 'sh sh_recursion.sh'&
done
