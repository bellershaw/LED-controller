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

    axios.put('http://192.168.0.219:8000/change_color', {},
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

  };
  return (
    <div className="App">
      <Fragment>
      <Wheel color={hsva} onChange={handleColorChange} />
      <div style={{ width: '100%', height: 34, marginTop: 20, background: hsvaToHex(hsva)}}></div>
    </Fragment>
    </div>
  );
}

export default App;
