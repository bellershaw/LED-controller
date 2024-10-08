from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rpi_ws281x import *
import neopixel
import board
import time

LED_COUNT       = 60
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 10
LED_BRIGHTNESS  = 30
LED_CHANNEL     = 0

lights_api = FastAPI()
lights_api.type = "00"

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
            'brightness' : 50,
            'effect' : 'static',
            'speed': 10
                 })

strip = neopixel.NeoPixel(board.D18, 60, brightness = 1)

strip.brightness = 0.1
strip.fill((255,255,255))
strip.show()

@lights_api.get("/")
async def get_info():
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

#change color
@lights_api.put("/change_color")
def change_color(red, green, blue):
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

#change brightness
@lights_api.put("/change_brightness")
def change_brightness(brightness):
    lights_api.lights.brightness = brightness
    strip.brightness = float(brightness)/100
    return({"BRIGHTNESS" : int(lights_api.lights.brightness)})

@lights_api.put("/fade_in")
def fade_in(max_brightness):
    max_brightness = float(max_brightness)
    for i in range(0, int(max_brightness + 1), int(max_brightness/40)): 
        lights_api.lights.brightness = i
        strip.brightness = float(i)/100
        time.sleep(.05)
    return({"BRIGHTNESS" : int(lights_api.lights.brightness)})

@lights_api.put("/fade_out")
def fade_out():
    brightness = lights_api.lights.brightness
    for i in range(0, int(brightness + 1), int(brightness/40)): 
        lights_api.lights.brightness = brightness-i
        strip.brightness = float(brightness-i)/100
        time.sleep(.05)
    return({"BRIGHTNESS" : int(lights_api.lights.brightness)})


@lights_api.put("/alarm_mode")
def alarm_mode(alarm_mode):
    temp_color = [lights_api.lights.red, lights_api.lights.green, lights_api.lights.blue]
    temp_bright = lights_api.lights.brightness
    if alarm_mode:
        for i in range(0,1):
            change_color(255,255,255)
            fade_in(100)
            fade_out()
        change_color(int(temp_color[0]), int(temp_color[1]), int(temp_color[2]))
        fade_in(temp_bright)
#change speed

#change effect
    