const express = require('express');
const cors = require('cors');
const app = express();


app.use(cors({origin: true}));
app.use(express.json())
app.get("/", (req, res) => {
  return res.status(200).send("Hey how you doing!");
})

app.post("/api", (req, res) => {
  (async() => {
    try {
      const query = req.body.query;
      console.log(`Got query: ${query}`);
      res.status(200).json({data: query});
    }catch(error) {
      console.log(`Error: ${error}`);
      res.status(400).json({error: error});
    }
  })()
})

const PORT = process.env.PORT || 4000;

app.listen(PORT, ()=> {console.log(`Server running on port ${PORT}`)});
