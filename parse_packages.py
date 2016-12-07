import re
packages_file = 'packages.txt'

name_regex = 'Product Name:(.*)'
vers_regex = 'Version:(.*)'

pkg_name = ''
pkg_vers = ''
pkg_dict = {}

pkg_names_dict = {'PkgInFile':'PkgOnServer'}

with open(packages_file, 'r') as f:
  for line in f:
    pkg_name_match = re.search(name_regex, line)
    if pkg_name_match:
      pkg_name = pkg_name_match.group(1).strip()
    pkg_vers_match = re.search(vers_regex, line)
    if pkg_vers_match:
      pkg_vers = pkg_vers_match.group(1).strip()
      pkg_dict[pkg_name] = pkg_vers

for k, v in pkg_dict.items():
  if k in pkg_names_dict:
    print(pkg_names_dict[k], v)
  else:
    print(k, v)
