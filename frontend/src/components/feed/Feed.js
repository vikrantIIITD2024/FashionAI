import "./feed.css"

function LoadImage(srcLoc) {
  // console.log("got src loc: ")
  return (
   <img className="outfitImage" src={srcLoc.srcLoc} alt="Recommended image"/>
  )
}

export default function Feed() {
  let srctest = "https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/24954752/2023/9/28/373ca967-22a6-4223-859e-29271defd7641695917897722IndoEraGreenFloralPrintLivaFitFlareDress1.jpg"
  let srctest2 = "https://assets.myntassets.com/dpr_2,q_60,w_210,c_limit,fl_progressive/assets/images/23840244/2023/7/1/07a98eda-b831-453f-ae13-ae360feffa8d1688212230689ShreeRamkrishnaFabWomenTealDyedFlaredSleevesThreadWorkGeorge1.jpg"
  return (
  <div className="feedcontainer">
      <div className="imageContainer">
        <LoadImage srcLoc = {srctest} />
        <LoadImage srcLoc = {srctest2} />
        <LoadImage srcLoc = {srctest} />
        <LoadImage srcLoc = {srctest} />
      </div>
  </div>
  )
}
