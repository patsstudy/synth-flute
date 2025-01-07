import pygame
import numpy as np
from gpiozero import Button
from signal import pause
import time

# Initialize pygame mixer to play sounds
pygame.mixer.init(frequency=22050, size=-16, channels=2)

# Variables to track the current octave, sharp state, chord mode, and major/minor toggle
current_octave = 4
sharp_pressed = False
chord_mode = False  # False for single note mode, True for chord mode
minor_chord = False  # False for major chords, True for minor chords

# Frequencies for the notes
NOTES = {
    'C': 261.63,  'C#': 277.18, 'D': 293.66,  'D#': 311.13, 'E': 329.63,
    'F': 349.23,  'F#': 369.99, 'G': 392.00,  'G#': 415.30, 'A': 440.00,
    'A#': 466.16, 'B': 493.88
}

# Function to generate a sine wave for a given frequency
def generate_tone(frequency, duration=0.5, sample_rate=22050):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t) * 32767
    return np.array(wave, dtype=np.int16)

# Function to play a chord sound (list of notes)
def play_chord(notes):
    for note in notes:
        frequency = NOTES.get(note, 440)  # Default to A if note not found
        sound_wave = generate_tone(frequency * 2 ** (current_octave - 4))  # Adjust frequency by octave
        sound = pygame.sndarray.make_sound(sound_wave)
        sound.play()
        time.sleep(0.5)  # Wait for the sound to finish

# Function to play a single note
def play_sound(note):
    if sharp_pressed:
        note = f'{note}#'  # Add sharp symbol (#) to the note if sharp button is pressed
    frequency = NOTES.get(note, 440)  # Default to A if note not found
    sound_wave = generate_tone(frequency * 2 ** (current_octave - 4))  # Adjust frequency by octave
    sound = pygame.sndarray.make_sound(sound_wave)
    sound.play()

# Functions to set the octave based on button press
def octave_3():
    global current_octave
    current_octave = 3
    print(f"Current octave: {current_octave}")

def octave_4():
    global current_octave
    current_octave = 4
    print(f"Current octave: {current_octave}")

def octave_5():
    global current_octave
    current_octave = 5
    print(f"Current octave: {current_octave}")

def octave_6():
    global current_octave
    current_octave = 6
    print(f"Current octave: {current_octave}")

# Function to toggle sharp note
def toggle_sharp():
    global sharp_pressed
    sharp_pressed = True
    print("Sharp button pressed")

# Function to release sharp note
def release_sharp():
    global sharp_pressed
    sharp_pressed = False
    print("Sharp button released")

# Function to toggle chord mode
def toggle_chord_mode():
    global chord_mode
    chord_mode = not chord_mode  # Toggle the chord mode
    print(f"Chord mode: {'Enabled' if chord_mode else 'Disabled'}")

# Function to toggle between major and minor chords
def toggle_minor_major():
    global minor_chord
    minor_chord = not minor_chord  # Toggle between major and minor chords
    print(f"Chord type: {'Minor' if minor_chord else 'Major'}")

# Setup buttons (replace GPIO pins with your actual pin numbers)
button_1 = Button(17)  # C
button_2 = Button(27)  # D
button_3 = Button(22)  # E
button_4 = Button(5)   # F
button_5 = Button(6)   # G
button_6 = Button(13)  # A
button_7 = Button(19)  # B
octave_button_3 = Button(26)  # Octave 3 button
octave_button_4 = Button(21)  # Octave 4 button (default)
octave_button_5 = Button(20)  # Octave 5 button
octave_button_6 = Button(16)  # Octave 6 button
sharp_button = Button(12)  # Sharp button
chord_button = Button(25)  # Chord toggle button
minor_major_button = Button(24)  # Major/Minor toggle button

# Define chords (major and minor versions)
def get_chord_notes(note):
    if note == 'C':
        return ['C', 'E', 'G'] if not minor_chord else ['C', 'Eb', 'G']  # C major or minor
    elif note == 'D':
        return ['D', 'F#', 'A'] if not minor_chord else ['D', 'F', 'A']  # D major or minor
    elif note == 'E':
        return ['E', 'G#', 'B'] if not minor_chord else ['E', 'G', 'B']  # E major or minor
    elif note == 'F':
        return ['F', 'A', 'C'] if not minor_chord else ['F', 'Ab', 'C']  # F major or minor
    elif note == 'G':
        return ['G', 'B', 'D'] if not minor_chord else ['G', 'Bb', 'D']  # G major or minor
    elif note == 'A':
        return ['A', 'C#', 'E'] if not minor_chord else ['A', 'C', 'E']  # A major or minor
    elif note == 'B':
        return ['B', 'D#', 'F#'] if not minor_chord else ['B', 'D', 'F#']  # B major or minor
    return [note]  # Return the note itself if no chord is found

# Assign each note button to play the corresponding note or chord with current octave
def button_pressed(note):
    if chord_mode:
        notes = get_chord_notes(note)
        play_chord(notes)
    else:
        play_sound(note)

button_1.when_pressed = lambda: button_pressed('C')
button_2.when_pressed = lambda: button_pressed('D')
button_3.when_pressed = lambda: button_pressed('E')
button_4.when_pressed = lambda: button_pressed('F')
button_5.when_pressed = lambda: button_pressed('G')
button_6.when_pressed = lambda: button_pressed('A')
button_7.when_pressed = lambda: button_pressed('B')

# Assign octave buttons to change the octave
octave_button_3.when_pressed = octave_3
octave_button_4.when_pressed = octave_4
octave_button_5.when_pressed = octave_5
octave_button_6.when_pressed = octave_6

# Assign sharp button to toggle sharp notes
sharp_button.when_pressed = toggle_sharp
sharp_button.when_released = release_sharp

# Assign chord button to toggle chord mode
chord_button.when_pressed = toggle_chord_mode

# Assign major/minor toggle button
minor_major_button.when_pressed = toggle_minor_major

# Wait for button presses
pause()


