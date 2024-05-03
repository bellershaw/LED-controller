from fastapi import FastAPI
from pydantic import BaseModel
from rpi_ws281x import *

LED_COUNT       = 45
LED_PIN         = 18
LED_FREQ_HZ     = 800000
LED_DMA         = 10
LED_BRIGHTNESS  = 30
LED_CHANNEL     = 0

lights_api = FastAPI()
lights_api.type = "00"

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

lights_api.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, False, lights_api.lights.brightness, LED_CHANNEL)

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
async def change_color(red, green, blue):
    lights_api.lights.red = red
    lights_api.lights.green = green
    lights_api.lights.blue = blue
    return({"LED_COLOR" : {
                "RED" : lights_api.lights.red,
                "GREEN" : lights_api.lights.green,
                "BLUE" : lights_api.lights.blue
                }
            })

#change brightness
@lights_api.put("/change_brightness")
async def change_brightness(brightness):
    lights_api.lights.brightness = brightness
    return({"BRIGHTNESS" : lights_api.lights.brightness})

#change speed

#change effect