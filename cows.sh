echo "Hi, i guessed a secret number _ _ _ _.
Try to quess it.
If the matching digits are in their right positions, they are "bulls",
if in different positions, they are "cows"."
DIV=$((9+1))
A=$(($RANDOM%$DIV))
B=$A
C=$A
D=$A
while [ $B -eq $A ]
do
	B=$(($RANDOM%$DIV))
done
while [ $C -eq $A -o $C -eq $B ]
do
	C=$(($RANDOM%$DIV))
done
while [ $D -eq $A -o $D -eq $B -o $D -eq $C ]
do
	D=$(($RANDOM%$DIV))
done
cows=0
bulls=0
while [ $cows -ne 4 ]
do
	cows=0
	bulls=0
	read -p "i think it is
(please print digits separeted by space): " var1 var2 var3 var4
	while [ $var1 -eq $var2 -o $var1 -eq $var3 -o $var1 -eq $var4 -o $var2 -eq $var3 -o $var2 -eq $var4 -o $var3 -eq $var4 ]
	do
		read -p "numbers should be different, baby
(please print digits separeted by space): " var1 var2 var3 var4
	done
	if [ $var1 -eq $A ]
	then
		cows=$((cows+1))
	fi
	if [ $var2 -eq $B ]
	then
		cows=$((cows+1))
	fi
	if [ $var3 -eq $C ]
	then
		cows=$((cows+1))
	fi
	if [ $var4 -eq $D ]
	then
		cows=$((cows+1))
	fi
	if [ $var1 -eq $B -o $var1 -eq $C -o $var1 -eq $D ]
	then
		bulls=$((bulls+1))
	fi
	if [ $var2 -eq $A -o $var2 -eq $C -o $var2 -eq $D ]
	then
		bulls=$((bulls+1))
	fi
	if [ $var3 -eq $B -o $var3 -eq $A -o $var3 -eq $D ]
	then
		bulls=$((bulls+1))
	fi
	if [ $var4 -eq $B -o $var4 -eq $C -o $var4 -eq $A ]
	then
		bulls=$((bulls+1))
	fi
	echo "cows are" $cows
	echo "bulls are" $bulls
done
echo "CONGRATS, BABY!"
