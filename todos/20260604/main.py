from schema.response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest
from fastapi import FastAPI, status
from starlette.exceptions import HTTPException

from database.db_connection import engine, SessionFactory #데이터베이스 팩토리
from database.orm import Base
from models import Todo #ORM 모델

Base.metadata.create_all(bind=engine) #테이블 생성 지시, 이미 존재하는 테이블은 건너뛰고 없는 테이블만 생성
# 터미널에서 fastapi dev 서버 실행, 웹 애플리케이션이 실행되면서 todo 테이블이 자동으로 DB에서생성됨

app = FastAPI()


#이 클래스를 상속받는 모든 클래스는 데이터베이스 테이블로 취급한다.

#할일 저장
todos = [
    {"id":1, "title":"공부하기", "is_done":False},
    {"id":2, "title":"운동하기", "is_done":True},
    {"id":3, "title":"책읽기", "is_done":False},
]

#전체 할일 조회
@app.get( #GET_API 정의
    "/todos/{todo_id}", #경로로 접속하면 todo_id에 저장되고 함수의 매개변수로 전달
    response_model=list[TodoResponse],
    status_code = status.HTTP_200_OK)
def get_todos_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found") #예외처리
#raise HTTPException(status_code=status.HTTP_상대코드, detail="오류 메시지")

#할일 생성
@app.post(
    "/todos", #todos 경로로 들어오는 생성 요청을 처리하기 위해 post api 정의하고 함수와 연결
    response_model=TodoResponse,
    status_code = status.HTTP_201_CREATED)
def create_todo_handler(body: TodoResponse): #요청 본문을 body 매개변수로 받고 타임을 지정, fast api가 요청본문이 생성요청모델에 맞는지 검증하고 올바른 타입으로 변환해 전달
    session = SessionFactory()
    try:
        todo = Todo( #ORM 모델 객체 생성
            title = body.title,
                is_done = body.is_done
        )
        session.add(todo) #todo 모델 객체를 세션에 등록
        session.commit() #데이터베이스에 저장
        return todo # 저장이 완료된 Todo 모델 객체를 반환
    finally:
        session.close()

# 할 일 수정
@app.patch(
    "/todos/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    for todo in todos:
        if todo["id"] == todo_id:
            if body.title is not None:
                todo["title"] = body.title
            if body.is_done is not None:
                todo["is_done"] = body.is_done
            return todo #수정된 데이터 반환
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found") #예외처리 존재하지 않는 데이터를 수정하려 했을 경우

@app.delete(
    "todos/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_handler(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not Found") #예외 처리



