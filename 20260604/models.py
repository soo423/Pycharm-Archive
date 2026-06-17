#ORM
#pip install sqlalchemy pymysql

#ORM 모델 정의(데이터를 데이터베이스 테이블과 연결할 수 있는 형태)
#ORM 모델을 사용하려면 애플리케이션이 종료되더라도 데이터는 데이터베이스에 저장되어 사라지지 않는다.

from sqlalchemy import Integer, String, Boolean #칼럼 타입
from sqlalchemy.orm import Mapped, mapped_column #ORM 칼럼 매핑 도구
from database.orm import Base #ORM 기준 클래스

#orm todo 모델 정의, base 클래스의 상속받아 할일 데이터를 정의하는 orm 모델, 데이터베이스 테이블과 1:1 매핑
class Todo(Base): #Base클래스를 상속받은 클래스만 SQLalchemy가 테이블로 인식
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True, #값 자동 증가
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False, #Not Null

    )
    is_done : Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )