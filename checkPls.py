from subprocess import call, Popen, PIPE
from optparse import OptionParser
from shutil import copyfile
from sys import argv
import subprocess, os

# Used for colors. ANSI color codes.
PASS = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
US   = '\033[34m'
THEM = '\033[37m'

# Counts for testing
global fail_count
fail_count  = 0
total_count = 0;

parser = OptionParser()
parser.add_option('-t','--test-folder',dest='test_dir',help='directory containing .rc tests', default='tests/')
parser.add_option('-r','--rc-location',dest='rc_location',help='directory containing RC binary', default='./')
parser.add_option('-f',dest='generate_requested', action='store_true', help='flag to force regeneration of testrunner_client .s files',default=False)

(options, args) = parser.parse_args()

# Option set by optparse
test_dir = options.test_dir if '/' in options.test_dir[-1:] else options.test_dir + '/'
rc_location = options.rc_location if '/' in options.rc_location[-1:] else options.rc_location + '/'

error = False

# Remove comments, generated dialog, and extra lines
def sanitize_file(path):
    return [line for line in open(path).read().split('\n') 
      if not (line.strip() == '') and not ('!' in line) and not ('*' in line)]

# Write list to file
def list2file(path, contents):
    f = open(path, 'w+')
    proc_rc = '\n'.join(contents)
    f.write(proc_rc)
    f.close()

# Generate success/failure dialog
def determine_output(error):
    print '[' + rc_file + ']: ' + ((FAIL + 'Failure.' + ENDC) if error else (PASS + 'Passed!' + ENDC))
    error = False

# Determine if valid test and ./RC output is valid
def compile_check(output, error):
    if 'Compile: failure.' in output:
        print '[' + rc_file + ']: ' + ('Bad test, WNBT. Continuing...' if not error else 'Yo shit fukt. Skipping.')
        return False
    return True

# Execute command
def binary_output(opts, cwd='.'):
    try:
        p = subprocess.Popen(opts, stdout=subprocess.PIPE, cwd=cwd)
        s = p.communicate()[0]
        return s
    except OSError as e:
        print FAIL + "Error executing command. Are you trying to generate testrunner_client's .s files offline?" + ENDC
        print 'Check directory settings. Exiting...'
        exit()


# Print score/footer
def print_footer():
    print '\nTesting completed successfully.'
    print str(total_count - fail_count) + '/' + str(total_count) + ' tests passing.'

# Formatting for diff output
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

# Gather all the *.rc files in the test directory
for rc_file in [test for test in os.listdir(test_dir) if '.rc' in test]:
    filePref = rc_file[0:rc_file.find('.')]
    outFile = filePref  + '.s'

    # Generate testrunner_client's solution files if not already present
    if not(outFile in os.listdir(test_dir)) or options.generate_requested:
        print '\t' + outFile + ' missing, generating...'
        if not compile_check(binary_output(['testrunner_client', test_dir]), False): continue

        # Write generated files
        copyfile('rc.s', test_dir + outFile)
        list2file(test_dir + outFile, sanitize_file(test_dir + outFile))

    # Always generate and write user's RC .s files
    if not compile_check(binary_output([rc_location + 'RC', test_dir + rc_file], rc_location), True): continue
    list2file(rc_location + 'rc.s', sanitize_file(rc_location + 'rc.s'))

    # Diff matching pair of RC and testrunner_client's files
    out = binary_output(['diff', '-w', '-I', "'!.*'", rc_location + 'rc.s',test_dir + outFile])

    # If diff exists, generate error output
    if len(out) > 0: 
        generate_error(out)
        error=True

    # General housekeeping
    total_count += 1
    determine_output(error)
    error = False

# Print score
print_footer()
