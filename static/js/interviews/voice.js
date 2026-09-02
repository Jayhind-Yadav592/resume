/**
 * ResumeForge AI — Real-Time Conversational Mock Interview Engine
 * Provides autonomous real-time interview loop:
 * AI Speaks -> Auto Listening -> Live Speech Transcription -> Silence Detection -> Auto Process -> AI Responds.
 * Supports Barge-In / Interruption, Audio Autoplay Unblockers, Tech Pronunciation, and Pacing Metrics.
 */

(function () {
  'use strict';

  // Check Web Speech API Support
  const SpeechRecognitionAPI = window.SpeechRecognition || window.webkitSpeechRecognition || null;
  const isSpeechSynthesisSupported = 'speechSynthesis' in window;
  const isSpeechRecognitionSupported = !!SpeechRecognitionAPI;

  // Interview States
  const STATES = {
    IDLE: 'IDLE',
    AI_SPEAKING: 'AI_SPEAKING',
    LISTENING: 'LISTENING',
    USER_SPEAKING: 'USER_SPEAKING',
    PROCESSING: 'PROCESSING',
    COMPLETED: 'COMPLETED'
  };

  let currentState = STATES.IDLE;
  let voiceModeEnabled = true;
  let isRecording = false;
  let isAiSpeaking = false;
  let recognitionInstance = null;
  let preferredVoice = null;
  let availableVoices = [];
  let silenceTimer = null;
  let currentTranscript = '';
  let speechStartTime = null;
  let lastSpokenText = '';
  let hasUserInteracted = false;
  let silenceDurationMs = 2200; // 2.2 seconds of silence triggers auto-submission

  const FILLER_WORD_REGEX = /\b(um|uh|like|basically|actually|literally|you know|sort of|kind of)\b/gi;

  // Technical pronunciation dictionary for natural speech
  const TECH_PRONUNCIATION_MAP = [
    [/\bAPI\b/g, 'A P I'],
    [/\bAPIs\b/g, 'A P I s'],
    [/\bREST\b/g, 'Rest'],
    [/\bRESTful\b/g, 'Rest full'],
    [/\bSQL\b/g, 'Sequel'],
    [/\bNoSQL\b/g, 'No Sequel'],
    [/\bPostgreSQL\b/gi, 'Postgres Q L'],
    [/\bPostgres\b/gi, 'Postgres'],
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
    [/\bWPM\b/g, 'Words Per Minute'],
    [/\bGraphQL\b/gi, 'Graph Q L'],
    [/\bKafka\b/gi, 'Khaf-ka'],
    [/\bRedis\b/gi, 'Red-iss'],
    [/\bKubernetes\b/gi, 'Koo-ber-net-ees'],
    [/\bK8s\b/gi, 'Kates'],
    [/\bOAuth\b/gi, 'O Auth'],
    [/\bgRPC\b/gi, 'G R P C']
  ];

  // DOM references
  let micBtn = null;
  let liveTranscriptBox = null;
  let stateStatusBadge = null;
  let captionTextEl = null;
  let pulseRing = null;
  let speakingStatus = null;
  let answerInput = null;
  let finishAnswerBtn = null;

  function initVoiceEngine() {
    micBtn = document.getElementById('btn-main-mic');
    liveTranscriptBox = document.getElementById('live-transcript-text');
    stateStatusBadge = document.getElementById('interview-state-badge');
    captionTextEl = document.getElementById('meet-caption-text');
    pulseRing = document.getElementById('ai-pulse-ring');
    speakingStatus = document.getElementById('ai-speaking-status');
    answerInput = document.getElementById('answer-input');
    finishAnswerBtn = document.getElementById('btn-finish-answer');

    // Autoplay unblocker on any initial tap
    const unlockAudio = () => {
      hasUserInteracted = true;
      if (isSpeechSynthesisSupported) {
        window.speechSynthesis.resume();
      }
    };
    window.addEventListener('click', unlockAudio, { passive: true });
    window.addEventListener('keydown', unlockAudio, { passive: true });
    window.addEventListener('touchstart', unlockAudio, { passive: true });

    if (isSpeechSynthesisSupported) {
      loadVoices();
      if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = loadVoices;
      }
    }

    if (micBtn) {
      micBtn.addEventListener('click', onMicButtonClicked);
    }

    if (finishAnswerBtn) {
      finishAnswerBtn.addEventListener('click', () => {
        finalizeAndSendAnswer();
      });
    }

    playEnterChime();
    setInterviewState(STATES.IDLE);
  }

  function playEnterChime() {
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
      gain1.gain.setValueAtTime(0.06, now);
      gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
      osc1.connect(gain1);
      gain1.connect(ctx.destination);
      osc1.start(now);
      osc1.stop(now + 0.3);

      // Note 2 (B5)
      const osc2 = ctx.createOscillator();
      const gain2 = ctx.createGain();
      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(987.77, now + 0.15);
      gain2.gain.setValueAtTime(0.08, now + 0.15);
      gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.6);
      osc2.connect(gain2);
      gain2.connect(ctx.destination);
      osc2.start(now + 0.15);
      osc2.stop(now + 0.6);
    } catch (e) {}
  }

  function loadVoices() {
    if (!isSpeechSynthesisSupported) return;
    const voices = window.speechSynthesis.getVoices();
    if (!voices || voices.length === 0) return;

    availableVoices = voices;

    const naturalUsFemale = voices.find(v => (v.name.includes('Aria') || v.name.includes('Jenny') || v.name.includes('Samantha') || v.name.includes('Zira') || v.name.includes('Natural')) && v.lang.startsWith('en'));
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

  // Set the current real-time State & Update UI
  function setInterviewState(newState, extraInfo = '') {
    currentState = newState;
    const badge = document.getElementById('interview-state-badge');
    const micBtnIcon = document.getElementById('mic-btn-icon');
    const micBtnText = document.getElementById('mic-btn-label');
    const pulseElement = document.getElementById('ai-pulse-ring');
    const aiStatusText = document.getElementById('ai-speaking-status');
    const userMicWave = document.getElementById('candidate-mic-icon');
    const liveTranscriptContainer = document.getElementById('live-transcript-container');

    switch (newState) {
      case STATES.IDLE:
        if (badge) {
          badge.className = 'badge bg-secondary-subtle text-secondary rounded-pill px-3 py-1.5';
          badge.innerHTML = '<i class="bi bi-circle-fill me-1.5 small text-secondary"></i> Ready';
        }
        if (aiStatusText) aiStatusText.innerHTML = 'Connecting to interviewer...';
        if (pulseElement) pulseElement.style.display = 'none';
        if (micBtn) {
          micBtn.className = 'mic-pulse-btn mic-btn-idle shadow';
          if (micBtnIcon) micBtnIcon.className = 'bi bi-mic text-white';
          if (micBtnText) micBtnText.textContent = 'Start Voice';
        }
        break;

      case STATES.AI_SPEAKING:
        if (badge) {
          badge.className = 'badge bg-primary text-white rounded-pill px-3 py-1.5 shadow-xs';
          badge.innerHTML = '<i class="bi bi-soundwave me-1.5 soundwave-bounce"></i> Interviewer is Speaking...';
        }
        if (aiStatusText) {
          aiStatusText.innerHTML = `
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
        if (pulseElement) pulseElement.style.display = 'block';
        if (micBtn) {
          micBtn.className = 'mic-pulse-btn mic-btn-interviewer-speaking shadow';
          if (micBtnIcon) micBtnIcon.className = 'bi bi-slash-circle text-white';
          if (micBtnText) micBtnText.textContent = 'Tap to Interrupt';
        }
        if (userMicWave) userMicWave.className = 'bi bi-mic-mute text-secondary ms-1';
        break;

      case STATES.LISTENING:
        if (badge) {
          badge.className = 'badge bg-danger text-white rounded-pill px-3 py-1.5 shadow-xs animate-pulse';
          badge.innerHTML = '<i class="bi bi-mic-fill me-1.5"></i> Listening to you... (Speak naturally)';
        }
        if (aiStatusText) {
          aiStatusText.innerHTML = '<span class="spinner-grow spinner-grow-sm text-primary me-1" style="width: 6px; height: 6px;"></span> Listening to you...';
        }
        if (pulseElement) pulseElement.style.display = 'none';
        if (micBtn) {
          micBtn.className = 'mic-pulse-btn mic-btn-listening shadow-lg';
          if (micBtnIcon) micBtnIcon.className = 'bi bi-mic-fill text-white';
          if (micBtnText) micBtnText.textContent = 'Listening (Tap when done)';
        }
        if (userMicWave) userMicWave.className = 'bi bi-mic-fill text-danger ms-1 animate-pulse';
        if (finishAnswerBtn) finishAnswerBtn.classList.remove('d-none');
        break;

      case STATES.USER_SPEAKING:
        if (badge) {
          badge.className = 'badge bg-danger text-white rounded-pill px-3 py-1.5 shadow-xs animate-pulse';
          badge.innerHTML = '<i class="bi bi-record-fill text-white me-1.5"></i> Capturing your answer...';
        }
        if (aiStatusText) {
          aiStatusText.innerHTML = '<span class="spinner-grow spinner-grow-sm text-success me-1" style="width: 6px; height: 6px;"></span> Listening to your response...';
        }
        if (pulseElement) pulseElement.style.display = 'none';
        if (micBtn) {
          micBtn.className = 'mic-pulse-btn mic-btn-user-speaking shadow-lg';
          if (micBtnIcon) micBtnIcon.className = 'bi bi-soundwave text-white';
          if (micBtnText) micBtnText.textContent = 'Speaking... (Pause to send)';
        }
        if (userMicWave) userMicWave.className = 'bi bi-soundwave text-success ms-1';
        if (finishAnswerBtn) finishAnswerBtn.classList.remove('d-none');
        break;

      case STATES.PROCESSING:
        if (badge) {
          badge.className = 'badge bg-warning-subtle text-dark border border-warning-subtle rounded-pill px-3 py-1.5';
          badge.innerHTML = '<span class="spinner-border spinner-border-sm me-1.5 text-warning" style="width: 12px; height: 12px;"></span> Interviewer is analyzing your response...';
        }
        if (aiStatusText) {
          aiStatusText.innerHTML = '<span class="spinner-border spinner-border-sm text-warning me-1" style="width: 8px; height: 8px;"></span> Analyzing response & preparing follow-up...';
        }
        if (pulseElement) pulseElement.style.display = 'none';
        if (micBtn) {
          micBtn.className = 'mic-pulse-btn mic-btn-processing shadow';
          if (micBtnIcon) micBtnIcon.className = 'spinner-border spinner-border-sm text-white';
          if (micBtnText) micBtnText.textContent = 'Processing...';
        }
        if (userMicWave) userMicWave.className = 'bi bi-hourglass-split text-warning ms-1';
        if (finishAnswerBtn) finishAnswerBtn.classList.add('d-none');
        break;

      case STATES.COMPLETED:
        if (badge) {
          badge.className = 'badge bg-success text-white rounded-pill px-3 py-1.5 shadow-xs';
          badge.innerHTML = '<i class="bi bi-award-fill me-1.5"></i> Interview Completed';
        }
        if (aiStatusText) aiStatusText.innerHTML = 'Session Concluded';
        if (pulseElement) pulseElement.style.display = 'none';
        if (micBtn) micBtn.classList.add('d-none');
        if (finishAnswerBtn) finishAnswerBtn.classList.add('d-none');
        break;
    }
  }

  // Speaks the question or transition phrase
  function speakInterviewerText(text, onSpeechEndCallback = null) {
    if (!text) return;
    lastSpokenText = text;

    // Interrupt any ongoing user speech recognition or current audio
    stopListening();

    if (!isSpeechSynthesisSupported || !voiceModeEnabled) {
      setInterviewState(STATES.AI_SPEAKING);
      if (captionTextEl) captionTextEl.textContent = text;
      // If voice not supported, wait 3.5s then switch to listening
      setTimeout(() => {
        setInterviewState(STATES.LISTENING);
        startListening();
        if (onSpeechEndCallback) onSpeechEndCallback();
      }, 3500);
      return;
    }

    window.speechSynthesis.resume();
    window.speechSynthesis.cancel();

    const spokenText = humanizeTextForSpeech(text);
    if (!spokenText) return;

    setInterviewState(STATES.AI_SPEAKING);
    if (captionTextEl) captionTextEl.textContent = text;
    isAiSpeaking = true;

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

      utterance.rate = 0.96;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;

      utterance.onstart = () => {
        isAiSpeaking = true;
        setInterviewState(STATES.AI_SPEAKING);
      };

      utterance.onend = () => {
        isAiSpeaking = false;
        // Natural slight pause (450ms) before opening microphone
        setTimeout(() => {
          if (currentState === STATES.AI_SPEAKING) {
            setInterviewState(STATES.LISTENING);
            startListening();
            if (onSpeechEndCallback) onSpeechEndCallback();
          }
        }, 450);
      };

      utterance.onerror = (err) => {
        console.warn('Speech synthesis error or interrupt:', err);
        isAiSpeaking = false;
        setInterviewState(STATES.LISTENING);
        startListening();
        if (onSpeechEndCallback) onSpeechEndCallback();
      };

      window.speechSynthesis.speak(utterance);
      window.speechSynthesis.resume();
    }, 60);
  }

  function stopSpeaking() {
    if (isSpeechSynthesisSupported) {
      window.speechSynthesis.cancel();
    }
    isAiSpeaking = false;
  }

  // Handle clicking the main round microphone button
  function onMicButtonClicked() {
    if (currentState === STATES.AI_SPEAKING) {
      // Barge-in: User is interrupting the AI!
      stopSpeaking();
      setInterviewState(STATES.LISTENING);
      startListening();
      return;
    }

    if (isRecording) {
      // User tapped to finish answer immediately
      finalizeAndSendAnswer();
    } else {
      // User tapped to speak
      setInterviewState(STATES.LISTENING);
      startListening();
    }
  }

  // Start continuous speech recognition with live streaming transcript
  function startListening() {
    if (!isSpeechRecognitionSupported) {
      showMicErrorNotice("Speech recognition isn't supported in this browser. Please type your response in the box below.");
      return;
    }

    if (isRecording) return;

    speechStartTime = Date.now();
    currentTranscript = '';

    // Clear previous live transcript UI
    if (liveTranscriptBox) {
      liveTranscriptBox.textContent = 'Listening to your voice...';
      liveTranscriptBox.classList.add('text-muted');
    }
    if (answerInput) {
      answerInput.value = '';
    }

    try {
      if (!recognitionInstance) {
        recognitionInstance = new SpeechRecognitionAPI();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = 'en-US';

        recognitionInstance.onstart = () => {
          isRecording = true;
          setInterviewState(STATES.LISTENING);
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

          const combined = (currentTranscript + ' ' + finalTranscript + ' ' + interimTranscript).trim();
          if (finalTranscript) {
            currentTranscript = (currentTranscript + ' ' + finalTranscript).trim();
          }

          const displayText = combined || interimTranscript;

          if (displayText.length > 0) {
            setInterviewState(STATES.USER_SPEAKING);
            if (liveTranscriptBox) {
              liveTranscriptBox.textContent = `"${displayText}"`;
              liveTranscriptBox.classList.remove('text-muted');
            }
            if (answerInput) {
              answerInput.value = displayText;
              answerInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
            analyzeSpeechMetrics(displayText);
          }
        };

        recognitionInstance.onspeechend = () => {
          startSilenceTimer();
        };

        recognitionInstance.onerror = (event) => {
          if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
            showMicErrorNotice("Microphone permission was denied. Please allow microphone access in browser settings to speak, or type your answer.");
          } else if (event.error !== 'no-speech') {
            console.warn('Speech recognition notice:', event.error);
          }
          isRecording = false;
        };

        recognitionInstance.onend = () => {
          isRecording = false;
          clearSilenceTimer();
          // If the user was speaking and recognition stopped naturally, finalize answer
          if (currentState === STATES.USER_SPEAKING && currentTranscript.trim().length > 0) {
            finalizeAndSendAnswer();
          }
        };
      }

      hideMicErrorNotice();
      recognitionInstance.start();
      isRecording = true;
    } catch (err) {
      console.warn('Speech recognition start error:', err);
      isRecording = false;
    }
  }

  function stopListening() {
    if (recognitionInstance && isRecording) {
      try {
        recognitionInstance.stop();
      } catch (e) {}
    }
    isRecording = false;
    clearSilenceTimer();
  }

  function startSilenceTimer() {
    clearSilenceTimer();
    silenceTimer = setTimeout(() => {
      finalizeAndSendAnswer();
    }, silenceDurationMs);
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

  // Finalizes the speech and triggers backend analysis
  function finalizeAndSendAnswer() {
    stopListening();
    clearSilenceTimer();

    const textToSend = (answerInput ? answerInput.value.trim() : '') || currentTranscript.trim();

    if (!textToSend) {
      // Nothing spoken yet, remain in listening state
      setInterviewState(STATES.LISTENING);
      return;
    }

    setInterviewState(STATES.PROCESSING);

    // Call window.submitCandidateAnswer from interview_chat.html
    if (window.handleAutoSubmitAnswer) {
      window.handleAutoSubmitAnswer(textToSend);
    }
  }

  function analyzeSpeechMetrics(text) {
    if (!text) return;
    const words = text.trim().split(/\s+/);
    const wordCount = words.length;

    // Detect Filler Words
    const matches = text.match(FILLER_WORD_REGEX);
    const totalFillerWords = matches ? matches.length : 0;
    const fillerEl = document.getElementById('speech-filler-count');
    if (fillerEl) fillerEl.textContent = totalFillerWords;

    // Calculate WPM Pacing
    if (speechStartTime && wordCount > 3) {
      const elapsedMinutes = (Date.now() - speechStartTime) / 60000;
      if (elapsedMinutes > 0.03) {
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

  function showMicErrorNotice(msg) {
    const noticeEl = document.getElementById('mic-error-notice');
    if (noticeEl) {
      noticeEl.innerHTML = `<i class="bi bi-exclamation-triangle-fill me-1.5 text-warning"></i> ${msg}`;
      noticeEl.classList.remove('d-none');
    }
  }

  function hideMicErrorNotice() {
    const noticeEl = document.getElementById('mic-error-notice');
    if (noticeEl) {
      noticeEl.classList.add('d-none');
      noticeEl.innerHTML = '';
    }
  }

  // Export VoiceInterview global API
  window.VoiceInterview = {
    init: initVoiceEngine,
    speak: speakInterviewerText,
    replay: () => speakInterviewerText(lastSpokenText),
    stopSpeaking: stopSpeaking,
    startListening: startListening,
    stopListening: stopListening,
    finalizeAnswer: finalizeAndSendAnswer,
    setState: setInterviewState,
    STATES: STATES,
    isSpeechSynthesisSupported: () => isSpeechSynthesisSupported,
    isSpeechRecognitionSupported: () => isSpeechRecognitionSupported
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initVoiceEngine);
  } else {
    initVoiceEngine();
  }
})();

