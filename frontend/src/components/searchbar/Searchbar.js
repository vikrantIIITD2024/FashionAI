import { Checkroom, Menu, Search } from "@mui/icons-material"
import "./searchbar.css"

export default function Searchbar() {
  return (
    <div className="containerSearch">
      <div className="logo"> <Checkroom className="logoicon" /></div>
      <div className="query"> 
        <Search className="searchicon"/>
        <input placeholder="Enter your query here" className="searchquery"/>
      </div>
      <div className="options"><Menu className="menu"/></div>
    </div>
  )
}
