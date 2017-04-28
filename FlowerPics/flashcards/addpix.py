"""LATEX PICTURE FLASHCARD MAKER
Logan Halstrom
28 April 2017
DESCRIPTION:  Glob all picture filenames in a directory.  Write LaTeX script
that plots all pictures in flashcard form, with filename as label.
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
    ogdir = os.getcwd()
    os.chdir(picdir)
    files = glob.glob('*.{}'.format(filetype))
    os.chdir(ogdir)

    #OPEN SAVE OR APPEND FILE
    if append:
        #Copy base Tex file to output file and append to it
        cmd('cp base.txt {}'.format(ofilename))
        ofile = open(ofilename, 'a')
    else:
        #Write to empty output file
        ofile = open(ofilename, 'w')



    for file in files:
        ofile.write('{}\n'.format(file))




    #CLOSE SAVE FILE
    if append:
        #end LaTeX document if appending to have runnable script
        ofile.write('\end{document}\n')
    ofile.close()


    #     iters.append(re.search(head + r'\.([0-9]*)', file).group(1))
    # iters = [int(i) for i in iters]


if __name__ == "__main__":


    PicDir = '..'
    Type = 'jpg'


    main(PicDir, Type, True, 'FlowerTest.tex')




