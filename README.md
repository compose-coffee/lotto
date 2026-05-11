# 로또 서비스 개발 보고서 (260511)

**학과 :** 모바일시스템공학부

**학번 :** 32217647

**이름 :** 임찬형

---

## 1. 개발 환경 및 도구

- **운영체제** : Windows 11 (WSL2)
- **프레임워크** : Django 4.2+ (Python 3.11)
- **데이터베이스** : PostgreSQL 15
- **컨테이너 서버** : Docker, Docker Compose
- **편집기** : VS Code

---

## 2. 시스템 설계 및 구현 세부사항

### 2.1 Docker 가상화 구축

- **Dockerfile 작성**

Python 환경을 컨테이너화하여 OS 종속성 문제를 해결함. 

`pip install` 과정을 자동화하여 개발 환경의 일관성을 유지함.

- **멀티 컨테이너 연동**

`docker-compose.yml`을 통해 Django(Web)와 PostgreSQL(DB) 컨테이너를 생성함.

`depends_on` 설정을 통해 DB 컨테이너가 준비된 후 Web 서비스가 실행되도록 제어함.

- **데이터 보존**

Docker Volume을 설정하여 컨테이너 재부팅 시 DB 데이터가 소실되지 않도록 설계함.

### 2.2 Django 비즈니스 로직 (MVT 패턴)

- **Model 설계**

`LottoRound`(정답 회차)와 `LottoTicket`(사용자 티켓) 모델을 정의함.

`makemigrations` 및 `migrate` 명령어를 통해 PostgreSQL에 Schema를 반영함.

- **View 구현**

`random.sample`로 1~45 사이의 중복 없는 6개 번호를 생성하는 자동 구매 로직을 구현함.

- **당첨 확인 알고리즘**

사용자 티켓 번호와 관리자가 등록한 정답 번호를 `set`자료형으로 변환해 교집합 개수를 산출함.

일치 개수에 따라 1등부터 5등까지 등수 및 당첨금을 차등 지급하는 로직을 적용함.

### 2.3 템플릿 및 이벤트 연출

- **프론트엔드**

HTML과 Django Template Language를 활용하여 구매 내역 및 결과를 동적으로 출력함.

- **1등 당첨 이벤트**

`{% if %}` 조건문을 활용하여 1등 당첨 시 CSS Keyframes 애니메이션을 통한 황금빛 강조 효과를 추가하여 사용자 경험을 극대화함.

---

## 3. 트러블슈팅 (에러 해결 과정)

- **Migration 충돌**

모델 필드 추가 시 기존 데이터와의 호환성 문제로 발생한 `TypeError`를 `null=True` 설정 및 migrations 파일 초기화를 통해 해결함.

- **Template 경로 오류**

`TemplateDoesNotExist` 발생 시 Django 설정 파일(`settings.py`)의 앱 등록 상태와 `templates/lotto/` 폴더 구조를 재점검하여 경로를 정상화함.

- **DB 연결 지연**

컨테이너 실행 초기 DB 통신 오류를 `docker compose restart` 명령 및 `DATABASE` 호스트 설정 수정을 통해 해결함.

---

## 4. 테스트 및 최종 결과

본 프로젝트의 주요 기능이 정상적으로 작동함을 확인하기 위해 다음과 같은 시나리오로 테스트를 진행함.

### 4.1 Docker 컨테이너 구동 확인

Docker 환경에서 웹 서버와 데이터베이스가 정상적으로 격리되어 실행 중임을 확인함.

> 
> 
> 
> ![docker compose ps.png](attachment:c2e3c3d6-e97c-45ee-9e1a-25876fde8b61:docker_compose_ps.png)
> 
> - **설명**: `web`과 `db` 두 개의 서비스가 `Up (healthy)` 상태로 구동 중임을 확인함.

---

### 4.2 일반 사용자 로또 구매 기능

메인 페이지 접속 및 자동 번호 생성 기능을 테스트함.

> 
> 
> 
> ![main page.png](attachment:a3bf897a-e2d2-4db5-96cf-892bc6dc4f8a:main_page.png)
> 
> - **설명**: '로또 자동 구매하기' 버튼 클릭 시, 파이썬의 `random` 모듈을 통해 생성된 6개의 숫자가 구매 내역 리스트에 즉시 반영됨을 확인함.

---

### 4.3 관리자 페이지 데이터 관리 (추첨 기능)

Django Admin을 통해 당첨 번호를 등록하고 DB 연동 상태를 확인함.

> 
> 
> 
> ![3-1.png](attachment:a2e1d5fe-f093-4c26-b41d-de37f5bc30c0:3-1.png)
> 
> ![3-2.png](attachment:3c1fec7c-0f30-437e-b820-9aacd8aa4887:3-2.png)
> 
> - **설명**: 관리자가 특정 회차(예: 1회)와 당첨 번호(예: 1, 2, 3, 4, 5, 6)를 입력하여 데이터베이스 스키마에 저장함.

---

### 4.4 당첨 확인 및 결과 연출

사용자가 구매한 번호와 관리자의 당첨 번호를 비교하여 결과를 출력함.

> 
> 
> 
> ![당첨결과.png](attachment:b72821b0-8a56-4926-83cd-8600455a30eb:당첨결과.png)
> 
> ![안녕.png](attachment:bb450924-d5c5-42c7-abab-7d43afedd65a:안녕.png)
> 
> - **설명**: 6개의 숫자가 모두 일치할 경우, 구현된 CSS Animation이 적용된 황금색 강조 화면과 함께 당첨금(20억 원)이 정상적으로 표시됨을 확인함.

---

## 5. AI 도구 활용 명시

- **도구명**

Gemini (Google)

- **활용 범위**
    1. **환경 구축 -** `docker-compose.yml` 및 `Dockerfile`의 멀티 컨테이너 네트워크 구성 최적화.
    2. **트러블슈팅 -** 모델 필드 추가 시 발생한 에러 분석 및 `Migration` 초기화를 통한 DB 정합성 확보함.
    3. **로직 고도화 -** 집합 자료형을 이용한 번호 비교 알고리즘 및 1등 당첨 시 UI 이벤트 구현을 자문함.
    4. **보고서 검수 -** 기술적 구현 사항을 학술적 용어로 재구성하고, 논리적 구조 설계에 활용함.

---

## 6. 소스 코드 및 관리

- **GitHub 저장소 URL**

 [https://github.com/compose-coffee/lotto](https://www.google.com/search?q=https://github.com/compose-coffee/lotto&authuser=1)

- **주요 관리 항목**

- **Backend** : Django MVT 패턴 기반 로또 번호 생성 및 당첨 확인 로직
- **Infrastructure** : `Dockerfile`, `docker-compose.yml`을 통한 가상화 환경 구축
- **Database** : PostgreSQL 연동을 위한 스키마 정의 및 Migration 이력
- **Frontend** : CSS Animation을 활용한 당첨 결과 연출 페이지

---

## 7. 결론 및 느낀점

### 7.1 기술적 성장 및 성과

- **컨테이너 환경의 이해**

단순히 코드를 작성하는 것을 넘어, Docker를 활용해 OS 환경에 구속받지 않는 독립적인 개발 환경을 구축하는 법을 익힘. 특히 Web과 DB 컨테이너를 분리하여 관리하는 멀티 컨테이너 아키텍처를 실습하며 현대적인 백엔드 배포 프로세스를 이해하게 됨.

- **MVT 패턴의 실무 적용**

Django의 Model, View, Template 간의 데이터 흐름을 직접 구현하며, 프레임워크가 제공하는 추상화된 기능들을 활용해 복잡한 비즈니스 로직을 효율적으로 처리하는 경험을 함.

### 7.2 문제 해결 역량 강화

- **데이터베이스 마이그레이션**

실습 중 모델 수정 시 발생한 마이그레이션 충돌 문제를 해결하며, 데이터베이스 스키마 관리의 중요성과 Django의 내부 동작 원리를 깊이 있게 파악하는 계기가 됨.

- **에러 디버깅 능력**

`TemplateDoesNotExist`나 `ProgrammingError`와 같은 실무적인 에러들을 직면하고, 로그 분석과 AI 도구의 자문을 통해 원인을 파악하여 해결하는 과정을 통해 문제 해결 역량을 한 단계 높임.

### 7.3 향후 과제 및 고찰

- **확장성 고려**

현재는 단일 서버 환경이지만, 향후 실제 서비스 운영을 고려한다면 트래픽 분산 처리를 위한 로드밸런싱이나 Redis를 활용한 캐싱 처리 등을 추가로 공부해보고 싶음.

- **AI 협업 경험**

개발 과정에서 AI(Gemini)를 적절히 활용하여 단순 반복 코딩 시간을 줄이고, 논리적 설계와 트러블슈팅에 집중할 수 있었음. 이는 미래의 개발자로서 AI와 어떻게 협업 해야 하는 지에 대한 방향성을 정립하는 유익한 경험이었음.
