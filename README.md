####	Date: 18-05-2026

#	Audio Spectogram - OpenGL, Python, PyAudio

Visualizing an `.wav` audio file's data in its time domain and frequency domain, and implementing a realtime audio data visualization of audio data recorded straight from the microphone.

### Github Repo:
[`Git Repo`](https://github.com/OnyebuchiDeji/AudioSpectogram-Pypy_OpenGL)


###	Key Features

+	Utilized pyaudio to read `wav` files and read them as a stream of data to extract time-domain data.
+	Utilized PyQT for window creation and Moderngl capabilities..
+	Utilized Short Fourier Transform to separate `wav` audio samples into frequency bands (frequency domain of data).
+	Utliized Moderngl shaders to write to GPU and visualize time domain and frequency domain.
+	Performs in Realtime using callback architecture by library, pyaudio to stream data directly from microphone.


###	Tech Stack

+	PyQT, Moderngl, Pyaudio, Librosa (for fourier transform functions), Pyrr (for Matrix functions)


##	Setup Instructions
>	Install Python
>	Install Pip
>	Install Make either by msys64, on wsl, or Linux environment
1.	Create & Activate Environment:
	-	`python -m venv .venv`
	-	`.venv\Scripts\activate.bat`
2.	Install Dependencies:
	-	`pip install -r requirements.txt`
3.	Run (in root directory):
	-	`make`
	+	Or Run using Python if can't install Make:
	-	`python app/main.py`

####	References

+	Dystopian Dev (2023), "Audio Spectogram - Python + OpenGL + ...". Nov 4, 2024 [Youtube]. Available at: https://youtu.be/uapmmpA1wMk?si=r2DQDGFk_T4dbRwE. (Last Accessed: 18-05-2026)


### Architecture Diagram

```
AudioSpectogram-Pypy_OpenGL/
 ├── res/
 │	├── scooby.wav
 │	└── scooby.mp3
 ├── requirements.txt
 ├── README.md
 ├── Makefile
 ├── LICENSE
 ├── fonts/
 │	├── Rubik-Regular.ttf
 │	└── Agbalumo,Atomic_Age,Baumans,Cambo,EB_Garamond,etc.zip
 ├── app/
 │	├── window.py
 │	├── wave.py
 │	├── utils.py
 │	├── ticks.py
 │	├── text.py
 │	├── spec.py
 │	├── source.py
 │	├── rect.py
 │	├── main.py
 │	└── config.py
 ├── .pddignore
 └── .gitignore
```

###	Screenshots

![image0](./_scrnshots/scrnshot0.png)
![image1](./_scrnshots/scrnshot1.png)
![image2](./_scrnshots/scrnshot2.png)
![image3](./_scrnshots/scrnshot3.png)
![image4](./_scrnshots/scrnshot4.png)
![image5](./_scrnshots/scrnshot5.png)
![image6](./_scrnshots/scrnshot6.png)
![image7](./_scrnshots/scrnshot7.png)
![image8](./_scrnshots/scrnshot8.png)
![image9](./_scrnshots/scrnshot9.png)
![image10](./_scrnshots/scrnshot10.png)
![image11](./_scrnshots/scrnshot11.png)
![image12](./_scrnshots/scrnshot12.png)
![image13](./_scrnshots/scrnshot13.png)
![image14](./_scrnshots/scrnshot14.png)
![image15](./_scrnshots/scrnshot15.png)
![image16](./_scrnshots/scrnshot16.png)
![image17](./_scrnshots/scrnshot17.png)
