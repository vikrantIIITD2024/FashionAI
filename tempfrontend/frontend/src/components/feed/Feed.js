import "./feed.css"

function LoadImage(srcLoc) {
  // console.log("got src loc: ")
  return (
   <img className="outfitImage" src={srcLoc.srcLoc} alt="Recommended image"/>
  )
}

export default function Feed({imgdata, onimgdatachange}) {
  // console.log(`Got response in feed ${response}`)
  return (
  <div className="feedcontainer">
      <div className="imageContainer">
        <LoadImage srcLoc = {imgdata.text[0]} />
        <LoadImage srcLoc = {imgdata.text[1]} />
        <LoadImage srcLoc = {imgdata.text[2]} />
      </div>
  </div>
  )
}
