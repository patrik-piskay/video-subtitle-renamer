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
    # purge file name of some ID in parentheses at the end if present (titulky.com subtitle format)
    result = re.search(r'^(.*?)(?:\([0-9]+\))?\.([a-z0-9]+)$', fullName, re.I)
    if (result):
        name = result.group(1)
        extension = result.group(2)
        cleanName = name

        # in case file name contains Season/Episode part (TV show), stop there when looking for name
        result = re.search(r'^(.*?)(s[0-9]{1,2}e[0-9]{1,2})', name, re.I)
        if (result):
            cleanName = result.group(1) + result.group(2).upper()
        else:
            # file name contain some movie information (format, resolution, etc.), use that to detect actual movie name
            result = re.search(r'^(.*?)(hdtv|hd-?ts|xvid|hdrip|brrip|x264|480p|720p|1080p|ac3-ev)', name, re.I)
            if (result):
                cleanName = result.group(1)

        cleanName = cleanName[:-1] if cleanName.endswith(tuple(separatorList())) else cleanName

        return [cleanName, extension]
    else:
        return [None, None]

def selectFiles(types):
    files = []
    for selectedFiles in types:
        files.extend(glob.glob(selectedFiles))

    return files

def handleRename(oldFileName, newFileName, message, options):
    if (options['interactiveMode']):
        if confirm(message):
            renameFile(oldFileName, newFileName, options['testingMode'])
            print "Renamed"
        else:
            print "Skipped"
    else:
        renameFile(oldFileName, newFileName, options['testingMode'])

        # "will be" substring only makes sense for interactive mode
        print message.replace('will be ', '')

def confirm(message):
    proceed = raw_input(message + ", continue? (Y/n) ")
    return proceed.lower() == 'y' or proceed == ''

def renameFile(origName, newName, testingMode):
    if not testingMode:
        os.rename(origName, newName)

def renameVideoSubtitleFiles(fileName, filesRenamedTo, options):
    cleanName, extension = extractCleanNameWithExtension(fileName)

    if not cleanName:
        print "Name of '" + fileName + "' file does not match expected file format, skipping..."
        return

    # replace "-._ " separators for configured separator
    nameFormatted = replaceSeparators(cleanName, separator)

    newFileName = nameFormatted + '.' + extension

    # file name is already formatted correctly
    if newFileName == fileName:
        filesRenamedTo.append(fileName)
        print "File '" + fileName + "' is already in correct format, skipping..."
        return

    if (newFileName not in filesRenamedTo):
        filesRenamedTo.append(newFileName)

        message = "File will be renamed from '" + fileName + "' to '" + newFileName + "'"
    else:
        i = 1
        _newFileName = newFileName
        newFileName = nameFormatted + "(" + str(i) + ")." + extension
        while (newFileName in filesRenamedTo):
            i += 1
            newFileName = nameFormatted + "(" + str(i) + ")." + extension

        filesRenamedTo.append(newFileName)

        message = "File will be renamed from '" + fileName + "' to '" + newFileName + "' ('" + _newFileName + "' already exists)"

    handleRename(fileName, newFileName, message, options)

def renameFiles(separator, options):
    # list of all subtitle filenames in current directory, sorted by length with shortest one first
    subtitleFiles = sorted(selectFiles(['*.srt', '*.sub']), key = len)

    # list of all movie/TV Show filenames in current directory, sorted by length with shortest one first
    videoFiles = sorted(selectFiles(['*.mkv', '*.avi', '*.mp4', '*.m4p', '*.m4v', '*.mpg', '*.mp2', '*.mpeg', '*.mpe', '*.mpv', '*.m2v']), key = len)

    filesRenamedTo = []

    # rename files
    if (len(videoFiles) == 1 and len(subtitleFiles) == 1):
        # only one video and subtitles file, I guess it is safe to rename video file based on clean subtitles file name
        videoFile = videoFiles[0]
        subtitleFile = subtitleFiles[0]

        renameVideoSubtitleFiles(subtitleFile, filesRenamedTo, options)

        newSubtitleFile = filesRenamedTo[0]
        result = re.search(r'^(.*?)\.([a-z]+)$', newSubtitleFile, re.I)
        if result:
            name = result.group(1)

            result = re.search(r'^(.*?)\.([a-z]+)$', videoFile, re.I)
            if result:
                extension = result.group(2)
                newVideoFileName = name + '.' + extension

                message = "File will be renamed from '" + videoFile + "' to '" + newVideoFileName + "'"

                handleRename(videoFile, newVideoFileName, message, options)

    else:
        videoSubtitlesFiles = subtitleFiles + videoFiles
        for _file in videoSubtitlesFiles:
            renameVideoSubtitleFiles(_file, filesRenamedTo, options)

    if (options['recursiveMode']):
        # look for another directories within the current directory and continue renaming files in them
        for item in os.listdir('.'):
            if (os.path.isdir(item)):
                if (item.startswith('.')):
                    continue

                os.chdir(item)
                renameFiles(separator, options)
                os.chdir('..')

def usage():
    print "Usage: "+ sys.argv[0] + " [options]"
    print "Options:"
    print "\t-i, --interactive"
    print "\t\t Run interactively (you will have to confirm before each file gets renamed)"
    print "\t-r, --recursive"
    print "\t\t Rename files recursively in child directories"
    print "\t-s separator, --separator separator"
    print "\t\t Use separator for separating words in renamed file (default separator is '-')"

def main(separator, interactiveMode, recursiveMode, testingMode):
    try:
        options = {
            'interactiveMode': interactiveMode,
            'recursiveMode': recursiveMode,
            'testingMode': testingMode,
        }

        renameFiles(separator, options)
    except KeyboardInterrupt:
        print
        sys.exit(0)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hirs:', ['help', 'interactive', 'recursive', 'separator', 'testing'])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)

    separator = '-'
    interactiveMode = False
    recursiveMode = False
    testingMode = False

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
        elif option in ('--testing'):
            testingMode = True

    main(separator, interactiveMode, recursiveMode, testingMode)