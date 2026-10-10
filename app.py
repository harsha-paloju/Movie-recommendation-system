from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

import pickle 

def return_saved():
    with open("recommendations.pkl","rb") as f:
    
        saved=pickle.load(f)
    
    return saved

saved=return_saved()
    
movies=saved["movies"]
similarities=saved["similarities"]

class movie(BaseModel):
    
    id:int
    
app=FastAPI()

@app.post("/recommend")
def recommend(movie_id:movie):
    
    recommend_movies=[]
    
    desire_id=movie_id.id
    desire_idx=movies[movies["id"]==desire_id].index[0]
    recommendations=[]
    for idx,similarity in similarities[desire_idx]:
        recommendations.append([idx,similarity])
        
    for idx,similarity in recommendations:
        if idx==desire_idx:
            continue
        recommend_movies.append(movies.iloc[idx]["title"])
    
    return JSONResponse(status_code=200,content=recommend_movies)

    



