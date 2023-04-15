# LOFI

![](https://github.com/jacbz/lofi/actions/workflows/client.yml/badge.svg)

LOFI is a ML-supported lo-fi music generator. We trained a VAE model in [PyTorch](https://pytorch.org/) to represent a lo-fi track as a vector of 100 features. A lo-fi track consists of chords, melodies, and other musical parameters. The web client uses [Tone.js](https://tonejs.github.io/) to make a dusty lo-fi track out of these parameters.

<p align="center">
  <img src="https://repository-images.githubusercontent.com/377117802/d55ba858-636f-4c44-9195-94971754fec0" width="400px"/>
</p>

Click [here](http://lofi.jacobzhang.de/?default) for a pre-generated lo-fi playlist!

## Architecture

* **Client**: The client is written in TypeScript and built with Webpack. It uses Tone.js to generate music.
* **Model**: The model is implemented in PyTorch. We synthesized various datasets, including Hooktheory and Spotify.
* **Server**: The server is a basic Flask instance that deploys the trained model checkpoint. The client communicates with the Server using a REST API.

![](https://svgshare.com/i/ZG9.svg)


## Commands

```bash
ffmpeg -i \#1534512580463132377720656799780042553589113514594303783976.mp3 -framerate 30 -i 00020-2972180868.png     -c:v libx265 -x265-params
lossless=1     -pix_fmt yuv420p      -movflags faststart     out.mp4
```
```bash
ffmpeg -loop 1 -i 00020-2972180868.png  -i \#1534512580463132377720656799780042553589113514594303783976.mp3 -shortest -acodec copy -vcodec mjpeg result.mp4

```
```bash
ffmpeg -loop 1 -i 00020-2972180868.png -i \#1534512580463132377720656799780042553589113514594303783976.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest out.mp4


```
