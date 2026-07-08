# Grating Simulator - EXE 빌드 가이드

PyInstaller를 이용하여 Python 환경 없이 실행 가능한 standalone EXE를 생성합니다.

## 빠른 빌드

```bash
build.bat
```

실행하면:
1. PyInstaller 자동 설치
2. CPU-only torch 설치 (CUDA 제외, 빌드 크기 억제)
3. EXE 빌드 (onedir 모드)
4. 결과물: `dist\GratingSimulator\` 폴더 (~500MB)

> **참고**: CUDA torch를 그대로 번들하면 ~2-3GB가 됩니다. CPU-only torch로 ~500MB에 억제됩니다. Scheimpflug 시뮬레이터는 torch CPU로 동작합니다.

## 배포

`dist\GratingSimulator\` 폴더 전체를 배포합니다. `GratingSimulator.exe`를 실행하면 됩니다.

> **참고**: `GratingSimulator.exe` 단독으로는 실행되지 않습니다. 같은 폴더의 DLL/라이브러리가 모두 필요합니다.

## 빌드 후 개발환경 복구

`build.bat`은 venv의 torch를 CPU-only로 교체합니다. 개발용 CUDA torch를 복구하려면:

```bash
venv\Scripts\pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

## 커스텀 옵션

### 디버그 빌드

GUI 실행 전 오류를 확인하려면 bat 파일에서 `--windowed`를 `--console`로 변경:

```
venv\Scripts\pyinstaller.exe --name "GratingSimulator" --console --onedir ^
```

### 아이콘 추가

`.ico` 파일을 준비한 뒤 `--icon` 옵션 추가:

```
--icon "assets\icon.ico" ^
```

## 트러블슈팅

### "Failed to execute script" 오류

디버그 빌드(`--console`)로 전환하여 실제 에러 메시지를 확인하세요.

### DLL/모듈 누락 오류

특정 모듈이 누락된 경우 `--hidden-import` 옵션을 추가:

```
--hidden-import matplotlib.backends.backend_qtagg ^
```

## 요구사항

- Python 3.9+ (빌드 환경)
- Windows 10/11
- venv 생성 완료 (`install.bat` 실행 후)

## 생성되는 파일 구조

```
dist\
└── GratingSimulator\
    ├── GratingSimulator.exe    # 실행 파일
    ├── python3xx.dll           # Python 런타임
    ├── PySide6\                # Qt 라이브러리
    ├── matplotlib\             # matplotlib 데이터
    ├── torch\                  # torch CPU 런타임
    └── ...                     # 기타 의존성
```
