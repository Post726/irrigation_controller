from irrigation import sql_helper
from pprint import pprint

pprint(sql_helper.Zone().get_list('temperature'))
pprint(sql_helper.Water().get_list('water'))