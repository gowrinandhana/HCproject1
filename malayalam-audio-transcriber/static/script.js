let audioFile = "";

function startRecording() {
  document.getElementById("mic").style.display = "block";
  document.getElementById("transcript").value = "";

  fetch("/start-recording", { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
      audioFile = data.file;
      console.log("Recording done:", audioFile);
    });
}

function getTranscript() {
  document.getElementById("mic").style.display = "none";

  fetch("/transcribe")
    .then((res) => res.json())
    .then((data) => {
      if (data.transcript) {
        document.getElementById("transcript").value = data.transcript;

        const audioPlayer = document.getElementById("player");
        audioPlayer.src = `/uploads/${audioFile}`;
        audioPlayer.style.display = "block";
        audioPlayer.play();
      } else {
        document.getElementById("transcript").value = "Transcription failed.";
      }
    });
}
