"""LATEX PICTURE FLASHCARD MAKER
Logan Halstrom
28 April 2017

DESCRIPTION:  Glob all picture filenames in a directory.  Write LaTeX script
that plots all pictures in flashcard form, with filename as label.

NOTES: Orient all pictures so that longest dimension is horizontal

"""

import subprocess
import os
import glob
import re
import numpy as np

def cmd(command):
    """Execute a shell command.
    Execute multiple commands by separating with semicolon+space: '; '
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    #print proc_stdout
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout

def FindBetween(string, before='^', after=None):
    """Search 'string' for characters between 'before' and 'after' characters
    If after=None, return everything after 'before'
    Default before is beginning of line
    """
    if after == None and before != None:
        match = re.search('{}(.*)$'.format(before), string)
        if match != None:
            return match.group(1)
        else:
            return 'No Match'
    else:
        match = re.search('(?<={})(?P<value>.*?)(?={})'.format(before, after), string)
        if match != None:
            return match.group('value')
        else:
            return 'No Match'




def main(picdir, filetype='jpg', append=True, ofilename='out.tex'):
    """
    picdir --> path to directory with pictures in it
    filetype --> picture filetype to search for
    append --> append LaTeX script to 'base.tex' (True) or save as standalone
    ofilename --> name of output text file
    """




    #GET ALL FILENAMES OF SPECIFIED IMAGE TYPE
    # ogdir = os.getcwd()
    # os.chdir(picdir)
    # files = glob.glob('*.{}'.format(filetype))
    # os.chdir(ogdir)

    files = glob.glob('{}/*.{}'.format(picdir, filetype))

    #OPEN SAVE OR APPEND FILE
    if append:
        #Copy base Tex file to output file and append to it
        cmd('cp base.tex {}'.format(ofilename))
        ofile = open(ofilename, 'a')
        ofile.write('\n')
    else:
        #Write to empty output file
        ofile = open(ofilename, 'w')



    #WRITE LATEX SCRIPT

    #Determine how many pages will be made
    N = len(files)      #Number of individuals
    nper = 8            #Number of individuals per page
    np = N // nper      #Number of pages fully filled

    #Write complete pages until list is used up
    while files:
        cur = [' '] * nper    #Current nper images to write (empty)
        for i, f in enumerate(files[:nper]):
            cur[i] = f        #fill with titles until 'files' is empty
        # cur = files[:nper]    #Current nper images to write
        files = files[nper:]  #Remaining unused images


        # tit = list(cur)       #Titles for each flash card (remove extension)
        # #Titles for each flash card (remove extension)
        # tit = [re.search('(?<=^)(?P<value>.*?)(?=.{})'.format(filetype).group('value'), f) for f in cur]
        tit = [] #Titles for each flash card (remove extension)
        for c in cur:
            tit.append( FindBetween(c, '/'.format(picdir), '.{}'.format(filetype)) )

        #Swap every other title for correct double-sided printing
        for i in range(0, nper-2, 2):
            tit[i], tit[i+1] = tit[i+1], tit[i]


        # ofile.write('\\newpage\n')

        #Write all Titles
        for t in tit:

            ofile.write( '\\noindent  {}\n'.format(' ') )
            ofile.write( '\\vfill\n' )
            ofile.write( '\\centerline{{{{\Large\emph{{{}}}}}}}\n'.format(t) )
            ofile.write( '\\vfill\n' )
            ofile.write( '\\newpage\n\n' )



            # ofile.write('{}\n'.format(f))


        #Write corresponding Answers
        for c in cur:
            # ofile.write( '\\vspace*{\\stretch{1}}\n' )

            # ofile.write( '\\begin{figure}\n' )
            ofile.write( '\\begin{center}\n' )

            ofile.write( '\\includegraphics[height=0.925\\paperheight]{{{}}}\n'.format(c) )
            # ofile.write( '\\includegraphics[width=\\linewidth,height=\\textheight,keepaspectratio, angle=90]{{{}}}\n'.format(c) )



            ofile.write( '\\end{center}\n' )

            # ofile.write( '\\end{figure}\n' )

            # ofile.write( '\\vspace*{\\stretch{1}}\n' )
            ofile.write( '\\newpage\n\n' )




    #CLOSE SAVE FILE
    if append:
        #end LaTeX document if appending to have runnable script
        ofile.write('\n\end{document}\n')
    ofile.close()


if __name__ == "__main__":


    PicDir = '..'
    Type = 'jpg'


    main(PicDir, Type, True, 'Flashcards_Flowers.tex')




