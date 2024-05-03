import './App.css';
import { Button, TextInput} from "flowbite-react";
import axios from 'axios';
import React, { useState } from 'react';
import { ChromePicker } from "react-color";

function App() {

  const [color, setColor] = useState("");

  const handleColorChange  = (e) => {
    setColor(e.rgb);
    console.log(e)
    axios.put('http://192.168.0.219:8000/change_color', {},
     { params : {
      red : e.rgb.r,
      green : e.rgb.g,
      blue : e.rgb.b}}
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
      <div>
        <label for="text_input" class="mb-2 text-sm font-medium text-gray-100 m-2">Text Input</label>
        <input type="text" class="bg-black border border-gray-100 text-gray-100 text-sm rounded-sm m-2" placeholder="Enter Text"/>
      </div>
      <ChromePicker
        color={color}
        onChange={handleColorChange}
      />
    </div>
  );
}

export default App;
