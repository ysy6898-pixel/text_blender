from flask import Flask, request, jsonify, send_from_directory
from llm import generate_script
from blender import run_blender_script
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_SCRIPTS_DIR = os.path.join(BASE_DIR, 'generated_scripts')
os.makedirs(GENERATED_SCRIPTS_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'static', 'generated_models'), exist_ok=True)
print("Current working directory:", os.getcwd())

def generated_script_path(filename: str | None = None) -> str:
    """Return absolute path to `generated_scripts` or to a file inside it.

    Args:
        filename: optional file name (e.g. '12345.py'). If None, returns the
            directory path.

    Returns:
        Absolute path as string.
    """
    if filename:
        return os.path.join(GENERATED_SCRIPTS_DIR, filename)
    return GENERATED_SCRIPTS_DIR

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        user_prompt = request.json.get('prompt')
        if not user_prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # LLM으로 Blender 스크립트 생성
        script_code = generate_script(user_prompt)

        # 스크립트 파일 저장 (항상 절대경로 사용)
        script_name = f"{abs(hash(user_prompt))}.py"
        script_path = generated_script_path(script_name)
        with open(script_path, 'w') as f:
            f.write(script_code)

        # Blender 실행 후 GLTF 모델 생성
        output_url = run_blender_script(script_path)

        return jsonify({"script": script_code, "output": output_url})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


