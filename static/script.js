document.addEventListener("DOMContentLoaded", () => {
  const allPlayers = document.querySelectorAll("audio");
  allPlayers.forEach((player) => {
    player.addEventListener("play", () => {
      allPlayers.forEach((other) => {
        if (other !== player) other.pause();
      });
    });
  });
});

const player = document.getElementById("mainPlayer");
const source = document.getElementById("mainSource");
const nowPlaying = document.getElementById("nowPlaying");

function playCurrent(track) {
  source.src = `/static/music/${track}`;
  player.load();
  player.play();
  nowPlaying.textContent = `Сейчас играет: ${track}`;
}

function playRandom(tracks) {
  const randomIndex = Math.floor(Math.random() * tracks.length);
  const randomTrack = `/static/music/${tracks[randomIndex]}`;
  source.src = randomTrack;
  player.load();
  player.play();
  nowPlaying.textContent = `Сейчас играет: ${tracks[randomIndex]}`;
}

function pauseAudio() {
  if (!player.paused) {
    player.pause();
  } else {
    player.play();
  }
}

function stopAudio() {
  player.pause();
  player.currentTime = 0;
}
