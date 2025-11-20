import subprocess
import os
import sys
import platform

def get_blender_path():
    system = platform.system()
    if system == "Darwin":  # Mac
        return "/Applications/Blender.app/Contents/MacOS/Blender"
    elif system == "Linux":
        return "/usr/bin/blender"
    elif system == "Windows":
        # 가장 흔한 설치 경로 (버전별 폴더 감안)
        default_path = r"C:\Program Files\Blender Foundation"
        
        # 폴더 내부에서 blender.exe 자동 탐색
        for root, dirs, files in os.walk(default_path):
            if "blender.exe" in files:
                return os.path.join(root, "blender.exe")
        
        # 자동 탐색 실패 시 fallback 경로
        return r"C:\Program Files\Blender Foundation\Blender\blender.exe"
    else:
        raise RuntimeError("Unsupported OS")

def run_blender_script(script_path: str) -> str:
    output_file = script_path.replace(".py", ".png")
    BLENDER_PATH = get_blender_path()
    cmd = [
       BLENDER_PATH, "-b", "-P", script_path,
       "--", output_file
	]

    #로그------------------------

    print("▶ Running Blender:")
    print("  ", " ".join(cmd))
    print("▶ Output will be:", output_file)
    print("-" * 60)

    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # stderr도 같이 보기
        text=True,
        bufsize=1,
    )
    for line in process.stdout:
        print("[BLENDER]", line, end="")
    
    process.wait()

    print("\n" + "-" * 60)
    print("▶ Blender return code:", process.returncode)
    #-----------------------------------
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print("Blender Error:", result.stderr)
        raise RuntimeError("Blender script failed")
    return f"/static/generated_models/{os.path.basename(output_file)}"

