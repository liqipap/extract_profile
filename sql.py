#encoding=utf-8  
import os
import re
import sys
from imp import reload
reload(sys)


# enable file generation
gen_file = True

# generate file report
final_rpt_en = True

# enable print msg?
print_en = False

#programming language
code_dic = {b'java': 0, b'dotnet': 0, b'hadoop': 0, b'ruby': 0, b'python': 0, b'cplus': 0}

#email service company
email_service_dic={}

#age ranges from 1970 to 1988
age_dic = {}


total_records = 0

def print_status_1():
  print("Email service providers.......................")
  for k, v in sorted(email_service_dic.items(), key=lambda d: d[1]):
    # only print records > 10
    if v > 10: print("%s : %d" %(k,v))
    if final_rpt_en:
      file_handle = open (b'rpt.txt', 'a' )
      file_handle.write('\nEmail service providers.......................')
      file_handle.write('\n' + k.decode() + ' : ' + str(v))
      file_handle.close()


def print_status_2():
  print("current No. of candidates in each programming language.......................")
  for k, v in sorted(code_dic.items(), key=lambda d: d[1]):
    print('total No. of %s developers is ： %d'%(k,v))
    if final_rpt_en:
      file_handle = open (b'rpt.txt', 'a' )
      file_handle.write('\ncurrent No. of candidates in each programming language............')
      file_handle.write('\ntotal No. of ' + k.decode() + ' developers is ： ' + str(v))
      file_handle.close()

def print_status_3():
  print("current age data.......................")
  for k, v in sorted(age_dic.items(), key=lambda d: d[1]):
    print('total No. of developers (Age: %s) is ： %d'%(k,v))
    if final_rpt_en:
      file_handle = open (b'rpt.txt', 'a' )
      file_handle.write('\current age data...............................')
      file_handle.write('\ntotal No. of developers Age ： ' + k.decode() + ' is : ' + str(v))
      file_handle.close()


# match code with age
def match_age_code(line, code_key):
  code_match = re.search(b'.*'+ code_key +b'.*', line)
  email_match = re.search(b'\s+(\w+\S*)@(\w+\S*)\s+', line)
  #
  if email_match:
    email_addr = email_match.group(1).lower() + b'@' + email_match.group(2).lower()
  else:
    # no email match? im out
    return True
  
  for a in range(1970, 1988):
    #
    age_match = re.search(b'.*'+str.encode(str(a))+b'.*', line)
    #
    if age_match and code_match:
      #
      age_key = str.encode(str(a))
      if age_key in age_dic.keys():
        age_dic[age_key] +=1
      else:
        age_dic[age_key] = 1
      #
      if gen_file:
        file_handle = open (b'results/'+ b'_____1_age_' + age_key + b'_' + code_key + b'.txt', 'a' )
        file_handle.write('\n'+email_addr.decode())
        file_handle.close()
      return 
    elif age_match:
      age_key = str.encode(str(a))
      if age_key in age_dic.keys():
        age_dic[age_key] +=1
      else:
        age_dic[age_key] = 1
      #
      if gen_file:
        file_handle = open (b'results/'+ b'_____1_age_' + age_key + b'.txt', 'a' )
        file_handle.write('\n'+email_addr.decode())
        file_handle.close()
      return 
    #end for loop
  return

# match the programming language
def match_code(line, code_key):
  code_match = re.search(b'.*'+ code_key +b'.*', line)
  email_match = re.search(b'\s+(\w+\S*)@(\w+\S*)\s+', line)
  if email_match:
    email_addr = email_match.group(1).lower() + b'@' + email_match.group(2).lower()
  else:
    # no email match? im out
    return True
  
  if code_match:
    if code_key in code_dic.keys():
      code_dic[code_key] +=1
    else:
      code_dic[code_key] = 1
    #
    if gen_file:
      file_handle = open (b'results/'+ b'_____1_' + code_key + b'.txt', 'a' )
      file_handle.write('\n'+email_addr.decode())
      file_handle.close()
    return True
  else:
    return False
    
      
with open('db.sql', 'rb') as fp:
  if True:
    for line in fp:
        total_records += 1
        if total_records % 10000 == 0:
          if print_en:
            print_status_2()
            print_status_3()
          print("current total_records is %d"%total_records)

        # match the email service provider
        email_match = re.search(b'\s+(\w+\S*)@(\w+\S*)\s+', line)
        if email_match:
          tmp_key = email_match.group(2).lower()
          email_addr = email_match.group(1).lower() + b'@' + email_match.group(2).lower()
          if tmp_key in email_service_dic.keys():
            email_service_dic[tmp_key] +=1
            if gen_file:
              file_handle = open (b'results/'+tmp_key+b'.txt', 'a' )
              file_handle.write('\n'+email_addr.decode())
              file_handle.close()
          else:
            email_service_dic[tmp_key] = 1

        #match programming language 
        for k in code_dic.keys():
          if match_code(line, k): break

        #match code and age
        match_age_code(line, k)


print_status_1()
print_status_2()
print_status_3()

  



