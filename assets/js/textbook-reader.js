const GOOGLE_TTS_VALUE = "__google_tts__";
const voiceSelect = document.getElementById("voiceSelect");
const stopButton = document.getElementById("stopButton");
const statusEl = document.getElementById("ttsStatus");
const topButton = document.getElementById("topButton");

let voices = [];
let activeButton = null;
let currentAudio = null;

function setStatus(message, isError = false) {
  if (!statusEl) return;
  statusEl.textContent = message || "";
  statusEl.classList.toggle("unsupported", isError);
}

function normalizeForSpeech(text) {
  return text
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
    .replace(/\.\.\./g, ", ")
    .replace(/"/g, "");
}

function getLocalVoiceValue(voice) {
  return `local:${voice.name}`;
}

function addGoogleTTSOption() {
  if (!voiceSelect) return;
  const option = document.createElement("option");
  option.value = GOOGLE_TTS_VALUE;
  option.textContent = "Google TTS（在线固定）";
  voiceSelect.appendChild(option);
}

function chooseDefaultVoice(previousValue) {
  if (!voiceSelect) return;
  const values = Array.from(voiceSelect.options).map((option) => option.value);
  voiceSelect.value = previousValue && values.includes(previousValue) ? previousValue : GOOGLE_TTS_VALUE;
}

function loadVoices() {
  if (!voiceSelect) return;
  const previousValue = voiceSelect.value || GOOGLE_TTS_VALUE;
  voiceSelect.disabled = false;
  voiceSelect.innerHTML = "";
  addGoogleTTSOption();

  if (!("speechSynthesis" in window)) {
    voices = [];
    chooseDefaultVoice(previousValue);
    setStatus("当前浏览器不支持本地 TTS，可使用 Google TTS。");
    return;
  }

  voices = window.speechSynthesis.getVoices();
  const englishVoices = voices.filter((voice) => /^en/i.test(voice.lang));
  const source = englishVoices.length ? englishVoices : voices;

  source.forEach((voice) => {
    const option = document.createElement("option");
    option.value = getLocalVoiceValue(voice);
    option.textContent = `${voice.name} (${voice.lang})`;
    voiceSelect.appendChild(option);
  });

  chooseDefaultVoice(previousValue);
  setStatus("");
}

function clearActiveButton() {
  if (!activeButton) return;
  activeButton.classList.remove("is-speaking");
  activeButton = null;
}

function stopCurrentSpeech() {
  if ("speechSynthesis" in window) {
    window.speechSynthesis.cancel();
  }
  if (currentAudio) {
    currentAudio.pause();
    currentAudio.removeAttribute("src");
    currentAudio.load();
    currentAudio = null;
  }
  clearActiveButton();
}

function markSpeaking(button, message) {
  clearActiveButton();
  activeButton = button;
  button.classList.add("is-speaking");
  setStatus(message);
}

function finishSpeaking(button, message = "", isError = false) {
  if (button) button.classList.remove("is-speaking");
  if (activeButton === button) activeButton = null;
  setStatus(message, isError);
}

function playGoogleTTS(text, button) {
  stopCurrentSpeech();
  const speechText = normalizeForSpeech(text);
  const url = `https://tts.keepme.xyz/translate_tts?ie=UTF-8&client=tw-ob&q=${encodeURIComponent(speechText)}&tl=en`;
  const audio = new Audio(url);
  currentAudio = audio;
  markSpeaking(button, "Google TTS 朗读中...");

  audio.onended = () => {
    if (currentAudio === audio) currentAudio = null;
    finishSpeaking(button);
  };
  audio.onerror = () => {
    if (currentAudio === audio) currentAudio = null;
    finishSpeaking(button, "Google TTS 无法播放，可切换本地语音。", true);
  };

  audio.play().catch(() => {
    if (currentAudio === audio) currentAudio = null;
    finishSpeaking(button, "Google TTS 播放被浏览器拦截或网络不可用。", true);
  });
}

function playLocalTTS(text, button) {
  if (!("speechSynthesis" in window)) {
    setStatus("当前浏览器不支持本地 TTS。", true);
    return;
  }

  stopCurrentSpeech();
  const utterance = new SpeechSynthesisUtterance(normalizeForSpeech(text));
  utterance.lang = "en-GB";
  utterance.rate = 0.86;
  utterance.pitch = 1;

  const selectedName = voiceSelect.value.replace(/^local:/, "");
  const selected = voices.find((voice) => voice.name === selectedName);
  if (selected) {
    utterance.voice = selected;
    utterance.lang = selected.lang;
  }

  markSpeaking(button, "本地 TTS 朗读中...");
  utterance.onend = () => finishSpeaking(button);
  utterance.onerror = () => finishSpeaking(button, "本地朗读被中断或不可用。", true);
  window.speechSynthesis.speak(utterance);
}

function speak(text, button) {
  if (!voiceSelect || voiceSelect.value === GOOGLE_TTS_VALUE) {
    playGoogleTTS(text, button);
  } else {
    playLocalTTS(text, button);
  }
}

function clearLinkedState(scope) {
  scope.querySelectorAll(".is-linked").forEach((item) => item.classList.remove("is-linked"));
}

function revealLinkedTranslation(chunk) {
  const line = chunk.closest(".reader-line");
  if (!line) return;
  clearLinkedState(line);
  chunk.classList.add("is-linked");
  const linked = line.querySelector(`.translation[data-index="${chunk.dataset.index}"]`);
  if (linked) {
    linked.classList.add("is-visible", "is-linked");
    linked.focus({ preventScroll: true });
  }
}

document.addEventListener("click", (event) => {
  const target = event.target;
  const readButton = target.closest(".read-btn");
  if (readButton) {
    speak(readButton.dataset.text, readButton);
    return;
  }

  const sentenceChunk = target.closest(".sentence-chunk");
  if (sentenceChunk) {
    revealLinkedTranslation(sentenceChunk);
    return;
  }

  const translation = target.closest(".translation");
  if (translation) {
    const line = translation.closest(".reader-line");
    if (line) clearLinkedState(line);
    translation.classList.add("is-visible", "is-linked");
    translation.focus({ preventScroll: true });
  }
});

document.addEventListener("focusin", (event) => {
  const target = event.target;
  if (target.classList && target.classList.contains("translation")) {
    target.classList.add("is-visible");
  }
});

document.addEventListener("focusout", (event) => {
  const target = event.target;
  if (!target.classList || !target.classList.contains("translation")) return;
  const line = target.closest(".reader-line");
  target.classList.remove("is-visible", "is-linked");
  if (line && !line.contains(event.relatedTarget)) {
    clearLinkedState(line);
  }
});

function updateTopButton() {
  if (!topButton) return;
  topButton.classList.toggle("is-visible", window.scrollY > 360);
}

if (stopButton) {
  stopButton.addEventListener("click", () => {
    stopCurrentSpeech();
    setStatus("已停止朗读。");
  });
}

if (topButton) {
  topButton.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

loadVoices();
if ("speechSynthesis" in window) {
  window.speechSynthesis.onvoiceschanged = loadVoices;
}
updateTopButton();
window.addEventListener("scroll", updateTopButton, { passive: true });
