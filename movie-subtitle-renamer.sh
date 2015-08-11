#!/bin/bash

shopt -s nocasematch

separator=$1
if [[ -z $separator ]]; then
    # default separator
    separator="-"
fi

function renameFiles {
    for item in *
    do
        # if it is file...
        if [[ -f "$item" ]]; then
            local fileName=$item

            # find subtitles
            if [[ $fileName =~ ^([^\(\)]*)(\([0-9]+\))?\.(sub|srt)$ ]]; then
                local subName=${BASH_REMATCH[1]}
                local subCleanName=$subName

                # subName contains Season/Episode part (TV show)
                if [[ $subName =~ ^(.*)(s[0-9]{1,2}e[0-9]{1,2}) ]]; then
                    local showName=${BASH_REMATCH[1]}
                    local showSeasonEpisode=${BASH_REMATCH[2]}
                    subCleanName=$showName$showSeasonEpisode
                # subName contains some movie format information
                # hdtv|19[0-9]{2}|20[0-9]{2}|hd-?ts|xvid|hdrip|brrip|x264|480p|720p|1080p|ac3-ev
                # elif [[ $subName =~ ... ]]; then
                    # subCleanName=${BASH_REMATCH[1]}
                fi

                # replace "- _" characters with "." so when used as regex it will match files 
                # that contain the same name disregarding the separator used
                local nameRegex="${subCleanName//[-\ _]/\.}"

                # replace " _." separators for dash separator
                local nameFormatted="${subCleanName//[-\ _\.]/$separator}"

                for fileName2 in *
                do
                    if [[ -f "$fileName2" ]]; then
                        # this should pass for both movie and subtitle file because of the name regex 
                        # (provided both movie and subtitle file use the same movie name as its base)
                        if [[ $fileName2 =~ ^$nameRegex(.*?)\.([a-z0-9]{3,4})$ ]]; then
                            local extension=${BASH_REMATCH[2]}
                            local newName=$nameFormatted.$extension

                            if [ ! -e "$newName" ]; then
                                # mv "$fileName2" "$newName"
                                echo File renamed from "$fileName2" to "$newName"
                            fi
                        fi
                    fi
                done
            fi
        # if it is directory...
        elif [[ -d "$item" ]]; then
            cd "$item"
            renameFiles $separator
            cd ..
        fi
    done
}

# run
renameFiles $separator

shopt -u nocasematch

exit 0