from subprocess import call, Popen, PIPE
from sys import argv
import os
import subprocess
from time import sleep
from shutil import copyfile
import difflib

d = difflib.Differ()

PASS = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
US = '\033[34m'
THEM = '\033[37m'

fail_count = 0;
total_count = 0;

if "check_output" not in dir( subprocess ): # duck punch it in!
  def f(*popenargs, **kwargs):
    if 'stdout' in kwargs:
      raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
      cmd = kwargs.get("args")
      if cmd is None:
        cmd = popenargs[0]
      raise subprocess.CalledProcessError(retcode, cmd)
    return output

  subprocess.check_output = f

for rc_file in [test for test in os.listdir('./'+argv[1]) if '.rc' in test]:
  output = ''
  filePref = rc_file[0:rc_file.find('.')]

  if not(filePref + '.s' in os.listdir('./'+argv[1])):
    print '\t' + filePref + '.s missing, generating...'
    try:
      output = subprocess.check_output(['testrunner_client', './' + argv[1] + '/' + rc_file])
    except subprocess.CalledProcessError as e:
      pass

    if 'Compile: failure.' in output: #subprocess.check_output(['testrunner_client', rc_file]):
      print '[' + rc_file + ']: Bad test, WNBT. Continuing...'
      continue

    copyfile('rc.s', './'+argv[1] + '/' + filePref + '.s')

  tr_rc_s = open('./' + argv[1] + '/' + filePref + '.s').read()
  processed_tr_rc = []

  for line in tr_rc_s.split('\n'):
    if not (line.strip() == '') and not ('!' in line) and not ('*' in line):
      #processed_tr_rc.append(''.join(line.split()))
      processed_tr_rc.append(line)

  try:
    output = subprocess.check_output(['./RC', './' + argv[1] + '/' + rc_file])
  except subprocess.CalledProcessError as e:
    pass

  if 'Compile: failure.' in output: #subprocess.check_output(['./RC', rc_file]):
    print 'Error: Yo shit fuckt. Exiting.'
    exit()

  my_rc_s = open('rc.s').read()
  processed_my_rc = []

  for line in my_rc_s.split('\n'):
    if not (line.strip() == '') and not ('!' in line) and not ('*' in line):
      #processed_my_rc.append(''.join(line.split()))
      processed_my_rc.append(line)

  error = False

  f = open('./' + argv[1] + '/' + filePref + '.s', 'w+')
  proc_rc = '\n'.join(processed_tr_rc)
  f.write(proc_rc)
  f.close()

  f = open('rc.s','w+')
  proc_my = '\n'.join(processed_my_rc)
  f.write(proc_my)
  f.close()

  p = subprocess.Popen(['diff', '-w', '-I', "'!.*'", 'rc.s','./' + argv[1] + '/' + filePref + '.s'],stdout=subprocess.PIPE)
  out, err = p.communicate()

  if len(out) > 0:
    print '-- [' + rc_file + '] Differences found: '
    error = True
    fail_count += 1
    for line in out.split('\n'):
        line = line.replace('>','TR: ',1)
        line = line.replace('<','MY: ',1)
        if ':' in line:
            linePre = line[0:line.find(':')]
            linePost = line[line.find(':') + 1:]
            line = linePre + ': ' +  linePost.lstrip()
            print (THEM + '\t' + line + ENDC) if 'TR' in line else (US + '\t' + line + ENDC) 
    

  out = ""

  
  total_count += 1
  print '[' + rc_file + ']: ' + ((FAIL + 'Failure.' + ENDC) if error else (PASS + 'Passed!' + ENDC))
  #sleep(10)
    

print '\nTesting completed successfully.'
print str(total_count - fail_count) + '/' + str(total_count) + ' tests passing.'
