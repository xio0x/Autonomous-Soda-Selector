import RPi.GPIO as GPIO
import time

# Pin setup
# Right motor driver
RPWM_R = 23
LPWM_R = 24
R_EN_R = 27
L_EN_R = 22

# Left motor driver
RPWM_L = 17
LPWM_L = 18
R_EN_L = 5
L_EN_L = 6

# PWM settings
frequency = 1000  # Hz
speed = 75        # Duty cycle (0–100)

# GPIO setup
GPIO.setmode(GPIO.BCM)
all_pins = [RPWM_R, LPWM_R, R_EN_R, L_EN_R,
            RPWM_L, LPWM_L, R_EN_L, L_EN_L]
GPIO.setup(all_pins, GPIO.OUT)

# PWM initialization
pwm_r_r = GPIO.PWM(RPWM_R, frequency)
pwm_l_r = GPIO.PWM(LPWM_R, frequency)
pwm_r_l = GPIO.PWM(RPWM_L, frequency)
pwm_l_l = GPIO.PWM(LPWM_L, frequency)

pwm_r_r.start(0)
pwm_l_r.start(0)
pwm_r_l.start(0)
pwm_l_l.start(0)

# Movement functions
def stop():
    for pin in [R_EN_R, L_EN_R, R_EN_L, L_EN_L]:
        GPIO.output(pin, GPIO.LOW)
    for pwm in [pwm_r_r, pwm_l_r, pwm_r_l, pwm_l_l]:
        pwm.ChangeDutyCycle(0)
                
    time.sleep(0.25)

def forward():
    GPIO.output(R_EN_R, GPIO.HIGH)
    GPIO.output(L_EN_R, GPIO.HIGH)
    GPIO.output(R_EN_L, GPIO.HIGH)
    GPIO.output(L_EN_L, GPIO.HIGH)

    pwm_r_r.ChangeDutyCycle(speed)
    pwm_l_r.ChangeDutyCycle(0)
    
    # REVERSE LEFT MOTOR POLARITY
    pwm_r_l.ChangeDutyCycle(0)
    pwm_l_l.ChangeDutyCycle(speed)


def backward():
    GPIO.output(R_EN_R, GPIO.HIGH)
    GPIO.output(L_EN_R, GPIO.HIGH)
    GPIO.output(R_EN_L, GPIO.HIGH)
    GPIO.output(L_EN_L, GPIO.HIGH)

    pwm_r_r.ChangeDutyCycle(0)
    pwm_l_r.ChangeDutyCycle(speed)

    # REVERSE LEFT MOTOR POLARITY
    pwm_r_l.ChangeDutyCycle(speed)
    pwm_l_l.ChangeDutyCycle(0)


def turn_left():
    GPIO.output(R_EN_R, GPIO.HIGH)
    GPIO.output(L_EN_R, GPIO.HIGH)
    GPIO.output(R_EN_L, GPIO.HIGH)
    GPIO.output(L_EN_L, GPIO.HIGH)

    pwm_r_r.ChangeDutyCycle(speed)   # Right forward
    pwm_l_r.ChangeDutyCycle(0)

    pwm_r_l.ChangeDutyCycle(speed)   # Left backward (reversed)
    pwm_l_l.ChangeDutyCycle(0)

    time.sleep(0.6)
    stop()


def turn_right():
    GPIO.output(R_EN_R, GPIO.HIGH)
    GPIO.output(L_EN_R, GPIO.HIGH)
    GPIO.output(R_EN_L, GPIO.HIGH)
    GPIO.output(L_EN_L, GPIO.HIGH)

    pwm_r_r.ChangeDutyCycle(0)       # Right backward
    pwm_l_r.ChangeDutyCycle(speed)

    pwm_r_l.ChangeDutyCycle(0)       # Left forward (reversed)
    pwm_l_l.ChangeDutyCycle(speed)

    time.sleep(0.6)
    stop()

def cleanup():
    stop()
    pwm_r_r.stop()
    pwm_l_r.stop()
    pwm_r_l.stop()
    pwm_l_l.stop()
    GPIO.cleanup()

# Test routine
if __name__ == "__main__":
    try:
        print("Forward for 2 seconds")
        forward()
        time.sleep(2)
        stop()

        print("Turn left for 2 seconds")
        turn_left()

        print("Turn right for 2 seconds")
        turn_right()

        print("Backward for 2 seconds")
        backward()
        time.sleep(2)

        print("Stopping")
        stop()

    except KeyboardInterrupt:
        pass

    finally:
        stop()
        pwm_r_r.stop()
        pwm_l_r.stop()
        pwm_r_l.stop()
        pwm_l_l.stop()
        GPIO.cleanup()
