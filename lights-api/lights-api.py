from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rpi_ws281x import *
import neopixel
import board
import time
import math

LED_COUNT       = 60
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 10
LED_BRIGHTNESS  = 0
LED_CHANNEL     = 0

lights_api = FastAPI()
lights_api.type = "00"
lights_api.break_flag = 0
origins = ["*"]

lights_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lights(BaseModel):
    red: int
    green: int
    blue: int
    brightness: int
    effect: str
    speed: int

lights_api.lights = Lights(**{
            'red': 256,
            'green': 256,
            'blue': 256,
            'brightness' : 0,
            'effect' : 'static',
            'speed': 10
                 })

strip = neopixel.NeoPixel(board.D18, 60, brightness = 1)

strip.brightness = 0
strip.fill((255,255,255))
strip.show()

@lights_api.get("/")
def get_info():
    try:
        return({
            "LED_COUNT" : LED_COUNT,
            "LED_PIN"   : LED_PIN,
            "LED_FREQ_HZ" : LED_FREQ_HZ,
            "LED_DMA" : LED_DMA,
            "LED_CHANNEL" : LED_CHANNEL,    
            "LED_BRIGHTNESS" : lights_api.lights.brightness,
            "LED_EFFECT" : lights_api.lights.effect,
            "LED_SPEED" : lights_api.lights.speed,
            "LED_COLOR" : {
                    "RED" : lights_api.lights.red,
                    "GREEN" : lights_api.lights.green,
                    "BLUE" : lights_api.lights.blue
                    }
                })
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}")

#change color
@lights_api.put("/change_color")
def change_color(red = 255, green = 0, blue = 255):
    try:
        lights_api.lights.red = red
        lights_api.lights.green = green
        lights_api.lights.blue = blue
        strip.fill((int(red), int(green), int(blue)))
        return({"LED_COLOR" : {
                    "RED" : lights_api.lights.red,
                    "GREEN" : lights_api.lights.green,
                    "BLUE" : lights_api.lights.blue
                    }
                })
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}, red={red}, green={green}, blue={blue}")

#change brightness
@lights_api.put("/change_brightness")
def change_brightness(brightness = 100):
    try:
        lights_api.lights.brightness = int(brightness)
        strip.brightness = float(brightness)/100
        return({"BRIGHTNESS" : int(lights_api.lights.brightness)})
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}, brightness={brightness}")


@lights_api.put("/fade_in")
def fade_in(max_brightness = 100, speed = 0.5):
    try:
        speed = float(speed)
        max_brightness = int(max_brightness)
        current_brightness = int(lights_api.lights.brightness)
        for i in range(0, (max_brightness - current_brightness) * 1000 + 1, int(((max_brightness - current_brightness) * 1000)/480)): 
            if lights_api.break_flag == 1:
                lights_api.break_flag = 0
                return("break flag enabled")
            lights_api.lights.brightness = max(int(min(math.ceil((current_brightness * 1000 + i)/1000),100)), lights_api.lights.brightness)
            change_brightness(lights_api.lights.brightness)
            time.sleep((1/480) / speed)
        return({"BRIGHTNESS" : int(lights_api.lights.brightness)})
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}, max_brightness={max_brightness}, speed={speed}")

@lights_api.put("/fade_out")
def fade_out(min_brightness, speed = 0.5):
    try:
        speed = float(speed)
        min_brightness = int(min_brightness)
        current_brightness = int(lights_api.lights.brightness)
        for i in range(0, (current_brightness - min_brightness) * 1000 + 1, int(((current_brightness - min_brightness) * 1000) /480)): 
            if lights_api.break_flag == 1:
                lights_api.break_flag = 0
                return("break flag enabled")
            lights_api.lights.brightness = int(math.floor((current_brightness * 1000 - i)/1000))
            change_brightness(lights_api.lights.brightness)
            time.sleep((1/480) / speed)
        return({"BRIGHTNESS" : int(lights_api.lights.brightness)})
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}, min_brightness={min_brightness}, speed={speed}")


@lights_api.put("/alarm_mode")
def alarm_mode(alarm_mode = 1):
    try:
        temp_color = [lights_api.lights.red, lights_api.lights.green, lights_api.lights.blue]
        temp_bright = lights_api.lights.brightness
        if alarm_mode:
            change_color(255,255,255)
            for i in range(0,5):
                if lights_api.break_flag == 1:
                    lights_api.break_flag = 0
                    return("break flag enabled")
                fade_in(100, 30)
                fade_out(30)
            change_color(int(temp_color[0]), int(temp_color[1]), int(temp_color[2]))
            fade_in(temp_bright)
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}")

#change effect
@lights_api.put("/breathe")
def breathe(min_brightness = 0, speed = .5):
    try:
        lights_api.lights.effect = 'breathe'
        max_brightness = lights_api.lights.brightness
        while lights_api.lights.effect == 'breathe':
            if lights_api.break_flag == 1:
                lights_api.break_flag = 0
                return("break flag enabled")
            fade_out(min_brightness, speed)
            if lights_api.break_flag == 1:
                lights_api.break_flag = 0
                return("break flag enabled")
            fade_in(max_brightness, speed)
        return({"BRIGHTNESS" : int(lights_api.lights.brightness)})
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}, min_brightness={min_brightness}, speed={speed}")

@lights_api.put("/static")
def static():
    try:
        lights_api.break_flag = 1
        lights_api.lights.effect = 'static'
        time.sleep(.1)
        change_brightness()
        return({"BRIGHTNESS" : int(lights_api.lights.brightness)})
    except Exception as err:
        return(f"Unexpected {err=}, {type(err)=}")