#!/usr/bin/python

import sys, getopt, os, re, glob

def separatorList():
    return ['-', '.', '_', ' ']

def replaceSeparators(inputString, desiredSeparator):
    outputString = inputString
    for separator in separatorList():
        outputString = outputString.replace(separator, desiredSeparator)

    return outputString

def extractCleanNameWithExtension(fullName):
    # purge subtitle name of some ID in parentheses at the end if present (titulky.com format)
    result = re.search(r'^(.*?)(?:\([0-9]+\))?\.([a-z]{3})$', fullName, re.I)
    if (result):
        name = result.group(1)
        extension = result.group(2)
        cleanName = name

        # in case subtitles name contains Season/Episode part (TV show), stop there when looking for name
        result = re.search(r'^(.*?)(s[0-9]{1,2}e[0-9]{1,2})', name, re.I)
        if (result):
            cleanName = result.group(1) + result.group(2).upper()
        else:
            # subtitles name contain some movie information (year, format, etc.), use that to detect actual movie name
            # TODO make sure year is only matched if it is not part of the movie title (i.e. is surrounded by separators)
            result = re.search(r'^(.*?)(hdtv|19[0-9]{2}|20[0-9]{2}|hd-?ts|xvid|hdrip|brrip|x264|480p|720p|1080p|ac3-ev)', name, re.I)
            if (result):
                cleanName = result.group(1)

        cleanName = cleanName[:-1] if cleanName.endswith(tuple(separatorList())) else cleanName

        return [cleanName, extension]
    else:
        return False

def selectFiles(types):
    files = []
    for selectedFiles in types:
        files.extend(glob.glob(selectedFiles))

    return files

def rename(origName, newName):
    # os.rename(origName, newName)
    return

def renameSubtitles(subtitleFiles, separator, interactiveMode):
    subtitlesRegexes = []
    subtitlesRenamedTo = []

    for subtitleFile in subtitleFiles:
        cleanSubtitleName, subtitleExtension = extractCleanNameWithExtension(subtitleFile)

        if not cleanSubtitleName:
            continue

        # replace separator character with "." character so when used as regex it will match Movie files 
        # that contain the same name no matter what separator was used in those files
        subtitlesRegexes.append(replaceSeparators(cleanSubtitleName, '.'))

        # replace "-._ " separators for configured separator
        nameFormatted = replaceSeparators(cleanSubtitleName, separator)

        nameWithExtension = nameFormatted + '.' + subtitleExtension

        # filename is already formatted correctly
        if nameWithExtension == subtitleFile:
            subtitlesRenamedTo.append(subtitleFile)
            print "File " + subtitleFile + " is already in correct format, skipping..."
            continue

        if (nameWithExtension not in subtitlesRenamedTo):
            subtitlesRenamedTo.append(nameWithExtension)

            message = "File will be renamed from " + subtitleFile + " to " + nameWithExtension
        else:
            i = 1
            _nameWithExtension = nameWithExtension
            nameWithExtension = nameFormatted + "(" + str(i) + ")." + subtitleExtension
            while (nameWithExtension in subtitlesRenamedTo):
                i += 1
                nameWithExtension = nameFormatted + "(" + str(i) + ")." + subtitleExtension

            subtitlesRenamedTo.append(nameWithExtension)

            message = "File will be renamed from " + subtitleFile + " to " + nameWithExtension + " (" + _nameWithExtension + " already exists)" 

        if (interactiveMode):
            proceed = raw_input(message + ", continue? (y/N) ")
            if proceed.lower() == 'y':
                rename(subtitleFile, nameWithExtension)
        else:
            rename(subtitleFile, nameWithExtension)
            print message

    return subtitlesRegexes

def renameVideoFiles(videoFiles, subtitlesRegexes, separator, interactiveMode):
    # sort subtitle name regexes based on their length, longest one first
    subtitleRegexesSorted = sorted(subtitlesRegexes, key = len, reverse = True)

    for videoFile in videoFiles:
        for nameRegex in subtitleRegexesSorted:
            regex = r'^' + nameRegex + '(?:.*?)\.([a-z0-9]{3,4})$'
            result = re.search(regex, videoFile, re.I)
            if (result):
                movieExtension = result.group(1)

                newMovieName = replaceSeparators(nameRegex, separator) + '.' + movieExtension
                print "MOVIE renaming from ", videoFile, " to ", newMovieName
                break

def renameFiles(separator, interactiveMode, recursiveMode):
    # list of all subtitle filenames in current directory, sorted by length with shortest one first
    subtitleFiles = sorted(selectFiles(['*.srt', '*.sub']), key = len)

    # list of all movie/TV Show filenames in current directory
    videoFiles = selectFiles(['*.mkv', '*.avi', '*.mp4', '*.m4p', '*.m4v', '*.mpg', '*.mp2', '*.mpeg', '*.mpe', '*.mpv', '*.m2v'])

    # rename subtitles files
    newSubtitleNameRegexes = renameSubtitles(subtitleFiles, separator, interactiveMode)

    # rename video files base on new subtitles names
    renameVideoFiles(videoFiles, newSubtitleNameRegexes, separator, interactiveMode)

    if (recursiveMode):
        # look for another directories within the current directory and continue renaming files in them
        for item in os.listdir('.'):
            if (os.path.isdir(item)):
                if (item.startswith('.')):
                    continue

                os.chdir(item)
                renameFiles(separator, interactiveMode, recursiveMode)
                os.chdir('..')

def usage():
    print "Usage: "+ sys.argv[0] + " [options]"
    print "Options:"
    print "\t-i, --interactive"
    print "\t\t Run interactively"
    print "\t-r, --recursive"
    print "\t\t Rename files recursively in child directories"
    print "\t-s separator, --separator separator"
    print "\t\t Use separator for separating words in renamed file (default separator is '-')"

def main(separator, interactiveMode, recursiveMode):
    os.chdir('..')

    renameFiles(separator, interactiveMode, recursiveMode)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hirs:', ['help', 'interactive', 'recursive', 'separator'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    separator = '-'
    interactiveMode = False
    recursiveMode = False

    for option, value in opts:
        if option in ('-h', '--help'):
            usage();
            sys.exit(0)
        elif option in ('-i', '--interactive'):
            interactiveMode = True
        elif option in ('-r', '--recursive'):
            recursiveMode = True
        elif option in ('-s', '--separator'):
            separator = value

    main(separator, interactiveMode, recursiveMode)