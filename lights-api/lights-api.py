from fastapi import FastAPI
from pydantic import BaseModel

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

lights = Lights(**{
            'red': 256,
            'green': 256,
            'blue': 256,
            'brightness' : 50,
            'effect' : 'static',
            'speed': 10
                 })

@lights_api.get("/")
def read_root():
    print(lights)
    return({
        "LED_COUNT" : LED_COUNT,
        "LED_PIN"   : LED_PIN,
        "LED_FREQ_HZ" : LED_FREQ_HZ,
        "LED_DMA" : LED_DMA,
        "LED_BRIGHTNESS" : LED_BRIGHTNESS,
        "LED_CHANNEL" : LED_CHANNEL,    
        "LED_COLOR" : {
                "RED" : lights.red,
                "GREEN" : lights.green,
                "BLUE" : lights.blue
                }
            })

#change color
@lights_api.put("/change_color")
def change_color(red, green, blue):
    lights.red = red
    lights.green = green
    lights.blue = blue
    return({"LED_COLOR" : {
                "RED" : lights.red,
                "GREEN" : lights.green,
                "BLUE" : lights.blue
                }
            })

#change speed

#change effect