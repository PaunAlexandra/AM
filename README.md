# Lyrics Video Generator

This project is a Python application that generates videos with synchronized lyrics based on an audio file and a text file containing the lyrics. The application uses libraries such as `moviepy`, `tkinter`, and machine learning models for lyrics synchronization.

## Project Structure

```
.
├── app_script.py          # GUI for user interaction
├── video_generator.py     # Script for video generation
├── whisperx_script.py     # Script for lyrics synchronization
├── pretrained_models/     # Pre-trained models for audio processing
├── .vscode/               # Visual Studio Code configurations
└── output_spleeter/       # Directory for separated audio files
```

## Requirements

1. **Python 3.8+**
2. **Conda** for virtual environment management.
3. **Python Libraries**:
   - `moviepy`
   - `tkinter`
   - `whisperx`
   - `spleeter`

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/username/lyrics-video-generator.git
   cd lyrics-video-generator
   ```

2. Create the required virtual environments:
   ```bash
   conda create -n whisperx_env python=3.8 -y
   conda activate whisperx_env
   pip install whisperx moviepy
   conda deactivate

   conda create -n spleeter_env python=3.8 -y
   conda activate spleeter_env
   pip install spleeter
   conda deactivate
   ```

3. Ensure `ImageMagick` is installed for `moviepy`:
   ```bash
   brew install imagemagick
   ```

4. Configure the path to `convert` in `video_generator.py`:
   ```python
   mpy_config({'IMAGEMAGICK_BINARY': '/opt/homebrew/bin/convert'})
   ```

## Usage

1. Run the GUI application:
   ```bash
   python app_script.py
   ```

2. Use the graphical interface to upload audio and lyrics files.

3. Click the buttons to synchronize lyrics and generate the video.

4. Generated videos will be saved in the current directory.

## Debugging

For debugging, use the `.vscode/launch.json` configuration in Visual Studio Code.

## Contributions

Contributions are welcome! Create a pull request or open an issue for suggestions and improvements.

## License

This project is licensed under the [MIT License](LICENSE).