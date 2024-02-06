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
        <p>{imgdata.text}</p>
        {
        // <LoadImage srcLoc = {srctest} />
        // <LoadImage srcLoc = {srctest2} />
        // <LoadImage srcLoc = {srctest} />
        // <LoadImage srcLoc = {srctest} />
        }
      </div>
  </div>
  )
}
