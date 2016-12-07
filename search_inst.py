import fnmatch
import os
import sys
import glob
import shutil

if len(sys.argv) != 3:
  print('Usage: search_inst.py <version> <product>')
  sys.exit()

version = sys.argv[1]
product = sys.argv[2]

out_dir = 'd:\\doc\\suppl'

def walklevel(some_dir, level = 1):
  some_dir = some_dir.rstrip(os.path.sep)
  assert os.path.isdir(some_dir)
  num_sep = some_dir.count(os.path.sep)
  for root, dirs, files in os.walk(some_dir):
    yield root, dirs, files
    num_sep_this = root.count(os.path.sep)
    if num_sep + level <= num_sep_this:
      del dirs[:]

def dir_search(where, what, level = 1, first = True):
  matches = []
  for root, dirnames, filenames in walklevel(where, level):
    for dirname in fnmatch.filter(dirnames, what):
      path = os.path.join(root, dirname)
      if first:
        return path
      matches.append(path)
  return matches

def file_search(where, what, level = 1, first = True):
  matches = []
  for root, dirnames, filenames in walklevel(where, level):
    for filename in fnmatch.filter(filenames, what):
      path = os.path.join(root, filename)
      if first:
        return path
      matches.append(path)
  return matches

def make_symbols_path(dst_dir):
  paths = []
  bin_dir = dir_search(dst_dir, 'bin', 3)
  paths.append(bin_dir)
  nc5000_dir = dir_search(dst_dir, 'nc5000', 4)
  paths.append(nc5000_dir)
  rs_dir = dir_search(dst_dir, 'RadarServer', 4)
  paths.append(rs_dir)
  return paths

def make_sources_path(dst_dir):
  paths = []
  src_dir = dir_search(dst_dir, 'Work')
  paths.append(src_dir)
  return paths

dir_search_pattern = version + '*'
pdb_search_pattern = 'pdb_rel_' + version + '.exe'
src_search_pattern = 'src_' + version + '.exe'

version_dir = dir_search('\\\\votts-navtech\\install', dir_search_pattern)
if os.path.exists(version_dir):
  product_dir = os.path.join(version_dir, product)
  if os.path.exists(product_dir):

    pdb_file = file_search(product_dir, pdb_search_pattern, 10)
    src_file = file_search(product_dir, src_search_pattern, 10)
    print('PDB found here: {}'.format(pdb_file))
    print('SRC found here: {}'.format(src_file))

    dst_dir = os.path.join(out_dir, version, product)
    os.makedirs(dst_dir)

    pdb_dst = os.path.join(dst_dir, os.path.basename(pdb_file))
    print ('Copy {} to {} ...'.format(pdb_file, pdb_dst))
    shutil.copy(pdb_file, pdb_dst)

    src_dst = os.path.join(dst_dir, os.path.basename(src_file))
    print ('Copy {} to {} ...'.format(src_file, src_dst))
    shutil.copy(src_file, src_dst)

    os.chdir(dst_dir)

    print ('Execute {} ...'.format(pdb_dst))
    os.system(pdb_dst)
    print ('Remove {} ...'.format(pdb_dst))
    os.remove(pdb_dst)
    symbols_path = ';'.join(make_symbols_path(dst_dir))

    print ('Execute {} ...'.format(src_dst))
    os.system(src_dst)
    print ('Remove {} ...'.format(src_dst))
    os.remove(src_dst)
    sources_path = ';'.join(make_sources_path(dst_dir))

    paths_file = os.path.join(dst_dir, 'paths.txt')
    with open(paths_file, 'w') as f:
      f.write('Symbols path:\n')
      f.write(symbols_path + '\n')
      f.write('Sources path:\n')
      f.write(sources_path + '\n')

  else:
    print('Sorry, I can\'t find {} version of {}'.format(version, product))
else:
  print('Sorry, I can\'t find {}'.format(version))


