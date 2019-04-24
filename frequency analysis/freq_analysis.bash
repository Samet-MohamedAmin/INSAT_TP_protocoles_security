#! /bin/bash

# read -p "give me input> "
REPLY='wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj'

# normalize text: convert uppercase letters to lowercase and remove ponctuation
TEXT=($(echo $REPLY | tr [A-Z] [a-z] | tr -d [:punct:]))
TEXT_LENGTH=${#TEXT[@]}

# path to the dictionary we will use
DICT_PATH='/usr/share/dict/words'

# create lines we will use
OUTPUT_LENGTH=50
line=''; spaces=''
for((i=0;i<$OUTPUT_LENGTH;i++)); do line=$line'=';done
for((i=0;i<$OUTPUT_LENGTH;i++)); do spaces=$spaces'-';done

# define the barrier.
# if a certain letter gives `score` higher than `TOP` then it will be accepted
TOP=50

# iterate each letter
for c in {a..z}
do
    # next letter
    c1=$(echo $c | tr [a-z] [b-za])
    # decrypt with the current letter `c`
    decrypted=($(echo ${TEXT[@]} | tr [$c1-za-$c] [a-z]))
    # initally each letter gives full score.
    # i.e every word is accepted and for each word it has 1 for each word.
    # i.e it has initially words length as initial value
    # then with each wrong decrypted word the score decriment with 1
    score=$TEXT_LENGTH
    for word in ${decrypted[@]}; do
        grep -e "^$word$" $DICT_PATH > /dev/null
        score=$(($score-$?))
    done
    # percentage of accepted word
    percentage=$(($score*100/$TEXT_LENGTH))
    # defines the length of the accepted words
    line_percentage=$(($percentage*$OUTPUT_LENGTH/100))

    # if no details demanded and the current letter `score` didn't reach `top`,
    # the current iteration will be skiped
    [[ -z $1 ]] && [[ $percentage -le $TOP ]] && continue 

    # show current letter information
    echo -n "$c : "
    [[ $percentage -gt $TOP ]] && echo -n '['${decrypted[@]}'] => '
    echo $percentage
    # represent line percent
    echo [${line:0:line_percentage}${spaces:line_percentage:$OUTPUT_LENGTH}]
done
