import controller
from irrigation import board

board.setup_pins()

#controller.run_water(1, 60)
#controller.run_water(2, 60)
controller.run_water(3, 60)
controller.run_water(4, 60)
#controller.run_water(5, 60)
#controller.run_water(6, 60)