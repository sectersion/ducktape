from pinlayout import ARM


def arm_shorted():
    return ARM.value() == 0

