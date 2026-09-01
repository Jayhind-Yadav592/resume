/**
 * Voice Mode Engine for ResumeForge AI Mock Interview
 * Uses native Web Speech API (SpeechSynthesis & SpeechRecognition)
 * Features real-time Speech Intelligence: WPM (Words Per Minute) Pacing & Filler Word Tracking.
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
  let silenceTimer = null;
  let transcriptBase = '';
  let speechStartTime = null;
  let totalFillerWords = 0;

  const FILLER_WORD_REGEX = /\b(um|uh|like|basically|actually|literally|you know|sort of|kind of)\b/gi;

  let micBtn = null;
  let voiceToggle = null;
  let voiceStatusLabel = null;
  let answerTextarea = null;
  let voiceSupportNotice = null;

  function initVoiceMode() {
    micBtn = document.getElementById('btn-mic');
    voiceToggle = document.getElementById('voice-mode-toggle');
    voiceStatusLabel = document.getElementById('voice-recording-status');
    answerTextarea = document.getElementById('answer-input');
    voiceSupportNotice = document.getElementById('voice-support-notice');

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

    updateVoiceUIState();
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

    preferredVoice = voices.find(v => (v.lang === 'en-IN' || v.lang === 'en_IN') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Neural'))) ||
                     voices.find(v => v.lang === 'en-IN' || v.lang === 'en_IN') ||
                     voices.find(v => (v.lang === 'en-US' || v.lang === 'en_US') && (v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('Google') || v.name.includes('Jenny') || v.name.includes('Guy'))) ||
                     voices.find(v => v.lang.startsWith('en')) ||
                     voices[0];
  }

  function speakText(text, isManualReplay = false, triggerBtn = null) {
    if (!isSpeechSynthesisSupported) return;
    if (!isManualReplay && !voiceModeEnabled) return;

    stopSpeaking();

    const cleanText = text.replace(/[*_~`#]/g, '').trim();
    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.lang = preferredVoice ? preferredVoice.lang : 'en-US';

    if (triggerBtn) {
      const origIcon = triggerBtn.innerHTML;
      triggerBtn.innerHTML = '<i class="bi bi-volume-up-fill text-primary"></i>';
      triggerBtn.classList.add('btn-primary-subtle');

      utterance.onend = () => {
        triggerBtn.innerHTML = origIcon;
        triggerBtn.classList.remove('btn-primary-subtle');
      };
      utterance.onerror = () => {
        triggerBtn.innerHTML = origIcon;
        triggerBtn.classList.remove('btn-primary-subtle');
      };
    }

    window.speechSynthesis.speak(utterance);
  }

  function stopSpeaking() {
    if (isSpeechSynthesisSupported && window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
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

    // Calculate WPM
    if (speechStartTime && wordCount > 3) {
      const elapsedMinutes = (Date.now() - speechStartTime) / 60000;
      if (elapsedMinutes > 0.05) {
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
    }, 3000);
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
        voiceStatusLabel.innerHTML = '<span class="spinner-grow spinner-grow-sm text-danger me-1" style="width: 8px; height: 8px;"></span> <span class="text-danger fw-bold">Listening...</span>';
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
