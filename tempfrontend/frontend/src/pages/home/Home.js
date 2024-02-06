import Searchbar from "../../components/searchbar/Searchbar"
import Feed from "../../components/feed/Feed"
import { useState } from "react"

export default function Home() {
  const [imgdata, setImgdata] = useState({text: ['something', 'random', 'else']})
  return (
    <div>
      <Searchbar imgdata={imgdata} onimgdatachange={setImgdata}/>
      <Feed imgdata={imgdata} onimgdatachange={setImgdata}/>
    </div>
  )
}
