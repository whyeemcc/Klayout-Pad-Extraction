"""
please fill in the '/coordinate_&_testplan/Config.txt' correctly first.
press Shift+F5 to run me.

           |
       \       /
         .---. 
    '-.  |   |  .-'
      ___|   |___
 -=  [           ]  =-
     `---.   .---' 
  __||__ |   | __||__
  '-..-' |   | '-..-'
    ||   |   |   ||
    ||_.-|   |-,_||
  .-"`   `"`'`   `"-.
.'    Grothendieck   '.
"""

import sys
print('----------start---------')

path = sys.path[0]
path_config   = path.rstrip('lib\\python\\DLLs')+'/coordinate_&_testplan'
path_pymacros = path.rstrip('lib\\python\\DLLs')+'/pymacros'

exec(open(path_config   + '/Config.txt','rb').read())
exec(open(path_pymacros + '/check_cfg.py','rb').read())
exec(open(path_pymacros + '/core.py','rb').read())
exec(open(path_pymacros + '/to_json.py','rb').read())

Check(search_cells,pad_layer_num,pad_data_type)
core = Core(search_cells,pad_layer_num,pad_data_type)
to_json = To_json(core.get_coordinates())
to_json.puts()