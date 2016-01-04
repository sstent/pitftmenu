import sys, pygame, socket
from pygame.locals import *
import time
import subprocess
import os
import RPi.GPIO
from pprint import pprint
from subprocess import *
os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

# Initialize pygame and hide mouse
pygame.init()
pygame.mouse.set_visible(0)

# define function for printing text in a specific place with a specific width and height with a specific colour and border
def make_button(text, xpo, ypo, height, width, colour):
    font=pygame.font.Font(None,24)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))
    pygame.draw.rect(screen, blue, (xpo-10,ypo-10,width,height),5)

# define function for printing text in a specific place with a specific colour
def make_label(text, xpo, ypo, fontsize, colour):
    font=pygame.font.Font(None,fontsize)
    label=font.render(str(text), 1, (colour))
    screen.blit(label,(xpo,ypo))

# define function that checks for touch location
def on_touch():
    # get the position that was touched
    touch_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
    #  x_min                 x_max   y_min                y_max
    # button 1 event
    if 30 <= touch_pos[0] <= 240 and 105 <= touch_pos[1] <=160:
            button(1)
    # button 2 event
    if 260 <= touch_pos[0] <= 470 and 105 <= touch_pos[1] <=160:
            button(2)
    # button 3 event
    if 30 <= touch_pos[0] <= 240 and 180 <= touch_pos[1] <=235:
            button(3)
    # button 4 event
    if 260 <= touch_pos[0] <= 470 and 180 <= touch_pos[1] <=235:
            button(4)
    # button 5 event
    if 30 <= touch_pos[0] <= 240 and 255 <= touch_pos[1] <=310:
            button(5)
    # button 6 event
    if 260 <= touch_pos[0] <= 470 and 255 <= touch_pos[1] <=310:
            button(6)

# Get Your External IP Address
def get_ip():
    ip_msg = "Not connected"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        ip_msg="IP:" + s.getsockname()[0]
    except Exception:
        pass
    return ip_msg

# Restart Raspberry Pi
def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

# Shutdown Raspberry Pi
def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def get_temp():
    command = "vcgencmd measure_temp"
    process = Popen(command.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

def run_cmd(cmd):
    process = Popen(cmd.split(), stdout=PIPE)
    output = process.communicate()[0]
    return output

# Define each button press action
def button(number):
    print "You pressed button ",number

    if number == 1:
        # desktop
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Launching Desktop", 1, (white))
        screen.blit(label,(10,120))
        pygame.display.flip()
        pygame.quit()
        subprocess.call("FRAMEBUFFER=/dev/fb1 startx", shell=True)
        #run_cmd("FRAMEBUFFER=/dev/fb1 startx")
        sys.exit()

    if number == 2:
        # exit
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Exiting to Terminal", 1, (white))
        screen.blit(label,(10,120))
        pygame.display.flip()
        pygame.quit()
        sys.exit()

    if number == 3:
        # Pretend Shutdown
        screen.fill(black)
        font=pygame.font.Font(None,48)
        label=font.render("Battery Low, Shutting down", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        time.sleep(120)
        pygame.quit()
        sys.exit()

    if number == 4:
        # Wifi Settings
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("WiFi Settings. .", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        os.system("sudo python /home/pi/pifi.py/pifi.py --gui")
        sys.exit()

    if number == 5:
        # reboot
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Rebooting. .", 1, (white))
        screen.blit(label,(40,120))
        pygame.display.flip()
        pygame.quit()
        restart()
        sys.exit()

    if number == 6:
        # shutdown
        screen.fill(black)
        font=pygame.font.Font(None,72)
        label=font.render("Shutting Down. .", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        pygame.quit()
        shutdown()
        sys.exit()



# colors    R    G    B
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
black   = (  0,   0,   0)
cyan    = ( 50, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)
orange  = (255, 127,   0)

# Set up the base menu you can customize your menu with the colors above
screen_width = 320
screen_height = 240
screen_border_width = 10
vertical_spacing = 30
horizontal_spacing = 20
headersize = 80
button_rows = 3
button_columns = 2
button_height = 35
button_width = 140

button_labels = ["Desktop","Terminal","Empty","WiFi Settings","blank","blank"]

#set size of the screen
size = screen_width, screen_height
screen = pygame.display.set_mode(size)

# Background Color
screen.fill(black)

# Outer Border
pygame.draw.rect(screen, blue, (0,0,screen_width,screen_height), screen_border_width)
pi_hostname = run_cmd("hostname")
pi_hostname = pi_hostname[:-1]


# Buttons and labels
# First Row Label
#make_label(text, xpo, ypo, fontsize, colour):
make_label(pi_hostname + " - " +  get_ip(), vertical_spacing, horizontal_spacing, 24, blue)
# Second Row buttons 3 and 4
button_iter = 0

for row in xrange(0,button_rows):
    for column in xrange(0,button_columns):
        #print ('row: {} column: {}').format(row, column)
        #button = row + column
        if row < 1:
            button_id = row + column + 1
        else:
            button_id = row + column
        pprint (button_labels[button_id])
        from_left = horizontal_spacing + (horizontal_spacing * column) + (button_width * column)
        from_top =  headersize + (vertical_spacing * row) + (button_height * row)
        print ('row: {} column: {} from_left: {} from_top: {}').format(row, column, from_left, from_top)
        make_button(button_labels[row + column], from_left, from_top, button_height, button_width, blue)

# #in pixels from left, from top, height, width
# make_button("Desktop", 40, 105, 35, 120, blue)
# make_button("Terminal", 180, 105, 35, 120, blue)
# # Third Row buttons 5 and 6
# make_button("Empty Button", 40, 180, 35, 120, blue)
# make_button("WiFi Settings", 180, 180, 35, 120, blue)
# Fourth Row Buttons
# make_button("      Reboot", 30, 255, 55, 210, blue)
# make_button("   Shutdown", 260, 255, 55, 210, blue)

# LBO Pin from Powerboost
RPi.GPIO.setmode (RPi.GPIO.BCM)
RPi.GPIO.setup(21, RPi.GPIO.IN, pull_up_down=RPi.GPIO.PUD_UP)


#While loop to manage touch screen inputs
while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
            on_touch()

        #ensure there is always a safe way to end the program if the touch screen fails
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    pygame.display.update()

    if RPi.GPIO.input(21) == RPi.GPIO.LOW:
        screen.fill(black)
        font=pygame.font.Font(None,48)
        label=font.render("Battery Low, Shutting down", 1, (white))
        screen.blit(label,(20,120))
        pygame.display.flip()
        time.sleep(10)
        pygame.quit()
        shutdown()
        sys.exit()
