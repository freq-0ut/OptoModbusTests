from pymodbus3.client.sync import ModbusTcpClient
from time import sleep

# dictionary for configuring I/O module channels (points) in Opto22 memory map holding registers
input_output_flags = {'module1': {'ch1': 641, 'ch2': 643, 'ch3': 645, 'ch4': 647},
                      'module2': {'ch1': 649, 'ch2': 651, 'ch3': 653, 'ch4': 655},
                      'module3': {'ch1': 657, 'ch2': 659, 'ch3': 661, 'ch4': 663},
                      'module4': {'ch1': 665, 'ch2': 667, 'ch3': 669, 'ch4': 671},
                      'module5': {'ch1': 673, 'ch2': 675, 'ch3': 677, 'ch4': 679},
                      'module6': {'ch1': 681, 'ch2': 683, 'ch3': 685, 'ch4': 687},
                      'module7': {'ch1': 689, 'ch2': 691, 'ch3': 693, 'ch4': 695},
                      'module8': {'ch1': 697, 'ch2': 699, 'ch3': 701, 'ch4': 703},
                      'module9': {'ch1': 705, 'ch2': 707, 'ch3': 709, 'ch4': 711},
                      'module10': {'ch1': 713, 'ch2': 715, 'ch3': 717, 'ch4': 719},
                      'module11': {'ch1': 721, 'ch2': 723, 'ch3': 725, 'ch4': 727}}

client = ModbusTcpClient('192.168.100.12')

 # configure I/O modules (input = 0x100, output = 0x180)
client.write_register(6146, 0x180, unit=10)  #<--- this is supposed to config module 2, point 0 as an output but it doesn't work...
client.write_register(input_output_flags['module2']['ch1'], 0x180)
client.write_register(input_output_flags['module2']['ch2'], 0x180)
client.write_register(input_output_flags['module2']['ch3'], 0x180)
client.write_register(input_output_flags['module3']['ch1'], 0x180)
print("config set")

 # save configuration to flash (doesn't work... see Opto doc 1465, page 104)
#client.write_register(0, 0x00000003, unit=30)
#print("saved to flash")

 # save configuration to flash (also doesn't work... see Opto doc 1678, page 35)
#client.write_register(61496, True)
#print("saved to flash")

 # save configuration to flash (also doesn't work... see Opto doc 1678, page 35)
#client.write_coil(257, True)
#print("saved to flash")


# set module2 ch1 output high
client.write_coil(4, True)
print("done")


# scan module4 ch1 for input, send output to module3 ch1
while [True]:
    result = client.read_coils(12)
    print(result.bits[0])

    if (result.bits[0] == 1):
        for r in range(5):
            client.write_coil(8, True)
            sleep(.2)
            client.write_coil(8, False)
            sleep(.2)
    else:
        client.write_coil(8, False)

# scan module1 channels for input, send output to module2 channels
    for i in range(4):
        result = client.read_coils(i)
        print(result.bits[0])

        if (result.bits[0] == 1):
            client.write_coil(i+4, True)
        else:
            client.write_coil(i+4, False)
        
client.close()
