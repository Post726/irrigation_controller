from irrigation import sql_helper

temp = sql_helper.get_temperatures()
moisture = sql_helper.get_moistures()
water = sql_helper.get_water()

print(temp)