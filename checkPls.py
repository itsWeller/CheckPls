from subprocess import call, Popen, PIPE
from sys import argv
import os
import subprocess
from shutil import copyfile

PASS = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
US = '\033[34m'
THEM = '\033[37m'

global fail_count
fail_count = 0
total_count = 0;

test_dir    = './' + argv[1] + '/'
rc_location = './../cse131/'

error = False

def sanitize_file(path):
    return [line for line in open(path).read().split('\n') 
      if not (line.strip() == '') and not ('!' in line) and not ('*' in line)]

def list2file(path, contents):
    f = open(path, 'w+')
    proc_rc = '\n'.join(contents)
    f.write(proc_rc)
    f.close()

def determine_output(error):
    print '[' + rc_file + ']: ' + ((FAIL + 'Failure.' + ENDC) if error else (PASS + 'Passed!' + ENDC))
    error = False

def compile_check(output, error):
    if 'Compile: failure.' in output:
        print '[' + rc_file + ']: ' + ('Bad test, WNBT. Continuing...' if not error else 'Yo shit fukt. Skipping.')
        return False
    return True

def binary_output(opts, cwd='.'):
    p = subprocess.Popen(opts, stdout=subprocess.PIPE, cwd=cwd)
    s = p.communicate()[0]
    return s

def print_footer():
    print '\nTesting completed successfully.'
    print str(total_count - fail_count) + '/' + str(total_count) + ' tests passing.'

def generate_error(line):
    print '-- [' + rc_file + '] Differences found: '
    error = True
    global fail_count 
    fail_count += 1
    for line in out.split('\n'):
        line = line.replace('>','TR: ',1)
        line = line.replace('<','MY: ',1)
        if ':' in line:
            linePre = line[0:line.find(':')]
            linePost = line[line.find(':') + 1:]
            line = linePre + ': ' +  linePost.lstrip()
            print (THEM + '\t' + line + ENDC) if 'TR' in line else (US + '\t' + line + ENDC) 

for rc_file in [test for test in os.listdir(test_dir) if '.rc' in test]:
    filePref = rc_file[0:rc_file.find('.')]
    outFile = filePref  + '.s'

    if not(outFile in os.listdir(test_dir)):
        print '\t' + outFile + ' missing, generating...'
        if not compile_check(binary_output(['testrunner_client', test_dir]), False): continue

        copyfile('rc.s', test_dir + outFile)
        list2file(test_dir + outFile, sanitize_file(test_dir + outFile))

    if not compile_check(binary_output([rc_location + 'RC', test_dir + rc_file], rc_location), True): continue
    list2file(rc_location + 'rc.s', sanitize_file(rc_location + 'rc.s'))

    out = binary_output(['diff', '-w', '-I', "'!.*'", rc_location + 'rc.s',test_dir + outFile])
    if len(out) > 0: 
        generate_error(out)
        error=True

    total_count += 1
    determine_output(error)
    error = False

print_footer()
