#!/bin/bash

shopt -s nocasematch

function renameFiles {
    for item in *
    do
        # if it is file...
        if [[ -f "$item" ]];
        then
            local fileName=$item

            # find subtitles
            # if [[ $fileName =~ ^(.*?)(s[0-9]{1,2}e[0-9]{1,2})+(\([0-9]+\))?\.(srt|sub)$ ]]; 
            if [[ $fileName =~ ^(.*?)(\([0-9]+\))?\.(srt|sub)$ ]];
            then
                local namePart1=${BASH_REMATCH[1]}
                local namePart2=${BASH_REMATCH[2]}
                local name=$namePart1$namePart2

                # replace "- _" characters with "." so when used as regex it will match files 
                # that contain the same name disregarding the separator used
                local nameRegex="${name//[-\ _]/\.}"
                # replace " _." separators for dash separator
                local nameClean="${name//[\ _\.]/-}"

                for fileName2 in *
                do
                    if [[ -f "$fileName2" ]];
                    then
                        # this should pass for both movie and subtitle file because of the name regex 
                        # (provided both movie and subtitle file use the same movie name as its base)
                        if [[ $fileName2 =~ ^$nameRegex(.*?)\.([a-z0-9]{3,4})$ ]];
                        then
                            local extension=${BASH_REMATCH[2]}
                            local newName=$nameClean.$extension

                            if [ ! -e "$newName" ];
                            then
                                # mv "$fileName2" "$newName"
                                echo File renamed from "$fileName2" to "$newName"
                            fi
                        fi
                    fi
                done
            fi
        # if it is directory...
        elif [[ -d "$item" ]];
        then
            cd "$item"
            renameFiles
            cd ..
        fi
    done
}

renameFiles

shopt -u nocasematch

exit 0