from schema.response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest
from fastapi import FastAPI, status
from starlette.exceptions import HTTPException

app = FastAPI()

#할일 저장
todos = [
    {"id":1, "title":"공부하기", "is_done":False},
    {"id":2, "title":"운동하기", "is_done":True},
    {"id":3, "title":"책읽기", "is_done":False},
    {"id":4, "title":"독서", "is_done":True}
]

#전체 할일 조회
@app.get(
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
    new_todo = { # 새할일 데이터 생성
        "id":  len(todos) + 1,
        "title": body.title,
        "is_done": body.is_done
    }
    todos.append(new_todo) #리스트에서 새할일 추가후 응답 반환
    return new_todo

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



