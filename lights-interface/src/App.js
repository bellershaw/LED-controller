import './App.css';
import { Button, TextInput} from "flowbite-react";
import axios from 'axios';
import React, { useState, Fragment } from 'react';
import { ChromePicker } from "react-color";
import Wheel from '@uiw/react-color-wheel';
import { hsvaToHex, rgbaToHexa } from '@uiw/color-convert';
import Slider from '@mui/material/Slider';
import Box from '@mui/material/Box';

function App() {

  const [hsva, setHsva] = useState({ h: 0, s: 0, v: 100, a: 1 });
  const [bgColor, setBgColor] = useState({ r: 255, g: 255, b: 255, a: 0 });
  const [breatheSlider, setBreatheSlider] = React.useState([0, 10]);
  const [breatheMin, setBreatheMin] = React.useState(0);
  const [speed, setSpeed] = React.useState(1.0);

  const handleColorChange  = (color) => {
    
    setHsva({ ...hsva, ...color.hsva })
    setBgColor({r: color.rgb.r, g: color.rgb.g, b: color.rgb.b, a: bgColor.a})
    console.log('bgcolor', bgColor)
    console.log('color', color)
    console.log(color.rgb)
    console.log(color.g)
    
    axios.put('http://192.168.0.2:8000/change_color', {},
     { params : {
      red : color.rgb.r,
      green : color.rgb.g,
      blue : color.rgb.b}}
    )
     .then(response => {
      //Handle the response
      console.log("REPSONSE ", + response);
      })
      .catch(error => {
        console.error(error);
      // Handle errors
      });

  }

  const handleBrightnessChange  = (new_brightness) => { 
    setBgColor({r: bgColor.r, g: bgColor.g, b: bgColor.b, a: (new_brightness.target.value/100)})
    console.log('bgcolor', bgColor)
    
    axios.put('http://192.168.0.2:8000/change_brightness', {},
     { params : {
      brightness : new_brightness.target.value}}
    )
     .then(response => {
      //Handle the response
      console.log("ERROR ", + response);
      })
      .catch(error => {
        console.error(error);
      // Handle errors
      });

  }

  async function createColorDisplay(){
        const color_div = document.getElementById("Color-Div") 
        console.log(color_div)
        const color_display = document.createElement("div")
        color_display.className = "Color-Display"
        color_div.appendChild(color_display)
  } 

  const breathe  = (color) => {
    axios.put('http://192.168.0.2:8000/breathe', {},
     { params : {
      min_brightness : breatheMin,
      speed : speed
    }}
    )
     .then(response => {
      //Handle the response
      console.log("ERROR ", + response);
      })
      .catch(error => {
        console.error(error);
      // Handle errors
      });

  }
    const minDistance = 10;
    const handleBreatheSlider  = (event, newValue, activeThumb) => {
    if (newValue[1] - newValue[0] < minDistance) {
          if (activeThumb === 0) {
            const clamped = Math.min(newValue[0], 100 - minDistance);
            setBreatheSlider([clamped, clamped + minDistance]);
          } else {
            const clamped = Math.max(newValue[1], minDistance);
            setBreatheSlider([clamped - minDistance, clamped]);
          }
        } else {
          setBreatheSlider(newValue);
        }
        setBreatheMin(newValue[0])
        setBgColor({r: bgColor.r, g: bgColor.g, b: bgColor.b, a: (newValue[1]/100)})
        axios.put('http://192.168.0.2:8000/change_brightness', {},
          { params : {
            brightness : newValue[1]}}
          )
          .then(response => {
            //Handle the response
            console.log("ERROR ", + response);
            })
            .catch(error => {
              console.error(error);
            // Handle errors
            });
      };

    const handleSpeedChange  = (new_speed) => {
        setSpeed(new_speed.target.value);
      };

  const solid  = (error) => {
    axios.put('http://192.168.0.2:8000/static', {},
     { params : {
      max_brightness : (bgColor.a * 100)}}
    )
     .then(response => {
      //Handle the response
      console.log("ERROR ", + response);
      })
      .catch(error => {
        console.error(error);
      // Handle errors
      });

  }

  ;
  return (
    <div className="App" style={{backgroundColor: '#2b2b2b'}}>
      <div className="App-body" style={{backgroundColor: `rgba(${bgColor.r}, ${bgColor.g}, ${bgColor.b}, ${bgColor.a})`}}>
        <div className="Content">
          <div className="Color-Div" id="Color-Div">
            <Fragment>
              <Wheel color={hsva} onChange={handleColorChange}  className="Color-Wheel"/>
            </Fragment>
          </div>
          <div className="Brightness-Slider">
            Brightness
          <Slider defaultValue={0} valueLabelDisplay="auto" onChange={handleBrightnessChange}/>
          </div>
            <button type="button" class="text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l focus:ring-4 focus:outline-none focus:ring-purple-200 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-1vh" onClick={solid}>Solid</button>
            <button type="button" class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-1vh" onClick={breathe}>Breathe</button>
            <Slider
              value={breatheSlider}
              onChange={handleBreatheSlider}
              valueLabelDisplay="auto"
              disableSwap
            />
            <Slider min={0.1} max={5.0} defaultValue={.5} step={0.1} valueLabelDisplay="auto" onChange={handleSpeedChange}/>
          </div>
      </div>
    </div>
  );
}

export default App;
