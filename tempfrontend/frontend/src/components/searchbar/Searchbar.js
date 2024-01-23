import { Checkroom, Menu, Search } from "@mui/icons-material"
import "./searchbar.css"

async function connect(inputVal) {
  console.log("Got inputVal", inputVal);
  const options = {
    method:"post",
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(inputVal),
  };
  await fetch("http://localhost:4000/api", options).then(response => response.json()).then(
    data=> {
      console.log("Got data:",data)
      return data
    }).catch(error => {
        console.log("Error: ",error);
    })
}

async function handleKeyPressed(event) {
  console.log("Calling this");
  if (event.key === 'Enter') {
    console.log("Enter was pressed");
    const inputVal = document.getElementById("searchbox").value;
    console.log("Got value: "+inputVal);

    const response = await connect({'query': inputVal})

    console.log("Got response: ", response);
  }
}

export default function Searchbar() {
  return (
    <div className="containerSearch">
      <div className="logo"> <Checkroom className="logoicon" /></div>
      <div className="query"> 
        <Search className="searchicon"/>
        <input placeholder="Enter your query here" className="searchquery" id='searchbox' onKeyDown={handleKeyPressed}/>
      </div>
      <div className="options"><Menu className="menu"/></div>
    </div>
  )
}
