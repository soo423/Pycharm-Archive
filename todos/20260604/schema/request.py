from pydantic import BaseModel

#할 일 생성 요청 모델
class TodoCreateRequest(BaseModel): #생성 요청 본문을 검증하기 위한 모델
    title: str # 요청 본문 필드 구성
    is_done: bool = False

#할 일 수정 요청 모델
class TodoUpdateRequest(BaseModel):
    title: str | None = None #모든 필드를 선택 필드로 설정
    is_done: bool | None = None #서버는 None인 필드