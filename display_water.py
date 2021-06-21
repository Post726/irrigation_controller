from irrigation import sql_helper
from pprint import pprint

pprint(sql_helper.get_list('temperature'))
pprint(sql_helper.get_list('water'))