

# parse command line options
def cli_opts(argv, inp, call_conv):
  import sys, getopt
  
  def print_ft_exit():
    print call_conv
    sys.exit(2)
    
  try:
    opts, args = getopt.getopt(argv, ':'.join(inp.keys()) + ':')
  except getopt.GetoptError as e:
    print_ft_exit()
    print e
  except Exception as e:
    print e
    
  if len(opts) != len(inp):
    print 'Invalid option count'
    print_ft_exit()
  
  out = { }
  for opt, arg in opts:
    if opt in inp.keys():
      if inp[opt][0](arg):
        out[opt] = inp[opt][1](arg)
      else:
        print 'Invalid input type for argument %s' % opt
        print_ft_exit()
    else:
      print 'No option of form %s' % opt
      print_ft_exit()
    
  return out