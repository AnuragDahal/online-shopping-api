from fastapi import Response, APIRouter

router = APIRouter(tags=["cookie"])


@router.post("/session/")
def cookie(response: Response):
    response.set_cookie(key="mysession", value="1242r")
    return {"message": "Wanna cookie?"}
