# 🎭 공연 리뷰 플랫폼

## 개요
- 공연 정보를 조회하고, 좋아요 및 리뷰를 작성할 수 있는 플랫폼
- 기간 : 2025. 02. 09 ~ 02. 27
- 기획 및 개발 인원 : 1명(본인)

## 테이블 모델링

## 디렉토리 구조
```
.
├── config/
├── core/
├── docker/
├── performance/
├── review/
├── tests/
└── user/
```
- **config/** : 프로젝트의 설정 파일들을 포함하는 디렉터리
- **core/** : 프로젝트의 핵심 기능 및 공통 모듈을 포함하는 디렉터리
- **docker/** : 환경 별 도커 컴포즈 파일 관리 모듈
- **performance/** : 공연 관련 기능을 담당하는 애플리케이션 디렉터리
- **review/** : 리뷰 관련 기능을 담당하는 애플리케이션 디렉터리
- **tests/** : 테스트 코드를 포함하는 디렉터리
- **user/** : 사용자 관리 기능을 담당하는 애플리케이션 디렉터리

## 구현 기능

### 공연 (Performance)
- 공연 목록 조회
- 공연 상세 내용 조회
- 공연 좋아요/좋아요 취소
- 공연 좋아요 받은 개수 조회
- 내가 좋아요한 공연 목록 조회

### 리뷰 (Review)
- 최근 등록된 리뷰 목록 조회
- 공연별 리뷰 목록 조회
- 내가 작성한 리뷰 목록 조회
- 리뷰 신고 기능
- 내가 작성한 리뷰 신고 누적 5회 시 내가 작성한 리뷰 목록에서 제외
- 신고 누적 5회 시 최근 등록 리뷰 및 공연별 리뷰 목록에서 리뷰 내용이 "신고된 리뷰입니다"로 변경 조회

### 유저 (User)
- Django 기본 `User` 모델 사용
- JWT 기반 로그인 구현
- 회원가입 시 자동 로그인 기능 구현

## 테스트 코드
- `pytest`를 사용하여 작성
- `factory_boy`와 `faker`를 이용하여 테스트 데이터 주입
- 유저 API를 제외한 모든 API 테스트 코드 작성

## 로컬 실행 환경
- `docker-compose.local.yml` 파일을 이용하여 컨테이너 실행

### 로컬 실행 방법
1. 환경 파일 세팅
   - `env` 디렉토링 생성 및 `.env` 파일 추가
     ```bash
      mkdir env && cd env && touch .env
     ```
   - `.env`에 아래 양식으로 환경 변수 추가
       ```text
        SECRET_KEY=''
        DB_HOST=''
        POSTGRES_DB=''
        POSTGRES_USER=''
        POSTGRES_PASSWORD=''
       ```
2. 도커 실행
    ```shell
    docker compose -f docker/docker-compose.local.yml up --build -d
    ```
