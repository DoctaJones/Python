import urllib2
import json
import xml.etree.ElementTree as ET

#Detailed Health Checks
json_prod_urls = ['https://directory.drive.hpconnected.com/healthcheck?detail',
             'https://storage.drive.hpconnected.com/healthcheck?detail',
             'https://metadata.drive.hpconnected.com/healthcheck?detail',
             'https://crawler.drive.hpconnected.com/healthcheck?detail',
             'https://push.drive.hpconnected.com/healthcheck?detail',
             'https://action.drive.hpconnected.com/healthcheck?detail']

xml_prod_urls = ['https://webauth.hpconnected.com/oauth/healthcheck',
             'https://vault.hpconnected.com/vault/healthcheck',
             'https://dram.hpconnected.com/deviceregmgmt/healthcheck',
             'https://pam.hpconnected.com/pam/healthcheck',
             'https://services.hpconnected.com/subscription/healthcheck']

for url in json_prod_urls:
  print
  print (url)
  response = urllib2.urlopen(url)
  output = json.loads(response.read())
  numtests = len((output)['healthReport']['tests'])
  i = 0
  while i < numtests:
    result = (output)['healthReport']['tests'][i]['passed']
    test = (output)['healthReport']['tests'][i]['name']
    if result:
      print '  ' + test + ' HEALTHY'
    else:
      print json.dumps((output)['healthReport']['tests'][i], indent=2)
    i += 1

for url in xml_prod_urls:
  print
  print (url)
  response = urllib2.urlopen(url)
  root = ET.parse(response).getroot()
  test_results = []
  for test in root.findall('healthTest'):
    desc = test.find('description').text
    if len(desc) > 88:
      desc = desc[0:88] + '...'
    if "\n" in desc:
      desc = desc.rstrip()
    duration = test.find('durationMilliseconds').text
    result = test.find('result').text
    print "  Description: " + desc
    print "    Result: " + result
    if result == 'pass':
      test_results.append(result)
    else:
      test_results.append('fail')
      print "    Duration: " + duration 

print
