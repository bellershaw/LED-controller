import './App.css';
import { Button, TextInput} from "flowbite-react";
import axios from 'axios';
import React, { useState, Fragment } from 'react';
import { ChromePicker } from "react-color";
import Wheel from '@uiw/react-color-wheel';
import { hsvaToHex, rgbaToHexa } from '@uiw/color-convert';

function App() {

  const [hsva, setHsva] = useState({ h: 214, s: 43, v: 90, a: 1 });

  const handleColorChange  = (color) => {
    setHsva({ ...hsva, ...color.hsva })
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
    setHsva({ ...hsva, ...color.hsva })
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
      console.log("ERROR ", + response);
      })
      .catch(error => {
        console.error(error);
      // Handle errors
      });

  }
  ;
  return (
    <div className="App">
      <div className="Color-Div" id="Color-Div">
        <Fragment>
          <Wheel color={hsva} onChange={handleColorChange}  className="Color-Wheel"/>
          <div className="Color-Display"/>
        </Fragment>
      </div>
      <div className="Buttons">
        <button type="button" onClick={createColorDisplay} class="text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-1vh">Add</button>
        <button type="button" class="text-white bg-gradient-to-r from-purple-500 to-pink-500 hover:bg-gradient-to-l focus:ring-4 focus:outline-none focus:ring-purple-200 dark:focus:ring-purple-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 mb-1vh">Remove</button>
      </div>
      <div className="Effects-Div">
        Effects
        <div className="Effects-Buttons">
        <Button
        title="Press me"
        onPress={() => breathe}
        />
        </div>
      </div>
    </div>
  );
}

export default App;
