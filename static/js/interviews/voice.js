/**
 * ResumeForge AI — Ultra-Humanlike Conversational Voice Engine
 * Uses Web Speech Synthesis & Recognition with Natural Voice Filtering,
 * Tech Acronym Expansion, Pacing Intelligence, Autoplay Unblockers, and Live Equalizers.
 */

(function () {
  'use strict';

  const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition || null;
  const isSpeechSynthesisSupported = 'speechSynthesis' in window;
  const isSpeechRecognitionSupported = !!SpeechRecognitionAPI;

  let voiceModeEnabled = true;
  let isRecording = false;
  let recognitionInstance = null;
  let preferredVoice = null;
  let availableVoices = [];
  let silenceTimer = null;
  let transcriptBase = '';
  let speechStartTime = null;
  let totalFillerWords = 0;
  let lastSpokenText = '';

  const FILLER_WORD_REGEX = /\b(um|uh|like|basically|actually|literally|you know|sort of|kind of)\b/gi;

  // Technical pronunciation dictionary for natural speech
  const TECH_PRONUNCIATION_MAP = [
    [/\bAPI\b/g, 'A P I'],
    [/\bAPIs\b/g, 'A P I s'],
    [/\bREST\b/g, 'Rest'],
    [/\bSQL\b/g, 'Sequel'],
    [/\bNoSQL\b/g, 'No Sequel'],
    [/\bPostgreSQL\b/gi, 'Postgres Q L'],
    [/\bAWS\b/g, 'A W S'],
    [/\bGCP\b/g, 'G C P'],
    [/\bCI\/CD\b/gi, 'C I C D'],
    [/\bDRF\b/g, 'Django REST Framework'],
    [/\bUI\/UX\b/gi, 'U I U X'],
    [/\bJSON\b/g, 'Jason'],
    [/\bHTML\b/g, 'H T M L'],
    [/\bCSS\b/g, 'C S S'],
    [/\bJWT\b/g, 'J W T'],
    [/\bDSA\b/g, 'D S A'],
    [/\bWPM\b/g, 'Words Per Minute']
  ];

  let micBtn = null;
  let voiceToggle = null;
  let voiceStatusLabel = null;
  let answerTextarea = null;
  let voiceSupportNotice = null;
  let voiceSelectEl = null;

  function initVoiceMode() {
    micBtn = document.getElementById('btn-mic');
    voiceToggle = document.getElementById('voice-mode-toggle');
    voiceStatusLabel = document.getElementById('voice-recording-status');
    answerTextarea = document.getElementById('answer-input');
    voiceSupportNotice = document.getElementById('voice-support-notice');
    voiceSelectEl = document.getElementById('interviewer-voice-select');

    // Global Browser Autoplay Unblocker: Resume SpeechSynthesis on any user click or touch
    const unblockAudio = () => {
      if (isSpeechSynthesisSupported) {
        window.speechSynthesis.resume();
      }
    };
    window.addEventListener('click', unblockAudio, { passive: true });
    window.addEventListener('keydown', unblockAudio, { passive: true });
    window.addEventListener('touchstart', unblockAudio, { passive: true });

    const savedPref = localStorage.getItem('resumeforge_voice_mode');
    if (savedPref !== null) {
      voiceModeEnabled = savedPref === 'true';
    }

    if (voiceToggle) {
      if (!isSpeechSynthesisSupported && !isSpeechRecognitionSupported) {
        const toggleContainer = document.getElementById('voice-mode-toggle-container');
        if (toggleContainer) toggleContainer.classList.add('d-none');
      } else {
        voiceToggle.checked = voiceModeEnabled;
        voiceToggle.addEventListener('change', (e) => {
          voiceModeEnabled = e.target.checked;
          localStorage.setItem('resumeforge_voice_mode', voiceModeEnabled);
          updateVoiceUIState();
          if (!voiceModeEnabled) {
            stopSpeaking();
            if (isRecording) stopListening();
          }
        });
      }
    }

    if (micBtn) {
      if (!isSpeechRecognitionSupported) {
        micBtn.classList.add('d-none');
        if (voiceSupportNotice) {
          voiceSupportNotice.textContent = "Voice input isn't supported in this browser — please type your answer.";
          voiceSupportNotice.classList.remove('d-none');
        }
      } else {
        micBtn.addEventListener('click', toggleMicListening);
      }
    }

    if (isSpeechSynthesisSupported) {
      loadVoices();
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices;
      }
    }

    // Play subtle modern meeting enter chime
    playJoinChime();

    updateVoiceUIState();
  }

  function playJoinChime() {
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return;
      const ctx = new AudioCtx();
      const now = ctx.currentTime;

      // Note 1 (E5)
      const osc1 = ctx.createOscillator();
      const gain1 = ctx.createGain();
      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(659.25, now);
      gain1.gain.setValueAtTime(0.08, now);
      gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
      osc1.connect(gain1);
      gain1.connect(ctx.destination);
      osc1.start(now);
      osc1.stop(now + 0.35);

      // Note 2 (G#5)
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(830.61, now + 0.12);
      gain2.gain.setValueAtTime(0.1, now + 0.12);
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.55);
      osc2.connect(gain2);
      gain2.connect(ctx.destination);
      osc2.start(now + 0.12);
      osc2.stop(now + 0.55);

      // Note 3 (B5)
      const osc3 = ctx.createOscillator();
      const gain3 = ctx.createGain();
      osc3.type = 'sine';
      osc3.frequency.setValueAtTime(987.77, now + 0.24);
      gain3.gain.setValueAtTime(0.12, now + 0.24);
      gain3.gain.exponentialRampToValueAtTime(0.001, now + 0.85);
      osc3.connect(gain3);
      gain3.connect(ctx.destination);
      osc3.start(now + 0.24);
      osc3.stop(now + 0.85);
    } catch (e) {}
  }

  function updateVoiceUIState() {
    if (micBtn && isSpeechRecognitionSupported) {
      if (voiceModeEnabled) {
        micBtn.classList.remove('d-none');
      } else {
        micBtn.classList.add('d-none');
      }
    }
  }

  function loadVoices() {
    if (!isSpeechSynthesisSupported) return;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return;

    availableVoices = voices;

    // Intelligent Humanlike Natural Voice Ranking
    const naturalUsFemale = voices.find(v => (v.name.includes('Aria') || v.name.includes('Jenny') || v.name.includes('Samantha') || v.name.includes('Zira')) && v.lang.startsWith('en'));
    const naturalUsMale = voices.find(v => (v.name.includes('Guy') || v.name.includes('Alex') || v.name.includes('David') || v.name.includes('Christopher')) && v.lang.startsWith('en'));
    const googleVoice = voices.find(v => v.name.includes('Google') && v.lang.startsWith('en'));
    const indianNatural = voices.find(v => (v.name.includes('Neerja') || v.name.includes('Prabhat') || v.name.includes('Heera')) || (v.lang === 'en-IN' || v.lang === 'en_IN'));

    const savedVoiceURI = localStorage.getItem('resumeforge_selected_voice_uri');
    if (savedVoiceURI) {
      preferredVoice = voices.find(v => v.voiceURI === savedVoiceURI);
    }

    if (!preferredVoice) {
      preferredVoice = naturalUsFemale || naturalUsMale || googleVoice || indianNatural || voices.find(v => v.lang.startsWith('en')) || voices[0];
    }

    populateVoiceSelector(voices);
  }

  function populateVoiceSelector(voices) {
    if (!voiceSelectEl) return;

    const englishVoices = voices.filter(v => v.lang.startsWith('en'));
    const listToRender = englishVoices.length > 0 ? englishVoices : voices;

    voiceSelectEl.innerHTML = '';
    listToRender.forEach(v => {
      const opt = document.createElement('option');
      opt.value = v.voiceURI;
      let label = v.name.replace(/Microsoft|Google|Apple|Natural|Desktop|Online/gi, '').trim();
      if (v.lang) label += ` (${v.lang})`;
      opt.textContent = label;
      if (preferredVoice && v.voiceURI === preferredVoice.voiceURI) {
        opt.selected = true;
      }
      voiceSelectEl.appendChild(opt);
    });

    voiceSelectEl.onchange = (e) => {
      const chosen = voices.find(v => v.voiceURI === e.target.value);
      if (chosen) {
        preferredVoice = chosen;
        localStorage.setItem('resumeforge_selected_voice_uri', chosen.voiceURI);
      }
    };
  }

  function humanizeTextForSpeech(text) {
    if (!text) return '';
    let cleaned = text.replace(/[*_~`#]/g, ' ').trim();
    cleaned = cleaned.replace(/\s+/g, ' ');

    TECH_PRONUNCIATION_MAP.forEach(([regex, replacement]) => {
      cleaned = cleaned.replace(regex, replacement);
    });

    return cleaned;
  }

  function speakText(text, isManualReplay = false, triggerBtn = null) {
    if (!isSpeechSynthesisSupported) return;
    if (!isManualReplay && !voiceModeEnabled) return;

    lastSpokenText = text;

    // Chrome workaround: resume before speak
    window.speechSynthesis.resume();
    window.speechSynthesis.cancel();

    const spokenText = humanizeTextForSpeech(text);
    if (!spokenText) return;

    // Small delay prevents Chrome from aborting immediately after cancel()
    setTimeout(() => {
      const utterance = new SpeechSynthesisUtterance(spokenText);
      
      if (!preferredVoice && availableVoices.length > 0) {
        loadVoices();
      }

      if (preferredVoice) {
        utterance.voice = preferredVoice;
        utterance.lang = preferredVoice.lang;
      } else {
        utterance.lang = 'en-US';
      }

      // Natural human cadence
      utterance.rate = 0.95;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      const pulseRing = document.getElementById('ai-pulse-ring');
      const speakingStatus = document.getElementById('ai-speaking-status');
      const tileVoiceBtn = document.getElementById('btn-tile-hear-ai');

      utterance.onstart = () => {
        if (pulseRing) pulseRing.style.display = 'block';
        if (tileVoiceBtn) tileVoiceBtn.classList.add('d-none');
        if (speakingStatus) {
          speakingStatus.innerHTML = `
            <span class="badge bg-success rounded-pill px-2.5 py-1 d-inline-flex align-items-center gap-1.5 shadow-sm">
              <span class="soundwave-bars">
                <span class="soundwave-bar"></span>
                <span class="soundwave-bar"></span>
                <span class="soundwave-bar"></span>
                <span class="soundwave-bar"></span>
              </span>
              <span>Interviewer Speaking...</span>
            </span>
          `;
        }
      };

      utterance.onend = () => {
        if (pulseRing) pulseRing.style.display = 'none';
        if (speakingStatus) {
          speakingStatus.innerHTML = '<span class="spinner-grow spinner-grow-sm text-primary me-1" style="width: 6px; height: 6px;"></span> Listening to you...';
        }
        if (triggerBtn) {
          triggerBtn.innerHTML = '<i class="bi bi-volume-up text-secondary" style="font-size: 0.8rem;"></i>';
        }
      };

      utterance.onerror = (err) => {
        console.warn('Speech synthesis notice:', err);
        if (pulseRing) pulseRing.style.display = 'none';
        if (tileVoiceBtn) tileVoiceBtn.classList.remove('d-none');
        if (speakingStatus) {
          speakingStatus.innerHTML = '<span class="spinner-grow spinner-grow-sm text-primary me-1" style="width: 6px; height: 6px;"></span> Listening to you...';
        }
        if (triggerBtn) {
          triggerBtn.innerHTML = '<i class="bi bi-volume-up text-secondary" style="font-size: 0.8rem;"></i>';
        }
      };

      if (triggerBtn) {
        triggerBtn.innerHTML = '<i class="bi bi-volume-up-fill text-primary" style="font-size: 0.8rem;"></i>';
      }

      window.speechSynthesis.speak(utterance);
      window.speechSynthesis.resume();
    }, 60);
  }

  function replayLastQuestion() {
    if (lastSpokenText) {
      speakText(lastSpokenText, true);
    }
  }

  function stopSpeaking() {
    if (isSpeechSynthesisSupported) {
      window.speechSynthesis.cancel();
    }
    const pulseRing = document.getElementById('ai-pulse-ring');
    const speakingStatus = document.getElementById('ai-speaking-status');
    if (pulseRing) pulseRing.style.display = 'none';
    if (speakingStatus) {
      speakingStatus.innerHTML = '<span class="spinner-grow spinner-grow-sm text-primary me-1" style="width: 6px; height: 6px;"></span> Ready';
    }
  }

  function analyzeSpeechMetrics(text) {
    if (!text) return;
    const words = text.trim().split(/\s+/);
    const wordCount = words.length;

    // Detect Filler Words
    const matches = text.match(FILLER_WORD_REGEX);
    totalFillerWords = matches ? matches.length : 0;
    const fillerEl = document.getElementById('speech-filler-count');
    if (fillerEl) fillerEl.textContent = totalFillerWords;

    // Calculate WPM Pacing
    if (speechStartTime && wordCount > 3) {
      const elapsedMinutes = (Date.now() - speechStartTime) / 60000;
      if (elapsedMinutes > 0.04) {
        const wpm = Math.round(wordCount / elapsedMinutes);
        const wpmEl = document.getElementById('speech-wpm-val');
        const badgeEl = document.getElementById('speech-pacing-badge');

        if (wpmEl) wpmEl.textContent = `${wpm} WPM`;

        if (badgeEl) {
          if (wpm < 110) {
            badgeEl.className = 'badge bg-warning-subtle text-warning py-0 px-1.5';
            badgeEl.textContent = 'Slow';
          } else if (wpm > 175) {
            badgeEl.className = 'badge bg-danger-subtle text-danger py-0 px-1.5';
            badgeEl.textContent = 'Fast';
          } else {
            badgeEl.className = 'badge bg-success-subtle text-success py-0 px-1.5';
            badgeEl.textContent = 'Ideal Pace';
          }
        }
      }
    }
  }

  function toggleMicListening() {
    if (!isSpeechRecognitionSupported) return;

    if (isRecording) {
      stopListening();
    } else {
      startListening();
    }
  }

  function startListening() {
    if (!isSpeechRecognitionSupported || isRecording) return;

    stopSpeaking();
    speechStartTime = Date.now();

    try {
      if (!recognitionInstance) {
        recognitionInstance = new SpeechRecognitionAPI();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = 'en-US';

        recognitionInstance.onstart = () => {
          isRecording = true;
          setMicRecordingUI(true);
        };

        recognitionInstance.onresult = (event) => {
          resetSilenceTimer();
          let interimTranscript = '';
          let finalTranscript = '';

          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript;
            } else {
              interimTranscript += event.results[i][0].transcript;
            }
          }

          if (answerTextarea) {
            const currentFinal = transcriptBase + (finalTranscript ? (transcriptBase ? ' ' : '') + finalTranscript : '');
            if (finalTranscript) {
              transcriptBase = currentFinal;
            }
            const displayTranscript = currentFinal + (interimTranscript ? (currentFinal ? ' ' : '') + interimTranscript : '');
            answerTextarea.value = displayTranscript;
            answerTextarea.dispatchEvent(new Event('input', { bubbles: true }));

            analyzeSpeechMetrics(displayTranscript);
          }
        };

        recognitionInstance.onspeechend = () => {
          startSilenceTimer();
        };

        recognitionInstance.onerror = (event) => {
          if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
            showInlineVoiceNotice("Microphone access denied — you can still type your answer.");
          } else if (event.error !== 'no-speech') {
            console.warn('Speech recognition notice:', event.error);
          }
          stopListening();
        };

        recognitionInstance.onend = () => {
          isRecording = false;
          setMicRecordingUI(false);
          clearSilenceTimer();
        };
      }

      if (answerTextarea) {
        transcriptBase = answerTextarea.value.trim();
      }

      hideInlineVoiceNotice();
      recognitionInstance.start();
    } catch (err) {
      console.warn('Speech recognition start error:', err);
      stopListening();
    }
  }

  function stopListening() {
    if (recognitionInstance && isRecording) {
      try {
        recognitionInstance.stop();
      } catch (e) {}
    }
    isRecording = false;
    setMicRecordingUI(false);
    clearSilenceTimer();
  }

  function startSilenceTimer() {
    clearSilenceTimer();
    silenceTimer = setTimeout(() => {
      stopListening();
    }, 3500);
  }

  function resetSilenceTimer() {
    if (silenceTimer) {
      clearSilenceTimer();
      startSilenceTimer();
    }
  }

  function clearSilenceTimer() {
    if (silenceTimer) {
      clearTimeout(silenceTimer);
      silenceTimer = null;
    }
  }

  function setMicRecordingUI(active) {
    if (!micBtn) return;

    if (active) {
      micBtn.className = 'btn btn-danger px-3.5 shadow-sm position-relative';
      micBtn.innerHTML = '<i class="bi bi-mic-fill"></i>';
      micBtn.setAttribute('title', 'Listening... Tap to stop');
      if (voiceStatusLabel) {
        voiceStatusLabel.innerHTML = '<span class="spinner-grow spinner-grow-sm text-danger me-1" style="width: 8px; height: 8px;"></span> <span class="text-danger fw-bold">Listening to you...</span>';
        voiceStatusLabel.classList.remove('d-none');
      }
    } else {
      micBtn.className = 'btn btn-outline-custom px-3.5 shadow-none';
      micBtn.innerHTML = '<i class="bi bi-mic text-secondary"></i>';
      micBtn.setAttribute('title', 'Speak your answer');
      if (voiceStatusLabel) {
        voiceStatusLabel.classList.add('d-none');
        voiceStatusLabel.innerHTML = '';
      }
    }
  }

  function showInlineVoiceNotice(msg) {
    if (voiceSupportNotice) {
      voiceSupportNotice.textContent = msg;
      voiceSupportNotice.classList.remove('d-none');
    }
  }

  function hideInlineVoiceNotice() {
    if (voiceSupportNotice) {
      voiceSupportNotice.classList.add('d-none');
      voiceSupportNotice.textContent = '';
    }
  }

  window.VoiceInterview = {
    init: initVoiceMode,
    speak: speakText,
    replay: replayLastQuestion,
    stopSpeaking: stopSpeaking,
    isSpeechSynthesisSupported: () => isSpeechSynthesisSupported,
    isSpeechRecognitionSupported: () => isSpeechRecognitionSupported,
    isVoiceModeEnabled: () => voiceModeEnabled
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVoiceMode);
  } else {
    initVoiceMode();
  }
})();
