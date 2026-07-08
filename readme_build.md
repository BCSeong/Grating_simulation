# Grating Simulator - EXE 빌드 가이드

PyInstaller를 이용하여 Python 환경 없이 실행 가능한 standalone EXE를 생성합니다.

## 빠른 빌드

```bash
build.bat
```

실행하면:
1. PyInstaller 자동 설치
2. EXE 빌드 (onedir 모드)
3. 결과물: `dist\GratingSimulator\` 폴더

## 배포

`dist\GratingSimulator\` 폴더 전체를 배포합니다. 폴더 내의 `GratingSimulator.exe`를 실행하면 됩니다.

> **참고**: `GratingSimulator.exe` 단독으로는 실행되지 않습니다. 같은 폴더의 DLL/라이브러리가 모두 필요합니다.

## 빌드 옵션

### torch 포함 빌드

기본 빌드는 torch를 제외합니다 (Scheimpflug 시뮬레이터는 numpy fallback 사용).
GPU 가속이 필요하면 `build.bat`에서 아래 3줄을 제거하세요:

```
--exclude-module torch ^
--exclude-module torchvision ^
--exclude-module torchaudio ^
```

> **주의**: torch 포함 시 빌드 크기가 수 GB로 증가합니다.

### 디버그 빌드

GUI 실행 전 오류를 확인하려면 `build.bat`에서 `--windowed`를 `--console`로 변경하세요:

```
venv\Scripts\pyinstaller.exe --name "GratingSimulator" --console --onedir ^
```

콘솔 창이 함께 열리며 에러 메시지를 확인할 수 있습니다.

### 아이콘 추가

`.ico` 파일을 준비한 뒤 `--icon` 옵션을 추가합니다:

```
venv\Scripts\pyinstaller.exe --name "GratingSimulator" --windowed --onedir ^
    --icon "assets\icon.ico" ^
    ...
```

## 트러블슈팅

### "Failed to execute script" 오류

디버그 빌드(--console)로 전환하여 실제 에러 메시지를 확인하세요.

### DLL/모듈 누락 오류

특정 모듈이 누락된 경우 `--hidden-import` 옵션을 추가합니다:

```
--hidden-import matplotlib.backends.backend_qtagg ^
```

### 빌드 크기 최적화

불필요한 패키지를 제외하여 크기를 줄일 수 있습니다:

```
--exclude-module tkinter ^
--exclude-module unittest ^
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
    └── ...                     # 기타 의존성
```
