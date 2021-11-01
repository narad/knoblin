import serial   
import time
from threading import Thread


from serial.tools import list_ports


min_pos = 125
max_pos = 575
mid_pos = 350

thread_running = True
servo_delay_time = 2


class KnobControllerFactory:

    def ask_yesno(self, question):
        return str(input(question+' (y/n): ')).lower().strip() == "y"

    def ask_int(self, question):
        return int(str(input(question)).lower().strip())

    def ask_str(self, question):
        return input(question).lower().strip()

    def ask_str_queue(self, question, queue):
#        print("asking str")
#        i = input(question)
#        print(i)
        queue.put(input(question).lower().strip())

    def wiggle_loop(self, arduino):
        global thread_running

    #    start_time = time.time()

        # run this while there is no input
        pole = -1
        servo = 0
        while thread_running:
            pole = pole * -1
#            time.sleep(0.1)
            arduino.write(f"{servo}:{mid_pos + (20 * pole)}".encode())

            # if time.time() - start_time >= 5:
            #     start_time = time.time()
            #     print('Another 5 seconds has passed')
            time.sleep(servo_delay_time)


    def wiggle_ask(self, question, arduino):
        queue = Queue.Queue()
        t1 = Thread(target=self.ask_str_queue, args=(question, queue))
#        t2 = Thread(target=self.ask_str(question)).start()
        t2 = Thread(target=self.wiggle_loop, args=(arduino,))

        t1.start()
        t2.start()

        
        t1.join()  # interpreter will wait until your process get completed or terminated
        t2.join()
        label = queue.get()
        print("label: ", label)
        # thread_running = False
        # print(t2)
        print('The end')


    def make_controller(self):
        ports = list_ports.comports()
        
        # create serial object for arduino control
        for i, port in enumerate(ports):
            print(f"{i+1}) {port}")
        port_ID = self.ask_int("Which port is the Arduino port? ")-1
        port_name = str(ports[port_ID])
        port_name = port_name[:port_name.index(' ')]
        print(port_name)
        arduino = serial.Serial(port_name, 9600)   

        # For testing let's actually offset the knobs to some
        # bad spot
        # print("SEtting up servos to bad spot")
        # for i in range(2):
        #     arduino.write(f"{i}:{500}".encode())
        #     time.sleep(servo_delay_time)

        # for i in range(2):
        #     arduino.write(f"{i}:{500}".encode())
        #     time.sleep(servo_delay_time)


        # setup knobs 
        num_knobs = self.ask_int("How many knobs are you sampling? ")
        # Put all knobs to center position
        _ = self.ask_yesno("Calibrating servos.  Please detach from servos from knobs as they will now return to center positon.  Please press enter when ready.")
        # The first call is usually ignored, so a
        # redundant "dummy" call is done first.
        for _ in range(2):
            for i in range(num_knobs):
                arduino.write(f"{i}:{mid_pos}".encode())
                time.sleep(servo_delay_time)
        print("Finished.  You may now attach servos to the device.")


        # Label all knobs
        labels = []
        servo_map = dict()
        for i in range(num_knobs):
            label = self.ask_str(f"What is the knob label for servo {i}? ")
            labels.append(label)
            servo_map[label] = i
            # = self.wiggle_ask("What do you caaaaall this servo? ", arduino)

        print("\nLabels:")
        for i,l in enumerate(labels):
            print(f"  servo {i} --> {l}")
        print()


        # servo_map = dict()
        # for i in range(num_knobs):
        #     print(i)

        return KnobServoController(arduino, servo_map)

    def loop(self):
        positions = [350, 450, 570]
        for i in range(2):
            for pos in positions:
                self.move_servo(i, pos)
                time.sleep(servo_delay_time)

