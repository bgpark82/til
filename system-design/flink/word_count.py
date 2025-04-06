# pyflink.datastream: Flink의 데이터 스트림 처리를 위한 라이브러리
# StreamExecutionEnvironment: Flink 스트림 처리 실행 환경을 제공하는 클래스
from pyflink.datastream import StreamExecutionEnvironment

# pyflink.common: Flink의 공통 유틸리티와 타입 정의를 제공하는 라이브러리
# Types: Flink에서 사용되는 데이터 타입을 정의하는 클래스
from pyflink.common import Types

# Flink 실행 환경 생성
env = StreamExecutionEnvironment.get_execution_environment()
# localhost:9999 포트에서 텍스트 스트림 데이터를 읽어옴
text = env.socket_text_stream("localhost", 9999)

# 워드 카운트 로직 구현
# 워드 카운트 로직을 단계별로 구현
count = (
    # 1단계: 입력된 텍스트 라인을 단어들로 분리
    # 예: "hello world" -> ["hello", "world"]
    text.flat_map(
        lambda line: line.split(),  # 공백을 기준으로 문자열을 분리
        output_type=Types.STRING()  # 출력 타입은 문자열
    )
    
    # 2단계: 각 단어를 (단어, 1) 형태의 튜플로 변환 
    # 예: "hello" -> ("hello", 1)
    .map(
        lambda word: (word, 1),  # 각 단어를 카운트 1과 함께 튜플로 만듦
        output_type=Types.TUPLE([Types.STRING(), Types.INT()])  # (문자열, 정수) 튜플 타입 지정
    )
    
    # 3단계: 같은 단어끼리 그룹화
    # 예: ("hello", 1), ("world", 1), ("hello", 1) -> ("hello", [1,1]), ("world", [1])
    .key_by(lambda x: x[0])  # 튜플의 첫번째 요소(단어)를 키로 사용
    
    # 4단계: 그룹화된 단어들의 카운트를 합산
    # 예: ("hello", [1,1]) -> ("hello", 2)
    .sum(1)  # 튜플의 두번째 요소(카운트)를 합산
)

# 결과 출력
count.print()

# Flink 작업 실행 (작업 이름: "Socket Window WordCount")
env.execute("Socket Window WordCount")


